import json
import asyncio
from typing import List
from web3 import Web3
from redis.asyncio import Redis
from ..handlers.base import MessageHandler
from ..core.message import Message, MessageType
from ..utils.logger import logger
from ..config import ERC20_ABI, REDIS_URL

class CryptoTransferHandler(MessageHandler):
    def __init__(
        self,
        web3: Web3,
        token_address: str,
        source_address: str,
        target_address: str,
        private_key: str,
        agent_name: str  # Add agent_name parameter
    ):
        self.web3 = web3
        self.token_address = token_address
        self.source_address = source_address
        self.target_address = target_address
        self.private_key = private_key
        self.agent_name = agent_name  # Store agent name
        self.redis = None

        # Initialize token contract
        self.token_contract = self.web3.eth.contract(
            address=self.web3.to_checksum_address(token_address),
            abi=json.loads(ERC20_ABI)
        )
        # Get token decimals
        self.decimals = self.token_contract.functions.decimals().call()

    async def initialize(self):
        """Initialize Redis connection."""
        if not self.redis:
            self.redis = Redis.from_url(REDIS_URL, decode_responses=True)
            
    async def check_status_updates(self):
        """Check for status updates from the processor."""
        status_channel = f"transfer_status_{self.agent_name}"
        result = await self.redis.get(status_channel)
        
        if result:
            status_data = json.loads(result)
            # Clear the status after reading
            await self.redis.delete(status_channel)
            
            if status_data['status'] == 'success':
                # Convert amount to decimal representation if present
                if 'amount' in status_data:
                    amount = int(status_data['amount']) / (10 ** self.decimals)
                    logger.info(f"✅ Transfer of {amount} tokens completed for {self.agent_name}!")
                else:
                    logger.info(f"✅ Transfer completed for {self.agent_name}!")
                logger.info(f"   Transaction Hash: {status_data['tx_hash']}")
                logger.info(f"   Block Number: {status_data['block_number']}")
                logger.info(f"   Sender: {status_data['sender']}")
                logger.info(f"   Gas Used: {status_data['gas_used']}")
            elif status_data['status'] == 'error':
                logger.error(f"❌ Transfer failed for {self.agent_name}: {status_data['error']}")


    def supported_message_types(self) -> List[MessageType]:
        return [MessageType.TEXT]

    async def can_handle(self, message: Message) -> bool:
        return (
            isinstance(message.content, str)
            and "crypto" in message.content.lower()
        )

    async def handle(self, message: Message, agent: 'AutonomousAgent') -> None:
        """Queue crypto transfer for background processing."""
        await self.initialize()
        
        # Check for any pending status updates
        await self.check_status_updates()
        
         # Calculate amount in token units (1 token = 10^decimals units)
        amount = 1 * (10 ** self.decimals)

        transfer_data = {
            'token_address': self.token_address,
            'source_address': self.source_address,
            'target_address': self.target_address,
            'private_key': self.private_key,
            'amount': amount,  
            'web3_provider': self.web3.provider.endpoint_uri,
            'agent_name': self.agent_name
        }
        
        await self.redis.lpush('crypto_transfers', json.dumps(transfer_data))
        
        logger.info(f"💸 Token transfer of 1 token queued by {self.agent_name}")
        logger.info(f"   From: {self.source_address[:6]}...{self.source_address[-4:]}")
        logger.info(f"   To: {self.target_address[:6]}...{self.target_address[-4:]}")
        logger.info(f"   Token: {self.token_address[:6]}...{self.token_address[-4:]}")