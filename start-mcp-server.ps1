# PowerShell startup script for 123erfasst MCP Server

Write-Host "🚀 Starting 123erfasst MCP Server for Cursor/VS Code" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Set environment variables
$env:ERFASST_API_USERNAME = "philip.knoll@nevaris.com"
$env:ERFASST_API_TOKEN = "your_password_here"

Write-Host "👤 Username: $env:ERFASST_API_USERNAME" -ForegroundColor Cyan
Write-Host "🔑 Password: [HIDDEN]" -ForegroundColor Cyan
Write-Host ""

# Start the MCP server
Write-Host "🌐 Starting MCP server..." -ForegroundColor Yellow
uv run python server.py
