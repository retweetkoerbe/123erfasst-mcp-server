#!/usr/bin/env python3
"""
Quick setup script for 123erfasst MCP Server.
Creates configuration files with your credentials.
"""
import os
import json
import sys
from pathlib import Path

def create_config_files():
    """Create configuration files for Cursor and VS Code."""
    print("🚀 Quick Setup for 123erfasst MCP Server")
    print("=" * 50)
    
    # Get credentials from user input
    username = input("Enter your 123erfasst username: ").strip()
    if not username:
        print("❌ Username is required!")
        return False
    
    password = os.getenv("ERFASST_API_TOKEN")
    if not password:
        import getpass
        password = getpass.getpass("Enter your 123erfasst password: ").strip()
        if not password:
            print("❌ Password is required!")
            return False
    
    print(f"👤 Username: {username}")
    print(f"🔑 Password: {'*' * len(password)}")
    print()
    
    # Create .env file
    env_file = Path(__file__).parent / ".env"
    with open(env_file, 'w') as f:
        f.write(f"ERFASST_API_USERNAME={username}\n")
        f.write(f"ERFASST_API_TOKEN={password}\n")
    print(f"✅ Created: {env_file}")
    
    # Create Cursor config
    cursor_config = {
        "mcpServers": {
            "123erfasst": {
                "command": "uv",
                "args": ["run", "python", "start-server.py"],
                "cwd": str(Path(__file__).parent.absolute())
            }
        }
    }
    
    cursor_file = Path(__file__).parent / "cursor-mcp-config.json"
    with open(cursor_file, 'w') as f:
        json.dump(cursor_config, f, indent=2)
    print(f"✅ Created: {cursor_file}")
    
    # Create VS Code config
    vscode_config = {
        "mcp.servers": {
            "123erfasst": {
                "command": "uv",
                "args": ["run", "python", "start-server.py"],
                "cwd": str(Path(__file__).parent.absolute())
            }
        }
    }
    
    vscode_file = Path(__file__).parent / "vscode-mcp-config.json"
    with open(vscode_file, 'w') as f:
        json.dump(vscode_config, f, indent=2)
    print(f"✅ Created: {vscode_file}")
    
    print(f"\n🎉 Setup complete!")
    print(f"\n📋 Next steps:")
    print(f"   1. Add cursor-mcp-config.json to Cursor")
    print(f"   2. Restart Cursor")
    print(f"   3. Test: 'List all my projects' in Cursor chat")
    
    return True

if __name__ == "__main__":
    success = create_config_files()
    sys.exit(0 if success else 1)
