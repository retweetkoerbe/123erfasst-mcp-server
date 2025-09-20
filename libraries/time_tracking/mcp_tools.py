"""
MCP tools for time tracking functionality.

Follows Article I: Library-First Principle - MCP tools use standalone libraries.
"""
import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .time_tracker import TimeTracker
from .exceptions import TimeTrackingError, TimeTrackingActiveError, TimeTrackingNotActiveError

logger = logging.getLogger(__name__)


def register_time_tracking_tools(mcp: FastMCP, graphql_client) -> None:
    """
    Register time tracking MCP tools.
    
    Args:
        mcp: FastMCP server instance
        graphql_client: GraphQL client for API communication
    """
    
    @mcp.tool()
    async def start_time_tracking(
        project_id: str,
        person_id: str,
        description: Optional[str] = None
    ) -> str:
        """
        Start time tracking for a project and person.
        
        Args:
            project_id: Project identifier
            person_id: Person identifier  
            description: Optional work description
            
        Returns:
            Confirmation message with tracking details
        """
        try:
            tracker = TimeTracker(graphql_client)
            result = await tracker.start_time_tracking(project_id, person_id, description)
            
            return f"""✅ Time tracking started successfully!

📋 Details:
• Tracking ID: {result['id']}
• Project: {result['projectId']}
• Person: {result['personId']}
• Start Time: {result['startTime']}
• Description: {description or 'None'}

Time tracking is now active. Use 'stop_time_tracking' to end the session."""
            
        except TimeTrackingActiveError as e:
            return f"❌ Cannot start time tracking: {e}\n\nPlease stop the current time tracking session first using 'stop_time_tracking'."
            
        except TimeTrackingError as e:
            return f"❌ Failed to start time tracking: {e}"
    
    @mcp.tool()
    async def stop_time_tracking() -> str:
        """
        Stop the currently active time tracking session.
        
        Returns:
            Confirmation message with session summary
        """
        try:
            tracker = TimeTracker(graphql_client)
            result = await tracker.stop_time_tracking()
            
            return f"""✅ Time tracking stopped successfully!

📋 Session Summary:
• Tracking ID: {result['id']}
• End Time: {result['endTime']}
• Duration: {result['durationHours']} hours
• Status: Inactive

Time tracking session completed."""
            
        except TimeTrackingNotActiveError as e:
            return f"❌ No active time tracking session to stop.\n\nUse 'start_time_tracking' to begin a new session."
            
        except TimeTrackingError as e:
            return f"❌ Failed to stop time tracking: {e}"
    
    @mcp.tool()
    async def get_current_times(
        project_id: Optional[str] = None,
        person_id: Optional[str] = None
    ) -> str:
        """
        Get currently active time tracking records.
        
        Args:
            project_id: Optional project filter
            person_id: Optional person filter
            
        Returns:
            List of active time tracking records
        """
        try:
            tracker = TimeTracker(graphql_client)
            records = await tracker.get_current_times(project_id, person_id)
            
            if not records:
                filters = []
                if project_id:
                    filters.append(f"project: {project_id}")
                if person_id:
                    filters.append(f"person: {person_id}")
                
                filter_text = f" for {', '.join(filters)}" if filters else ""
                return f"⏸️ No active time tracking records found{filter_text}."
            
            result = f"📊 Active Time Tracking Records ({len(records)}):\n\n"
            
            for i, record in enumerate(records, 1):
                result += f"{i}. **{record['id']}**\n"
                result += f"   • Project: {record['projectId']}\n"
                result += f"   • Person: {record['personId']}\n"
                result += f"   • Start Time: {record['startTime']}\n"
                result += f"   • Description: {record.get('description', 'None')}\n"
                result += f"   • Status: {'🟢 Active' if record['isActive'] else '🔴 Inactive'}\n\n"
            
            return result
            
        except TimeTrackingError as e:
            return f"❌ Failed to get current times: {e}"
    
    @mcp.tool()
    async def get_time_tracking_history(
        project_id: Optional[str] = None,
        person_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Get time tracking history with optional filters.
        
        Args:
            project_id: Optional project filter
            person_id: Optional person filter
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)
            
        Returns:
            Time tracking history records
        """
        try:
            tracker = TimeTracker(graphql_client)
            records = await tracker.get_time_tracking_history(
                project_id, person_id, start_date, end_date
            )
            
            if not records:
                filters = []
                if project_id:
                    filters.append(f"project: {project_id}")
                if person_id:
                    filters.append(f"person: {person_id}")
                if start_date:
                    filters.append(f"from: {start_date}")
                if end_date:
                    filters.append(f"to: {end_date}")
                
                filter_text = f" for {', '.join(filters)}" if filters else ""
                return f"📋 No time tracking records found{filter_text}."
            
            result = f"📊 Time Tracking History ({len(records)} records):\n\n"
            
            for i, record in enumerate(records, 1):
                duration = record.get('durationHours', 'N/A')
                status_icon = '🟢' if record['isActive'] else '🔴'
                status_text = 'Active' if record['isActive'] else 'Completed'
                
                result += f"{i}. **{record['id']}** {status_icon}\n"
                result += f"   • Project: {record['projectId']}\n"
                result += f"   • Person: {record['personId']}\n"
                result += f"   • Start: {record['startTime']}\n"
                result += f"   • End: {record.get('endTime', 'N/A')}\n"
                result += f"   • Duration: {duration} hours\n"
                result += f"   • Status: {status_text}\n"
                if record.get('description'):
                    result += f"   • Description: {record['description']}\n"
                result += "\n"
            
            return result
            
        except TimeTrackingError as e:
            return f"❌ Failed to get time tracking history: {e}"
    
    @mcp.tool()
    async def time_tracking_status() -> str:
        """
        Check current time tracking status.
        
        Returns:
            Current time tracking status information
        """
        try:
            tracker = TimeTracker(graphql_client)
            is_active = tracker.is_tracking_active()
            active_id = tracker.get_active_tracking_id()
            
            if is_active:
                return f"""🟢 Time tracking is currently ACTIVE

📋 Details:
• Active Tracking ID: {active_id}
• Status: Running

Use 'stop_time_tracking' to end the current session."""
            else:
                return """⏸️ No active time tracking session

Use 'start_time_tracking' to begin a new session."""
                
        except TimeTrackingError as e:
            return f"❌ Failed to check time tracking status: {e}"
    
    logger.info("Time tracking MCP tools registered successfully")
