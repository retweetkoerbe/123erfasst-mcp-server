"""
CLI interface for time tracking operations.

Follows Article II: CLI Interface Mandate - All functionality accessible through CLI.
"""
import asyncio
import json
import logging
import sys
import argparse
from .time_tracker import TimeTracker
from .exceptions import TimeTrackingError, TimeTrackingActiveError, TimeTrackingNotActiveError

# Set up logger for CLI
logger = logging.getLogger(__name__)


async def start_tracking(base_url: str, token: str, project_id: str, person_id: str, description: str = None) -> None:
    """Start time tracking."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        tracker = TimeTracker(client)
        
        result = await tracker.start_time_tracking(project_id, person_id, description)
        logger.info(f"✅ Time tracking started:")
        logger.info(f"   ID: {result['id']}")
        logger.info(f"   Project: {result['projectId']}")
        logger.info(f"   Person: {result['personId']}")
        logger.info(f"   Start Time: {result['startTime']}")
        
    except TimeTrackingActiveError as e:
        logger.info(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        logger.info(f"❌ Failed to start time tracking: {e}")
        sys.exit(1)


async def stop_tracking(base_url: str, token: str) -> None:
    """Stop time tracking."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        tracker = TimeTracker(client)
        
        result = await tracker.stop_time_tracking()
        logger.info(f"✅ Time tracking stopped:")
        logger.info(f"   ID: {result['id']}")
        logger.info(f"   End Time: {result['endTime']}")
        logger.info(f"   Duration: {result['durationHours']} hours")
        
    except TimeTrackingNotActiveError as e:
        logger.info(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        logger.info(f"❌ Failed to stop time tracking: {e}")
        sys.exit(1)


async def get_current_times(base_url: str, token: str, project_id: str = None, person_id: str = None) -> None:
    """Get current time tracking records."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        tracker = TimeTracker(client)
        
        result = await tracker.get_current_times(project_id, person_id)
        
        if not result:
            logger.info(f"No active time tracking records found.")
            return
        
        logger.info(f"Active time tracking records ({len(result)}):")
        for record in result:
            logger.info(f"  ID: {record['id']}")
            logger.info(f"  Project: {record['projectId']}")
            logger.info(f"  Person: {record['personId']}")
            logger.info(f"  Start Time: {record['startTime']}")
            logger.info(f"  Description: {record.get('description', 'N/A')}")
            logger.info(f"  ---")
        
    except Exception as e:
        logger.info(f"❌ Failed to get current times: {e}")
        sys.exit(1)


async def get_history(base_url: str, token: str, project_id: str = None, person_id: str = None, 
                     start_date: str = None, end_date: str = None) -> None:
    """Get time tracking history."""
    try:
        from ..graphql_client import GraphQLClient
        client = GraphQLClient(base_url, token)
        tracker = TimeTracker(client)
        
        result = await tracker.get_time_tracking_history(project_id, person_id, start_date, end_date)
        
        if not result:
            logger.info(f"No time tracking records found.")
            return
        
        logger.info(f"Time tracking history ({len(result)} records):")
        for record in result:
            logger.info(f"  ID: {record['id']}")
            logger.info(f"  Project: {record['projectId']}")
            logger.info(f"  Person: {record['personId']}")
            logger.info(f"  Start: {record['startTime']}")
            logger.info(f"  End: {record.get('endTime', 'N/A')}")
            logger.info(f"  Duration: {record.get('durationHours', 'N/A')} hours")
            logger.info(f"  Active: {record['isActive']}")
            logger.info(f"  ---")
        
    except Exception as e:
        logger.info(f"❌ Failed to get time tracking history: {e}")
        sys.exit(1)


async def status(base_url: str, token: str) -> None:
    """Check time tracking status."""
    try:
        from ..graphql_client import GraphQLClient
import logging

# Set up logger for CLI
logger = logging.getLogger(__name__)
        client = GraphQLClient(base_url, token)
        tracker = TimeTracker(client)
        
        is_active = tracker.is_tracking_active()
        active_id = tracker.get_active_tracking_id()
        
        if is_active:
            logger.info(f"✅ Time tracking is active (ID: {active_id})")
        else:
            logger.info(f"⏸️  No active time tracking")
        
    except Exception as e:
        logger.info(f"❌ Failed to check status: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Time Tracking CLI")
    parser.add_argument("--base-url", required=True, help="GraphQL API base URL")
    parser.add_argument("--token", required=True, help="API authentication token")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Start tracking command
    start_parser = subparsers.add_parser("start", help="Start time tracking")
    start_parser.add_argument("--project-id", required=True, help="Project ID")
    start_parser.add_argument("--person-id", required=True, help="Person ID")
    start_parser.add_argument("--description", help="Work description")
    
    # Stop tracking command
    subparsers.add_parser("stop", help="Stop time tracking")
    
    # Get current times command
    current_parser = subparsers.add_parser("current", help="Get current time tracking records")
    current_parser.add_argument("--project-id", help="Filter by project ID")
    current_parser.add_argument("--person-id", help="Filter by person ID")
    
    # Get history command
    history_parser = subparsers.add_parser("history", help="Get time tracking history")
    history_parser.add_argument("--project-id", help="Filter by project ID")
    history_parser.add_argument("--person-id", help="Filter by person ID")
    history_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    history_parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    
    # Status command
    subparsers.add_parser("status", help="Check time tracking status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "start":
        asyncio.run(start_tracking(args.base_url, args.token, args.project_id, args.person_id, args.description))
    elif args.command == "stop":
        asyncio.run(stop_tracking(args.base_url, args.token))
    elif args.command == "current":
        asyncio.run(get_current_times(args.base_url, args.token, args.project_id, args.person_id))
    elif args.command == "history":
        asyncio.run(get_history(args.base_url, args.token, args.project_id, args.person_id, args.start_date, args.end_date))
    elif args.command == "status":
        asyncio.run(status(args.base_url, args.token))


if __name__ == "__main__":
    main()
