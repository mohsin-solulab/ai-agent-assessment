import time
import json
from web3 import Web3
from ..behaviors.base import Behavior
from ..config import ERC20_ABI
from ..utils.logger import logger

class TokenBalanceCheckBehavior(Behavior):
    """Behavior that monitors token balances."""
    
    def __init__(
        self,
        web3: Web3,
        token_address: str,
        wallet_address: str,
        interval: float = 10.0
    ):
        """
        Initialize the behavior.
        
        Args:
            web3 (Web3): Web3 instance
            token_address (str): Address of the token contract
            wallet_address (str): Address to monitor
            interval (float): Check interval in seconds
        """
        self.web3 = web3
        self.token_contract = self.web3.eth.contract(
            address=self.web3.to_checksum_address(token_address),
            abi=json.loads(ERC20_ABI)
        )
        self.wallet_address = self.web3.to_checksum_address(wallet_address)
        self.interval = interval
        self.last_execution = 0
        
        # Get token decimals
        self.decimals = self.token_contract.functions.decimals().call()

    async def should_act(self) -> bool:
        """
        Check if enough time has passed since last check.
        
        Returns:
            bool: True if enough time has passed, False otherwise
        """
        return time.time() - self.last_execution >= self.interval

    async def act(self, agent: 'AutonomousAgent') -> None:
        """
        Check and log the current token balance.
        
        Args:
            agent (AutonomousAgent): Agent executing the behavior
        """
        try:
            balance = self.token_contract.functions.balanceOf(self.wallet_address).call()
            # Convert balance to decimal representation
            decimal_balance = balance / (10 ** self.decimals)
            
            logger.info(f"💰 Token balance for {self.wallet_address[:6]}...{self.wallet_address[-4:]}: {decimal_balance} tokens")
            self.last_execution = time.time()
            
        except Exception as e:
            logger.error(f"❌ Failed to check balance: {str(e)}")