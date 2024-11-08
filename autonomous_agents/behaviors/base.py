"""
Base behavior definition for autonomous agents.

This module provides the abstract base class for implementing
agent behaviors.
"""

from abc import ABC, abstractmethod

class Behavior(ABC):
    """Abstract base class for agent behaviors."""
    
    @abstractmethod
    async def should_act(self) -> bool:
        """
        Determine if the behavior should execute.
        
        Returns:
            bool: True if the behavior should execute, False otherwise
        """
        pass

    @abstractmethod
    async def act(self, agent: 'AutonomousAgent') -> None:
        """
        Execute the behavior.
        
        Args:
            agent (AutonomousAgent): Agent executing the behavior
        """
        pass