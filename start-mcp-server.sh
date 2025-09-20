#!/bin/bash
# Startup script for 123erfasst MCP Server

echo "🚀 Starting 123erfasst MCP Server for Cursor/VS Code"
echo "=================================================="

# Set environment variables
export ERFASST_API_USERNAME="philip.knoll@nevaris.com"
export ERFASST_API_TOKEN="your_password_here"

echo "👤 Username: $ERFASST_API_USERNAME"
echo "🔑 Password: [HIDDEN]"
echo ""

# Start the MCP server
echo "🌐 Starting MCP server..."
uv run python server.py
