"""
Main application entry point for autonomous agents system.
This module initializes and runs the autonomous agents system with
configured behaviors and handlers.
"""
import asyncio
import signal
from web3 import Web3
from .core.agent import AutonomousAgent
from .behaviors.random_message import RandomMessageBehavior
from .behaviors.token_balance import TokenBalanceCheckBehavior
from .handlers.hello import HelloMessageHandler
from .handlers.crypto import CryptoTransferHandler
from .utils.logger import logger
from . import config

class AgentSystem:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(config.WEB3_PROVIDER_URL))
        self.agent1 = None
        self.agent2 = None
        self.shutdown_event = asyncio.Event()
        self.tasks = []

    async def setup_agents(self):
        """Initialize and configure the agents."""
        # Create agents
        self.agent1 = AutonomousAgent("Agent1")
        self.agent2 = AutonomousAgent("Agent2")
        
        # Connect agents
        self.agent1.outbox = self.agent2.inbox
        self.agent2.outbox = self.agent1.inbox
        
        # Configure agent1
        self.agent1.register_behavior(RandomMessageBehavior())
        self.agent1.register_behavior(TokenBalanceCheckBehavior(
            self.web3, config.TOKEN_ADDRESS, config.WALLET1_ADDRESS
        ))
        self.agent1.register_handler(HelloMessageHandler())
        self.agent1.register_handler(CryptoTransferHandler(
            self.web3,
            config.TOKEN_ADDRESS,
            config.WALLET1_ADDRESS,
            config.TARGET_ADDRESS,
            config.PRIVATE_KEY1,
            "Agent1"  # Add agent name here
        ))
        
        # Configure agent2
        self.agent2.register_behavior(RandomMessageBehavior())
        self.agent2.register_behavior(TokenBalanceCheckBehavior(
            self.web3, config.TOKEN_ADDRESS, config.WALLET2_ADDRESS
        ))
        self.agent2.register_handler(HelloMessageHandler())
        self.agent2.register_handler(CryptoTransferHandler(
            self.web3,
            config.TOKEN_ADDRESS,
            config.WALLET2_ADDRESS,
            config.TARGET_ADDRESS,
            config.PRIVATE_KEY2,
            "Agent2"  # Add agent name here
        ))

    async def shutdown(self):
        """Gracefully shutdown the agent system."""
        logger.info("👋 Initiating graceful shutdown...")
        
        # Signal the shutdown event
        self.shutdown_event.set()
        
        # Stop the agents
        if self.agent1:
            self.agent1.stop()
        if self.agent2:
            self.agent2.stop()
        
        # Wait for all tasks to complete with timeout
        if self.tasks:
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self.tasks, return_exceptions=True),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                logger.warning("⚠️ Some tasks did not complete within timeout")
        
        logger.info("✨ System shutdown complete")

    async def run_agent(self, agent):
        """Run an agent until shutdown is requested."""
        try:
            await agent.run()
        except Exception as e:
            logger.error(f"❌ Agent error: {str(e)}")
        finally:
            agent.stop()

    async def main(self):
        """Initialize and run the autonomous agents system."""
        try:
            await self.setup_agents()
            
            # Setup signal handlers for graceful shutdown
            for sig in (signal.SIGTERM, signal.SIGINT):
                asyncio.get_running_loop().add_signal_handler(
                    sig,
                    lambda: asyncio.create_task(self.shutdown())
                )
            
            logger.info("🚀 Starting autonomous agents system")
            
            # Create and store agent tasks
            self.tasks = [
                asyncio.create_task(self.run_agent(self.agent1)),
                asyncio.create_task(self.run_agent(self.agent2))
            ]
            
            # Wait for shutdown event
            await self.shutdown_event.wait()
            
        except Exception as e:
            logger.error(f"❌ System error: {str(e)}")
            await self.shutdown()

if __name__ == "__main__":
    system = AgentSystem()
    asyncio.run(system.main())