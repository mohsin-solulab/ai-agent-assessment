"""
Core autonomous agent implementation.

This module provides the main AutonomousAgent class that coordinates
behaviors and message handling.
"""

import asyncio
from ..utils.logger import logger
from ..core.message import Message, MessageBox
from ..core.registry import HandlerRegistry, BehaviorRegistry
from ..handlers.base import MessageHandler
from ..behaviors.base import Behavior

class AutonomousAgent:
    """
    Implementation of an autonomous agent that can process messages
    and execute behaviors.
    """
    
    def __init__(self, name: str):
        """
        Initialize a new autonomous agent.
        
        Args:
            name (str): Name of the agent
        """
        self.name = name
        self.inbox = MessageBox()
        self.outbox = MessageBox()
        self.handler_registry = HandlerRegistry()
        self.behavior_registry = BehaviorRegistry()
        self.running = False
        logger.info(f"🤖 Agent {self.name} initialized")

    def register_handler(self, handler: MessageHandler) -> None:
        """
        Register a message handler with the agent.
        
        Args:
            handler (MessageHandler): Handler to register
        """
        self.handler_registry.register_handler(handler)

    def register_behavior(self, behavior: Behavior) -> None:
        """
        Register a behavior with the agent.
        
        Args:
            behavior (Behavior): Behavior to register
        """
        self.behavior_registry.register_behavior(behavior)

    async def process_message(self, message: Message) -> None:
        """
        Process a received message.
        
        Args:
            message (Message): Message to process
        """
        await self.handler_registry.process_message(message, self)

    async def run_behaviors(self) -> None:
        """Execute all registered behaviors."""
        await self.behavior_registry.run_behaviors(self)

    async def run(self) -> None:
        """Start the agent's main processing loop."""
        self.running = True
        logger.info(f"▶️ Agent {self.name} started")
        
        while self.running:
            message = await self.inbox.get()
            if message:
                await self.process_message(message)
            await self.run_behaviors()
            await asyncio.sleep(0.1)

    def stop(self) -> None:
        """Stop the agent's processing loop."""
        self.running = False
        logger.info(f"⏹️ Agent {self.name} stopped")