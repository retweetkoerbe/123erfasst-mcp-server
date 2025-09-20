"""
123erfasst MCP Server

Main MCP server for integrating with 123erfasst construction management system.
Follows Article I: Library-First Principle - MCP tools are implemented using standalone libraries.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent / "libraries"))

from mcp.server.fastmcp import FastMCP
from graphql_client import GraphQLClient
from time_tracking.mcp_tools import register_time_tracking_tools
from project_management.mcp_tools import register_project_management_tools
from staff_management.mcp_tools import register_staff_management_tools
from equipment_management.mcp_tools import register_equipment_management_tools
import config

# Set up logging
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("123erfasst")

@mcp.tool()
async def health_check() -> str:
    """
    Health check endpoint for the MCP server.
    """
    return f"123erfasst MCP Server v{config.SERVER_VERSION} is running"

def setup_mcp_tools():
    """Set up all MCP tools with their dependencies."""
    try:
        # Initialize GraphQL client with Basic Authentication
        api_token = config.get_api_token()
        api_username = config.get_api_username()
        
        # Validate credentials before proceeding
        if not api_token or api_token == "YOUR_123ERFASST_API_TOKEN_HERE":
            raise ValueError("API token not configured. Please run setup-cursor.py first.")
        
        graphql_client = GraphQLClient(config.API_BASE_URL, api_token, api_username)
        
        # Register time tracking tools
        register_time_tracking_tools(mcp, graphql_client)
        
        # Register project management tools
        register_project_management_tools(mcp, graphql_client)
        
        # Register staff management tools
        register_staff_management_tools(mcp, graphql_client)
        
        # Register equipment management tools
        register_equipment_management_tools(mcp, graphql_client)
        
        # TODO: Register other tool groups as they are implemented
        # register_quality_management_tools(mcp, graphql_client)
        
        logger.info("✅ All MCP tools registered successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to set up MCP tools: {e}")
        raise

if __name__ == "__main__":
    # Validate configuration
    config.validate_configuration()
    
    # Set up MCP tools
    setup_mcp_tools()
    
    # Run MCP server
    mcp.run(transport='stdio')

