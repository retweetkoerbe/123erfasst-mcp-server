"""
Configuration module for 123erfasst MCP Server.
"""
import os
import sys
import logging
from pathlib import Path
from typing import Optional

# 123erfasst API Configuration
API_BASE_URL = "https://server.123erfasst.de/api/graphql"
API_TOKEN = os.getenv("ERFASST_API_TOKEN")
API_USERNAME = os.getenv("ERFASST_API_USERNAME", "api")  # Default username for 123erfasst API

# MCP Server Configuration
SERVER_NAME = "123erfasst"
SERVER_VERSION = "1.0.0"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Project paths
PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs"

def setup_logging() -> None:
    """
    Set up centralized logging configuration.
    Follows Article V.2: Error Response - All errors must be logged with appropriate context.
    """
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=LOG_FORMAT,
        handlers=[
            # File handler for all logs
            logging.FileHandler(LOGS_DIR / "app.log"),
            # File handler for errors only
            logging.FileHandler(LOGS_DIR / "error.log"),
            # Console handler for stderr (not stdout for MCP servers)
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("gql").setLevel(logging.WARNING)
    
    # Log startup
    logger = logging.getLogger(__name__)
    logger.info(f"Starting {SERVER_NAME} MCP Server v{SERVER_VERSION}")

def get_api_token() -> str:
    """
    Get API token from environment variables.
    Follows Article VI.1: Credential Management - Secure storage of authentication credentials.
    """
    if not API_TOKEN:
        raise ValueError(
            "ERFASST_API_TOKEN environment variable is required. "
            "Please set it with your 123erfasst API token."
        )
    return API_TOKEN

def get_api_username() -> str:
    """
    Get API username from environment variables.
    Follows Article VI.1: Credential Management - Secure storage of authentication credentials.
    """
    return API_USERNAME

def validate_configuration() -> None:
    """
    Validate that all required configuration is present.
    """
    try:
        get_api_token()
        logging.getLogger(__name__).info("Configuration validation passed")
    except ValueError as e:
        logging.getLogger(__name__).error(f"Configuration validation failed: {e}")
        raise

# Initialize logging when module is imported
setup_logging()

