# 123erfasst MCP Server

A Model Context Protocol (MCP) server for integrating with the 123erfasst construction management system. This server provides natural language access to 123erfasst data through Claude Desktop and other MCP-compatible clients.

## Features

- **Project Management**: List, search, and manage construction projects
- **Staff Management**: Access staff information and assignments
- **Equipment Tracking**: Monitor equipment status and assignments
- **Time Tracking**: Start, stop, and query time tracking records
- **GraphQL Integration**: Direct integration with 123erfasst GraphQL API
- **MCP Compliance**: Follows MCP best practices for reliable operation

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Valid 123erfasst API credentials
- Claude Desktop or other MCP-compatible client

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/123erfasst-mcp-server.git
   cd 123erfasst-mcp-server
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up credentials**:
   ```bash
   python quick-setup.py
   ```
   
   Or manually set environment variables:
   ```bash
   export ERFASST_API_USERNAME="your_username"
   export ERFASST_API_TOKEN="your_password"
   ```

## Usage

### With Claude Desktop

1. **Configure Claude Desktop**:
   - Open Claude Desktop settings
   - Add the MCP server configuration from `cursor-mcp-config.json`
   - Restart Claude Desktop

2. **Test the integration**:
   - Open Claude Desktop
   - Try commands like:
     - "List all my projects"
     - "Show me staff members"
     - "Get equipment statistics"

### With VS Code

1. **Install MCP extension** (if available)
2. **Configure MCP server** using `vscode-mcp-config.json`
3. **Restart VS Code**

### Command Line Testing

Test the MCP server directly:
```bash
uv run python test-mcp-tools.py
```

## Available Tools

### Project Management (6 tools)
- `list_projects` - List all projects with optional filters
- `get_project_details` - Get detailed project information
- `search_projects` - Search projects by name or description
- `get_project_statistics` - Get project metrics and statistics
- `get_active_projects` - List currently active projects
- `get_projects_by_date_range` - Filter projects by date range

### Staff Management (7 tools)
- `list_staff` - List all staff members
- `get_person_details` - Get detailed person information
- `search_staff` - Search staff by name or role
- `get_staff_by_role` - Filter staff by role
- `get_active_staff` - List active staff members
- `get_staff_by_project` - Get staff assigned to a project
- `get_staff_statistics` - Get staff metrics and statistics

### Equipment Management (8 tools)
- `list_equipment` - List all equipment
- `get_equipment_details` - Get detailed equipment information
- `search_equipment` - Search equipment by name or type
- `get_equipment_by_status` - Filter equipment by status
- `get_equipment_by_location` - Filter equipment by location
- `get_equipment_by_project` - Get equipment assigned to a project
- `get_equipment_statistics` - Get equipment metrics
- `get_equipment_maintenance` - Get maintenance schedules

### Time Tracking (5 tools)
- `start_time_tracking` - Start time tracking for a project
- `stop_time_tracking` - Stop current time tracking
- `get_current_times` - Get active time tracking records
- `get_time_tracking_history` - Get historical time records
- `get_time_statistics` - Get time tracking statistics

## Configuration

### Environment Variables

- `ERFASST_API_USERNAME` - Your 123erfasst username
- `ERFASST_API_TOKEN` - Your 123erfasst password/token
- `LOG_LEVEL` - Logging level (default: INFO)

### MCP Server Configuration

The server uses Basic Authentication with the 123erfasst GraphQL API:
- **Endpoint**: `https://server.123erfasst.de/api/graphql`
- **Authentication**: Basic Auth (username:password)
- **Transport**: STDIO (for MCP clients)

## Development

### Project Structure

```
123erfasst-mcp-server/
├── libraries/                 # Core libraries
│   ├── graphql_client/       # GraphQL API client
│   ├── models/               # Pydantic data models
│   ├── project_management/   # Project management tools
│   ├── staff_management/     # Staff management tools
│   ├── equipment_management/ # Equipment management tools
│   └── time_tracking/        # Time tracking tools
├── tests/                    # Test suite
├── server.py                 # Main MCP server
├── start-server.py          # Server startup script
└── pyproject.toml           # Project configuration
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=libraries

# Run specific test categories
uv run pytest -m unit
uv run pytest -m integration
```

### Code Quality

```bash
# Format code
uv run black .

# Sort imports
uv run isort .

# Type checking
uv run mypy libraries/

# Linting
uv run ruff check .
```

## API Reference

### GraphQL Schema

The server integrates with the 123erfasst GraphQL API. Key query types:

- `projects` - Project collection with nodes and totalCount
- `persons` - Person collection with staff information
- `equipments` - Equipment collection with status and assignments
- `times` - Time tracking records with person and project references

### Data Models

All data is validated using Pydantic models:
- `Project` - Project information and metadata
- `Person` - Staff member information
- `Equipment` - Equipment details and status
- `StaffTime` - Time tracking records
- `Ticket` - Support tickets and issues
- `Planning` - Project planning and milestones

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify your credentials are correct
   - Check that environment variables are set
   - Ensure your 123erfasst account is active

2. **Connection Issues**:
   - Verify network connectivity to `server.123erfasst.de`
   - Check if the 123erfasst API is accessible
   - Review firewall settings

3. **MCP Integration Issues**:
   - Ensure Claude Desktop is updated to the latest version
   - Check MCP configuration file syntax
   - Restart Claude Desktop after configuration changes

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
uv run python test-mcp-tools.py
```

### Log Files

Check log files for detailed error information:
- Application logs: `logs/app.log`
- Error logs: `logs/error.log`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the 123erfasst API documentation

## Changelog

### v1.0.0
- Initial release
- Complete MCP server implementation
- Support for all major 123erfasst entities
- Claude Desktop integration
- Comprehensive test suite