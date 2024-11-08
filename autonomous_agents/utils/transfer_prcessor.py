import json
import asyncio
import signal
from web3 import Web3
from eth_account import Account
from redis.asyncio import Redis
from ..config import REDIS_URL, ERC20_ABI
from ..utils.logger import logger

class TransferProcessor:
    def __init__(self):
        self.redis = None
        self.running = True

    async def initialize(self):
        """Initialize Redis connection."""
        if not self.redis:
            self.redis = Redis.from_url(REDIS_URL, decode_responses=True)

    async def publish_status(self, agent_name: str, status_data: dict):
        """Publish transfer status update to agent-specific channel."""
        status_channel = f"transfer_status_{agent_name}"
        await self.redis.set(status_channel, json.dumps(status_data))

    async def process_transfer(self, transfer_data: dict):
        """Process a single transfer."""
        try:
            web3 = Web3(Web3.HTTPProvider(transfer_data['web3_provider']))
            token_contract = web3.eth.contract(
                address=web3.to_checksum_address(transfer_data['token_address']),
                abi=json.loads(ERC20_ABI)
            )
            source_address = web3.to_checksum_address(transfer_data['source_address'])
            target_address = web3.to_checksum_address(transfer_data['target_address'])
            private_key = transfer_data['private_key']
            agent_name = transfer_data['agent_name']
            
            logger.info(f"📝 Processing transfer request from {agent_name}")
            logger.info(f"   From: {source_address[:6]}...{source_address[-4:]}")
            logger.info(f"   To: {target_address[:6]}...{target_address[-4:]}")
            
            # Check balance
            balance = token_contract.functions.balanceOf(source_address).call()
            if balance >= transfer_data['amount']:
                nonce = web3.eth.get_transaction_count(source_address)
                transfer_function = token_contract.functions.transfer(
                    target_address,
                    transfer_data['amount']
                )
                
                txn = transfer_function.build_transaction({
                    'from': source_address,
                    'nonce': nonce,
                    'gas': 1000000,
                    'gasPrice': int(web3.eth.gas_price * 1.1),
                    'chainId': web3.eth.chain_id
                })
                
                signed_txn = Account.sign_transaction(txn, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                
                logger.info(f"📤 Transaction sent by {agent_name}")
                logger.info(f"   TX Hash: {tx_hash.hex()}")
                
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                block = web3.eth.get_block(receipt['blockNumber'])
                
                if receipt['status'] == 1:
                    await self.publish_status(agent_name, {
                        'status': 'success',
                        'source_address': source_address,
                        'sender': receipt['from'],
                        'tx_hash': tx_hash.hex(),
                        'block_number': receipt['blockNumber'],
                        'gas_used': receipt['gasUsed'],
                        'timestamp': block['timestamp']
                    })
                    
                    logger.info(f"✅ Transfer completed for {agent_name}")
                    logger.info(f"   Block: {receipt['blockNumber']}")
                    logger.info(f"   From: {receipt['from']}")
                    logger.info(f"   TX Hash: {tx_hash.hex()}")
                    logger.info(f"   Gas Used: {receipt['gasUsed']}")
                else:
                    await self.publish_status(agent_name, {
                        'status': 'error',
                        'source_address': source_address,
                        'error': 'Transaction failed'
                    })
                    logger.error(f"❌ Transfer failed for {agent_name}!")
            else:
                await self.publish_status(agent_name, {
                    'status': 'error',
                    'source_address': source_address,
                    'error': f'Insufficient balance: {balance}'
                })
                logger.warning(f"⚠️ Insufficient balance for {agent_name}: {balance}")
        
        except Exception as e:
            error_msg = str(e)
            await self.publish_status(agent_name, {
                'status': 'error',
                'source_address': source_address,
                'error': error_msg
            })
            logger.error(f"❌ Transfer processing error for {agent_name}: {error_msg}")

    async def run(self):
        """Main processing loop."""
        await self.initialize()
        logger.info("🚀 Transfer processor started")
        
        while self.running:
            try:
                # Pop transfer request with timeout
                result = await self.redis.brpop('crypto_transfers', timeout=1)
                if result:
                    _, transfer_data = result
                    transfer_dict = json.loads(transfer_data)
                    await self.process_transfer(transfer_dict)
            except Exception as e:
                logger.error(f"❌ Processor error: {str(e)}")
                await asyncio.sleep(1)

    async def shutdown(self):
        """Graceful shutdown."""
        logger.info("👋 Transfer processor shutting down...")
        self.running = False
        if self.redis:
            await self.redis.close()
        logger.info("✨ Transfer processor stopped")