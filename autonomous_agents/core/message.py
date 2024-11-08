"""
Core message types and handling for autonomous agents system.

This module defines the message types and message box implementation
used for agent communication.
"""

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, List

class MessageType(Enum):
    """Enumeration of supported message types in the system."""
    TEXT = "text"
    TRANSACTION = "transaction"
    BALANCE_CHECK = "balance_check"

@dataclass
class Message:
    """
    Data class representing a message in the system.
    
    Attributes:
        type (MessageType): Type of the message
        content (Any): Content of the message
        timestamp (float): Unix timestamp when the message was created
    """
    type: MessageType
    content: Any
    timestamp: float = field(default_factory=time.time)

class MessageBox:
    """
    Thread-safe message queue implementation for agent communication.
    
    This class provides a simple message queue with async support
    for safe message passing between agents.
    """
    def __init__(self) -> None:
        """Initialize an empty message box with a lock."""
        self.messages: List[Message] = []
        self._lock = asyncio.Lock()

    async def put(self, message: Message) -> None:
        """
        Add a message to the message box.
        
        Args:
            message (Message): Message to add to the queue
        """
        async with self._lock:
            self.messages.append(message)

    async def get(self) -> Optional[Message]:
        """
        Retrieve and remove the next message from the message box.
        
        Returns:
            Optional[Message]: Next message in the queue, or None if empty
        """
        async with self._lock:
            if self.messages:
                message = self.messages.pop(0)
                return message
            return None