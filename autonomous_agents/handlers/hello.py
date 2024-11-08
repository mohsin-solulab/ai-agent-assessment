"""
Hello message handler implementation.

This module provides a handler that responds to messages
containing the word "hello".
"""

from typing import List
from ..handlers.base import MessageHandler
from ..core.message import Message, MessageType
from ..utils.logger import logger

class HelloMessageHandler(MessageHandler):
    """Handler for processing hello messages."""
    
    def supported_message_types(self) -> List[MessageType]:
        """
        Get supported message types.
        
        Returns:
            List[MessageType]: List containing TEXT message type
        """
        return [MessageType.TEXT]

    async def can_handle(self, message: Message) -> bool:
        """
        Check if message contains "hello".
        
        Args:
            message (Message): Message to check

        Returns:
            bool: True if message contains "hello", False otherwise
        """
        return (
            isinstance(message.content, str) and
            "hello" in message.content.lower()
        )

    async def handle(self, message: Message, agent: 'AutonomousAgent') -> None:
        """
        Process hello message.
        
        Args:
            message (Message): Message to process
            agent (AutonomousAgent): Agent processing the message
        """
        logger.info(f"👋 Hello message received by {agent.name}: '{message.content}'")