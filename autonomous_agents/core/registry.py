"""
Registry implementation for handlers and behaviors.

This module provides registry classes for managing message handlers
and agent behaviors in the system.
"""

from typing import Dict, List
from ..core.message import Message, MessageType
from ..behaviors.base import Behavior
from ..handlers.base import MessageHandler

class HandlerRegistry:
    """Registry for message handlers in the system."""
    
    def __init__(self) -> None:
        """Initialize empty handler registry."""
        self.handlers: Dict[MessageType, List[MessageHandler]] = {
            MessageType.TEXT: [],
            MessageType.TRANSACTION: [],
            MessageType.BALANCE_CHECK: [],
        }

    def register_handler(self, handler: MessageHandler) -> None:
        """
        Register a new message handler.
        
        Args:
            handler (MessageHandler): Handler instance to register
        """
        for message_type in handler.supported_message_types():
            self.handlers[message_type].append(handler)

    async def process_message(self, message: Message, agent: 'AutonomousAgent') -> None:
        """
        Process a message using registered handlers.
        
        Args:
            message (Message): Message to process
            agent (AutonomousAgent): Agent processing the message
        """
        for handler in self.handlers[message.type]:
            if await handler.can_handle(message):
                await handler.handle(message, agent)

class BehaviorRegistry:
    """Registry for agent behaviors in the system."""
    
    def __init__(self) -> None:
        """Initialize empty behavior registry."""
        self.behaviors: List[Behavior] = []

    def register_behavior(self, behavior: Behavior) -> None:
        """
        Register a new behavior.
        
        Args:
            behavior (Behavior): Behavior instance to register
        """
        self.behaviors.append(behavior)

    async def run_behaviors(self, agent: 'AutonomousAgent') -> None:
        """
        Execute all registered behaviors.
        
        Args:
            agent (AutonomousAgent): Agent running the behaviors
        """
        for behavior in self.behaviors:
            if await behavior.should_act():
                await behavior.act(agent)