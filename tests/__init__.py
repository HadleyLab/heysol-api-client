"""
Test configuration for HeySol API client tests.
"""

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    env_file = Path(__file__).parent.parent / ".env"
    load_dotenv(env_file)
    print(f"Loaded environment from: {env_file}")
except ImportError:
    print("python-dotenv not available, skipping .env file loading")
except Exception as e:
    print(f"Error loading .env file: {e}")
