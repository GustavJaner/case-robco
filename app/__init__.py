import os
from argparse import Namespace
from typing import Final

from dotenv import load_dotenv

load_dotenv()

class Config(Namespace):
    """Application configuration"""

    #BASIC_AUTH_USERNAME: Final[str] = os.getenv("BASIC_AUTH_USERNAME", "username")
    #BASIC_AUTH_PASSWORD: Final[str] = os.getenv("BASIC_AUTH_PASSWORD", "password")
    DEBUG_MODE: Final[bool] = os.getenv("DEBUG_MODE", "False").lower() == "true"
