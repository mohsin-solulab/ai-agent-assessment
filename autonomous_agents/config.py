"""
Configuration management module for autonomous agents system.

This module handles loading environment variables and providing
configuration values to the rest of the application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Web3 Configuration
WEB3_PROVIDER_URL = os.getenv('WEB3_PROVIDER_URL')

# Token Configuration
TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS')
TARGET_ADDRESS = os.getenv('TARGET_ADDRESS')

# Wallet Configuration
WALLET1_ADDRESS = os.getenv('WALLET1_ADDRESS')
WALLET2_ADDRESS = os.getenv('WALLET2_ADDRESS')
PRIVATE_KEY1 = os.getenv('PRIVATE_KEY1')
PRIVATE_KEY2 = os.getenv('PRIVATE_KEY2')

# Message Generation Configuration
WORDS = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]

# Token ABI
ERC20_ABI = '''[
    {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}
]'''

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
