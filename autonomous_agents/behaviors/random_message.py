"""
Random message generation behavior implementation.

This module provides a behavior that generates random messages
from a predefined word list.
"""

import random
import time
from ..behaviors.base import Behavior
from ..core.message import Message, MessageType
from ..config import WORDS
from ..utils.logger import logger

class RandomMessageBehavior(Behavior):
    """Behavior that generates random messages periodically."""
    
    def __init__(self, interval: float = 2.0):
        """
        Initialize the behavior.
        
        Args:
            interval (float): Minimum time between messages in seconds
        """
        self.interval = interval
        self.last_execution = 0

    async def should_act(self) -> bool:
        """
        Check if enough time has passed since last message.
        
        Returns:
            bool: True if enough time has passed, False otherwise
        """
        return time.time() - self.last_execution >= self.interval

    async def act(self, agent: 'AutonomousAgent') -> None:
        """
        Generate and send a random message.
        
        Args:
            agent (AutonomousAgent): Agent executing the behavior
        """
        words = random.sample(WORDS, 2)
        message = Message(
            type=MessageType.TEXT,
            content=" ".join(words)
        )
        await agent.outbox.put(message)
        self.last_execution = time.time()
        logger.info(f"🎲 Agent {agent.name} generated message: '{message.content}'")