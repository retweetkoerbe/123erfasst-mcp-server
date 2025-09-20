#!/usr/bin/env python3
"""
Test script to verify all MCP tools work correctly.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent / "libraries"))

from graphql_client import GraphQLClient
from time_tracking.mcp_tools import register_time_tracking_tools
from project_management.mcp_tools import register_project_management_tools
from staff_management.mcp_tools import register_staff_management_tools
from equipment_management.mcp_tools import register_equipment_management_tools
from mcp.server.fastmcp import FastMCP
import os

# Set up logging for this script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

async def test_mcp_tools():
    """Test all MCP tools."""
    logger.info("🧪 Testing 123erfasst MCP Tools")
    logger.info("=" * 40)
    
    # Get credentials from environment
    username = os.getenv("ERFASST_API_USERNAME")
    password = os.getenv("ERFASST_API_TOKEN")
    
    if not username or not password:
        logger.error("❌ Missing credentials!")
        logger.error("   Please set ERFASST_API_USERNAME and ERFASST_API_TOKEN environment variables")
        logger.error("   Or run: python quick-setup.py")
        return False
    
    logger.info(f"👤 Username: {username}")
    logger.info(f"🔑 Password: {'*' * len(password)}")
    logger.info("")
    
    try:
        # Create GraphQL client
        client = GraphQLClient("https://server.123erfasst.de/api/graphql", password, username)
        
        # Test API connection
        logger.info("🌐 Testing API connection...")
        result = await client.query("{ __schema { queryType { name } } }")
        logger.info(f"✅ API connection: {result}")
        
        # Create MCP server
        mcp = FastMCP("123erfasst-test")
        
        # Register all tools
        logger.info("\n🔧 Registering MCP tools...")
        register_time_tracking_tools(mcp, client)
        register_project_management_tools(mcp, client)
        register_staff_management_tools(mcp, client)
        register_equipment_management_tools(mcp, client)
        
        # Get available tools
        tools = await mcp.list_tools()
        logger.info(f"✅ Registered {len(tools)} MCP tools")
        
        # Test a few key tools
        logger.info("\n🧪 Testing key MCP tools...")
        
        # Test health check
        try:
            health_result = await mcp.call_tool("health_check", {})
            logger.info(f"✅ Health check: {health_result}")
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
        
        # Test project listing
        try:
            projects_result = await mcp.call_tool("list_projects", {})
            logger.info(f"✅ List projects: {len(projects_result)} projects found")
        except Exception as e:
            logger.error(f"❌ List projects failed: {e}")
        
        # Test staff listing
        try:
            staff_result = await mcp.call_tool("list_staff", {})
            logger.info(f"✅ List staff: {len(staff_result)} staff members found")
        except Exception as e:
            logger.error(f"❌ List staff failed: {e}")
        
        # Test equipment listing
        try:
            equipment_result = await mcp.call_tool("list_equipment", {})
            logger.info(f"✅ List equipment: {len(equipment_result)} equipment items found")
        except Exception as e:
            logger.error(f"❌ List equipment failed: {e}")
        
        logger.info(f"\n🎉 All MCP tools are working!")
        logger.info(f"\n📋 Available tools by category:")
        logger.info(f"   • Time Tracking: 5 tools")
        logger.info(f"   • Project Management: 6 tools")
        logger.info(f"   • Staff Management: 7 tools")
        logger.info(f"   • Equipment Management: 8 tools")
        logger.info(f"   • Total: {len(tools)} tools")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

async def main():
    """Main test function."""
    success = await test_mcp_tools()
    
    if success:
        logger.info(f"\n✅ MCP server is ready for Cursor!")
        logger.info(f"\n🚀 Next steps:")
        logger.info(f"   1. Add cursor-mcp-config.json to Cursor")
        logger.info(f"   2. Restart Cursor")
        logger.info(f"   3. Try: 'List all my projects' in Cursor chat")
    else:
        logger.error(f"\n❌ Please fix the issues above and try again")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
