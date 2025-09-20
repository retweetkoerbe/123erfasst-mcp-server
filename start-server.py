#!/usr/bin/env python3
"""
Startup script for 123erfasst MCP Server.
This script loads environment variables and starts the MCP server.
"""
import logging
import os
import sys
from pathlib import Path

# Set up logging for this script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        logger.info(f"📁 Loading environment from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        logger.info("✅ Environment variables loaded")
    else:
        logger.warning("⚠️  No .env file found, using system environment variables")

def check_credentials():
    """Check if credentials are properly set."""
    username = os.getenv("ERFASST_API_USERNAME")
    token = os.getenv("ERFASST_API_TOKEN")
    
    if not username:
        logger.error("❌ ERFASST_API_USERNAME not set")
        return False
    
    if not token or token == "YOUR_123ERFASST_API_TOKEN_HERE":
        logger.error("❌ ERFASST_API_TOKEN not set or is placeholder")
        return False
    
    logger.info(f"✅ Credentials found: {username}")
    return True

def main():
    """Main startup function."""
    logger.info("🚀 Starting 123erfasst MCP Server")
    logger.info("=" * 40)
    
    # Load environment variables
    load_env_file()
    
    # Check credentials
    if not check_credentials():
        logger.error("\n💡 To fix this:")
        logger.error("   1. Run: python setup-cursor.py")
        logger.error("   2. Or set environment variables manually:")
        logger.error("      export ERFASST_API_USERNAME='your_username'")
        logger.error("      export ERFASST_API_TOKEN='your_password'")
        return 1
    
    # Start the MCP server
    logger.info("\n🌐 Starting MCP server...")
    try:
        import server
        logger.info("✅ MCP server started successfully")
        return 0
    except Exception as e:
        logger.error(f"❌ Failed to start MCP server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
