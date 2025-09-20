"""
CLI interface for project management operations.

Follows Article II: CLI Interface Mandate - All functionality accessible through CLI.
"""
import asyncio
import json
import logging
import sys
import argparse
from .project_manager import ProjectManager
from .exceptions import ProjectManagementError, ProjectNotFoundError, InvalidProjectDataError

# Set up logger for CLI
logger = logging.getLogger(__name__)


async def list_projects(base_url: str, token: str, status: str = None, limit: int = None) -> None:
    """List all projects."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        manager = ProjectManager(client)
        
        result = await manager.list_projects(status=status, limit=limit)
        
        if not result:
            logger.info(f"No projects found.")
            return
        
        logger.info(f"Projects ({len(result)}):")
        for project in result:
            logger.info(f"  ID: {project['id']}")
            logger.info(f"  Name: {project['name']}")
            logger.info(f"  Status: {project['status']}")
            logger.info(f"  Client: {project.get('clientName', 'N/A')}")
            logger.info(f"  Start: {project.get('startDate', 'N/A')}")
            logger.info(f"  End: {project.get('endDate', 'N/A')}")
            logger.info(f"  ---")
        
    except Exception as e:
        logger.info(f"❌ Failed to list projects: {e}")
        sys.exit(1)


async def get_project_details(base_url: str, token: str, project_id: str) -> None:
    """Get project details."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        manager = ProjectManager(client)
        
        result = await manager.get_project_details(project_id)
        
        logger.info(f"Project Details:")
        logger.info(f"  ID: {result['id']}")
        logger.info(f"  Name: {result['name']}")
        logger.info(f"  Status: {result['status']}")
        logger.info(f"  Description: {result.get('description', 'N/A')}")
        logger.info(f"  Client: {result.get('clientName', 'N/A')}")
        logger.info(f"  Budget: {result.get('budget', 'N/A')}")
        logger.info(f"  Location: {result.get('location', 'N/A')}")
        logger.info(f"  Start Date: {result.get('startDate', 'N/A')}")
        logger.info(f"  End Date: {result.get('endDate', 'N/A')}")
        
        if result.get('staff'):
            logger.info(f"  Staff ({len(result['staff'])}):")
            for person in result['staff']:
                logger.info(f"    - {person['name']} ({person['role']})")
        
        if result.get('equipment'):
            logger.info(f"  Equipment ({len(result['equipment'])}):")
            for equipment in result['equipment']:
                logger.info(f"    - {equipment['name']} ({equipment['type']}) - {equipment['status']}")
        
    except ProjectNotFoundError as e:
        logger.info(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        logger.info(f"❌ Failed to get project details: {e}")
        sys.exit(1)


async def search_projects(base_url: str, token: str, query: str, status: str = None, limit: int = None) -> None:
    """Search projects."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        manager = ProjectManager(client)
        
        result = await manager.search_projects(query, status=status, limit=limit)
        
        if not result:
            logger.info(f"No projects found matching '{query}'.")
            return
        
        logger.info(f"Search Results for '{query}' ({len(result)}):")
        for project in result:
            logger.info(f"  ID: {project['id']}")
            logger.info(f"  Name: {project['name']}")
            logger.info(f"  Status: {project['status']}")
            logger.info(f"  Client: {project.get('clientName', 'N/A')}")
            logger.info(f"  ---")
        
    except Exception as e:
        logger.info(f"❌ Failed to search projects: {e}")
        sys.exit(1)


async def get_project_stats(base_url: str, token: str) -> None:
    """Get project statistics."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        manager = ProjectManager(client)
        
        result = await manager.get_project_statistics()
        
        logger.info(f"Project Statistics:")
        logger.info(f"  Total Projects: {result.get('totalProjects', 0)}")
        logger.info(f"  Active Projects: {result.get('activeProjects', 0)}")
        logger.info(f"  Completed Projects: {result.get('completedProjects', 0)}")
        logger.info(f"  On Hold Projects: {result.get('onHoldProjects', 0)}")
        logger.info(f"  Cancelled Projects: {result.get('cancelledProjects', 0)}")
        logger.info(f"  Total Budget: ${result.get('totalBudget', 0):,.2f}")
        logger.info(f"  Average Duration: {result.get('averageProjectDuration', 0)} days")
        logger.info(f"  Average Budget: ${result.get('averageProjectBudget', 0):,.2f}")
        
    except Exception as e:
        logger.info(f"❌ Failed to get project statistics: {e}")
        sys.exit(1)


async def create_project(base_url: str, token: str, project_data: str) -> None:
    """Create a new project."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        manager = ProjectManager(client)
        
        # Parse project data from JSON
        data = json.loads(project_data)
        result = await manager.create_project(data)
        
        logger.info(f"✅ Project created successfully:")
        logger.info(f"  ID: {result['id']}")
        logger.info(f"  Name: {result['name']}")
        logger.info(f"  Status: {result['status']}")
        
    except InvalidProjectDataError as e:
        logger.info(f"❌ Invalid project data: {e}")
        sys.exit(1)
    except Exception as e:
        logger.info(f"❌ Failed to create project: {e}")
        sys.exit(1)


async def update_project(base_url: str, token: str, project_id: str, update_data: str) -> None:
    """Update a project."""
    try:
        from ..graphql_client import GraphQLClient
import logging

# Set up logger for CLI
logger = logging.getLogger(__name__)
        client = GraphQLClient(base_url, token)
        manager = ProjectManager(client)
        
        # Parse update data from JSON
        data = json.loads(update_data)
        result = await manager.update_project(project_id, data)
        
        logger.info(f"✅ Project updated successfully:")
        logger.info(f"  ID: {result['id']}")
        logger.info(f"  Name: {result['name']}")
        logger.info(f"  Status: {result['status']}")
        
    except ProjectNotFoundError as e:
        logger.info(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        logger.info(f"❌ Failed to update project: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Project Management CLI")
    parser.add_argument("--base-url", required=True, help="GraphQL API base URL")
    parser.add_argument("--token", required=True, help="API authentication token")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List projects command
    list_parser = subparsers.add_parser("list", help="List all projects")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--limit", type=int, help="Limit number of results")
    
    # Get project details command
    details_parser = subparsers.add_parser("details", help="Get project details")
    details_parser.add_argument("--project-id", required=True, help="Project ID")
    
    # Search projects command
    search_parser = subparsers.add_parser("search", help="Search projects")
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument("--status", help="Filter by status")
    search_parser.add_argument("--limit", type=int, help="Limit number of results")
    
    # Get statistics command
    subparsers.add_parser("stats", help="Get project statistics")
    
    # Create project command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("--data", required=True, help="Project data as JSON string")
    
    # Update project command
    update_parser = subparsers.add_parser("update", help="Update a project")
    update_parser.add_argument("--project-id", required=True, help="Project ID")
    update_parser.add_argument("--data", required=True, help="Update data as JSON string")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "list":
        asyncio.run(list_projects(args.base_url, args.token, args.status, args.limit))
    elif args.command == "details":
        asyncio.run(get_project_details(args.base_url, args.token, args.project_id))
    elif args.command == "search":
        asyncio.run(search_projects(args.base_url, args.token, args.query, args.status, args.limit))
    elif args.command == "stats":
        asyncio.run(get_project_stats(args.base_url, args.token))
    elif args.command == "create":
        asyncio.run(create_project(args.base_url, args.token, args.data))
    elif args.command == "update":
        asyncio.run(update_project(args.base_url, args.token, args.project_id, args.data))


if __name__ == "__main__":
    main()
