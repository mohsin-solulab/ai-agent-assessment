"""
Logger configuration module for autonomous agents system.

This module provides a configured color logger instance for use
throughout the application.
"""

import colorlog
import logging

def setup_logger():
    """
    Set up and configure a colored logger with custom formatting.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s [%(levelname)s] %(purple)s%(name)s%(reset)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'ERROR': 'red',
                'INFO': 'green',
                'WARNING': 'yellow',
                'DEBUG': 'cyan'
            }
        },
        style='%'
    ))
    
    logger = colorlog.getLogger('autonomous_agent')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

# Create global logger instance
logger = setup_logger()