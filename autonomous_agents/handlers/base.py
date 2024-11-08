"""
Base message handler definition for autonomous agents.

This module provides the abstract base class for implementing
message handlers.
"""

from abc import ABC, abstractmethod
from typing import List
from ..core.message import Message, MessageType

class MessageHandler(ABC):
    """Abstract base class for message handlers."""
    
    @abstractmethod
    def supported_message_types(self) -> List[MessageType]:
        """
        Get the message types supported by this handler.
        
        Returns:
            List[MessageType]: List of supported message types
        """
        pass

    @abstractmethod
    async def can_handle(self, message: Message) -> bool:
        """
        Check if this handler can process the given message.
        
        Args:
            message (Message): Message to check

        Returns:
            bool: True if the handler can process the message, False otherwise
        """
        pass

    @abstractmethod
    async def handle(self, message: Message, agent: 'AutonomousAgent') -> None:
        """
        Process the given message.
        
        Args:
            message (Message): Message to process
            agent (AutonomousAgent): Agent processing the message
        """
        pass