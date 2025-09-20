#!/usr/bin/env python3
"""
Setup script for 123erfasst MCP Server.
This script helps users get started quickly.
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are met."""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        return False
    
    # Check if uv is installed
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("✅ uv package manager found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv package manager not found")
        print("   Install it from: https://docs.astral.sh/uv/getting-started/installation/")
        return False
    
    print("✅ All requirements met")
    return True

def install_dependencies():
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_credentials():
    """Help user set up credentials."""
    print("\n🔐 Setting up credentials...")
    print("You can either:")
    print("1. Run 'python quick-setup.py' for interactive setup")
    print("2. Set environment variables manually:")
    print("   export ERFASST_API_USERNAME='your_username'")
    print("   export ERFASST_API_TOKEN='your_password'")
    
    choice = input("\nWould you like to run interactive setup now? (y/n): ").strip().lower()
    if choice == 'y':
        try:
            subprocess.run([sys.executable, "quick-setup.py"], check=True)
            print("✅ Credentials configured")
            return True
        except subprocess.CalledProcessError:
            print("❌ Setup failed, please configure manually")
            return False
    else:
        print("ℹ️  Please configure credentials before using the MCP server")
        return True

def test_installation():
    """Test the installation."""
    print("\n🧪 Testing installation...")
    try:
        subprocess.run([sys.executable, "test-mcp-tools.py"], check=True)
        print("✅ Installation test passed")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Installation test failed - this might be due to missing credentials")
        print("   Please configure your credentials and try again")
        return False

def main():
    """Main setup function."""
    print("🚀 123erfasst MCP Server Setup")
    print("=" * 40)
    
    if not check_requirements():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not setup_credentials():
        sys.exit(1)
    
    test_installation()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Configure your MCP client (Claude Desktop, VS Code, etc.)")
    print("2. Use the configuration files in this directory")
    print("3. Start using the MCP server!")

if __name__ == "__main__":
    main()
