"""
MCP tools for project management functionality.

Follows Article I: Library-First Principle - MCP tools use standalone libraries.
"""
import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .project_manager import ProjectManager
from .exceptions import ProjectManagementError, ProjectNotFoundError, InvalidProjectDataError

logger = logging.getLogger(__name__)


def register_project_management_tools(mcp: FastMCP, graphql_client) -> None:
    """
    Register project management MCP tools.
    
    Args:
        mcp: FastMCP server instance
        graphql_client: GraphQL client for API communication
    """
    
    @mcp.tool()
    async def list_projects(
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> str:
        """
        List all projects with optional filters.
        
        Args:
            status: Optional status filter (active, completed, on_hold, cancelled, planning)
            limit: Optional limit on number of results
            
        Returns:
            List of projects with details
        """
        try:
            manager = ProjectManager(graphql_client)
            projects = await manager.list_projects(status=status, limit=limit)
            
            if not projects:
                status_text = f" with status '{status}'" if status else ""
                return f"📋 No projects found{status_text}."
            
            result = f"📊 Projects ({len(projects)}):\n\n"
            
            for i, project in enumerate(projects, 1):
                result += f"{i}. **{project.get('name', 'Unknown Project')}**\n"
                result += f"   • ID: {project.get('ident', 'N/A')}\n"
                result += f"   • Status: N/A (not available in current schema)\n"
                result += f"   • Client: N/A (not available in current schema)\n"
                result += f"   • Start: N/A (not available in current schema)\n"
                result += f"   • End: N/A (not available in current schema)\n"
                result += "\n"
            
            return result
            
        except ProjectManagementError as e:
            return f"❌ Failed to list projects: {e}"
    
    @mcp.tool()
    async def get_project_details(project_id: str) -> str:
        """
        Get detailed information for a specific project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Detailed project information
        """
        try:
            manager = ProjectManager(graphql_client)
            project = await manager.get_project_details(project_id)
            
            status_icon = {
                'active': '🟢',
                'completed': '✅',
                'on_hold': '⏸️',
                'cancelled': '❌',
                'planning': '📋'
            }.get(project['status'], '❓')
            
            result = f"📋 **{project['name']}** {status_icon}\n\n"
            result += f"**Basic Information:**\n"
            result += f"• ID: {project['id']}\n"
            result += f"• Status: {project['status']}\n"
            result += f"• Description: {project.get('description', 'N/A')}\n"
            result += f"• Client: {project.get('clientName', 'N/A')}\n"
            result += f"• Location: {project.get('location', 'N/A')}\n"
            result += f"• Start Date: {project.get('startDate', 'N/A')}\n"
            result += f"• End Date: {project.get('endDate', 'N/A')}\n"
            
            if project.get('budget'):
                result += f"• Budget: ${project['budget']:,.2f}\n"
            
            if project.get('staff'):
                result += f"\n**Staff ({len(project['staff'])}):**\n"
                for person in project['staff']:
                    result += f"• {person['name']} - {person['role']}\n"
            
            if project.get('equipment'):
                result += f"\n**Equipment ({len(project['equipment'])}):**\n"
                for equipment in project['equipment']:
                    status_icon = '🟢' if equipment['status'] == 'operational' else '🔴'
                    result += f"• {equipment['name']} ({equipment['type']}) {status_icon}\n"
            
            return result
            
        except ProjectNotFoundError as e:
            return f"❌ {e}"
        except ProjectManagementError as e:
            return f"❌ Failed to get project details: {e}"
    
    @mcp.tool()
    async def search_projects(
        query: str,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> str:
        """
        Search projects by name, description, or client name.
        
        Args:
            query: Search query string
            status: Optional status filter
            limit: Optional limit on number of results
            
        Returns:
            List of matching projects
        """
        try:
            manager = ProjectManager(graphql_client)
            projects = await manager.search_projects(query, status=status, limit=limit)
            
            if not projects:
                status_text = f" with status '{status}'" if status else ""
                return f"🔍 No projects found matching '{query}'{status_text}."
            
            result = f"🔍 Search Results for '{query}' ({len(projects)}):\n\n"
            
            for i, project in enumerate(projects, 1):
                status_icon = {
                    'active': '🟢',
                    'completed': '✅',
                    'on_hold': '⏸️',
                    'cancelled': '❌',
                    'planning': '📋'
                }.get(project['status'], '❓')
                
                result += f"{i}. **{project['name']}** {status_icon}\n"
                result += f"   • ID: {project['id']}\n"
                result += f"   • Status: {project['status']}\n"
                result += f"   • Client: {project.get('clientName', 'N/A')}\n"
                result += f"   • Location: {project.get('location', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except ProjectManagementError as e:
            return f"❌ Failed to search projects: {e}"
    
    @mcp.tool()
    async def get_project_statistics() -> str:
        """
        Get project statistics and metrics.
        
        Returns:
            Project statistics summary
        """
        try:
            manager = ProjectManager(graphql_client)
            stats = await manager.get_project_statistics()
            
            result = "📊 **Project Statistics**\n\n"
            result += f"**Overview:**\n"
            result += f"• Total Projects: {stats.get('totalProjects', 0)}\n"
            result += f"• Active Projects: {stats.get('activeProjects', 0)} 🟢\n"
            result += f"• Completed Projects: {stats.get('completedProjects', 0)} ✅\n"
            result += f"• On Hold Projects: {stats.get('onHoldProjects', 0)} ⏸️\n"
            result += f"• Cancelled Projects: {stats.get('cancelledProjects', 0)} ❌\n\n"
            
            result += f"**Financial:**\n"
            result += f"• Total Budget: ${stats.get('totalBudget', 0):,.2f}\n"
            result += f"• Average Budget: ${stats.get('averageProjectBudget', 0):,.2f}\n\n"
            
            result += f"**Timeline:**\n"
            result += f"• Average Duration: {stats.get('averageProjectDuration', 0)} days\n"
            
            if stats.get('projectsByStatus'):
                result += f"\n**Projects by Status:**\n"
                for status_info in stats['projectsByStatus']:
                    status_icon = {
                        'active': '🟢',
                        'completed': '✅',
                        'on_hold': '⏸️',
                        'cancelled': '❌',
                        'planning': '📋'
                    }.get(status_info['status'], '❓')
                    result += f"• {status_info['status'].title()}: {status_info['count']} {status_icon}\n"
            
            return result
            
        except ProjectManagementError as e:
            return f"❌ Failed to get project statistics: {e}"
    
    @mcp.tool()
    async def get_active_projects() -> str:
        """
        Get all currently active projects.
        
        Returns:
            List of active projects
        """
        try:
            manager = ProjectManager(graphql_client)
            projects = await manager.get_projects_by_status("active")
            
            if not projects:
                return "⏸️ No active projects found."
            
            result = f"🟢 **Active Projects** ({len(projects)}):\n\n"
            
            for i, project in enumerate(projects, 1):
                result += f"{i}. **{project['name']}**\n"
                result += f"   • ID: {project['id']}\n"
                result += f"   • Client: {project.get('clientName', 'N/A')}\n"
                result += f"   • Start: {project.get('startDate', 'N/A')}\n"
                result += f"   • End: {project.get('endDate', 'N/A')}\n"
                if project.get('location'):
                    result += f"   • Location: {project['location']}\n"
                result += "\n"
            
            return result
            
        except ProjectManagementError as e:
            return f"❌ Failed to get active projects: {e}"
    
    @mcp.tool()
    async def get_projects_by_date_range(start_date: str, end_date: str) -> str:
        """
        Get projects within a specific date range.
        
        Args:
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            List of projects within date range
        """
        try:
            manager = ProjectManager(graphql_client)
            projects = await manager.get_projects_by_date_range(start_date, end_date)
            
            if not projects:
                return f"📅 No projects found between {start_date} and {end_date}."
            
            result = f"📅 **Projects ({start_date} to {end_date})** ({len(projects)}):\n\n"
            
            for i, project in enumerate(projects, 1):
                status_icon = {
                    'active': '🟢',
                    'completed': '✅',
                    'on_hold': '⏸️',
                    'cancelled': '❌',
                    'planning': '📋'
                }.get(project['status'], '❓')
                
                result += f"{i}. **{project['name']}** {status_icon}\n"
                result += f"   • ID: {project['id']}\n"
                result += f"   • Status: {project['status']}\n"
                result += f"   • Client: {project.get('clientName', 'N/A')}\n"
                result += f"   • Start: {project.get('startDate', 'N/A')}\n"
                result += f"   • End: {project.get('endDate', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except ProjectManagementError as e:
            return f"❌ Failed to get projects by date range: {e}"
    
    logger.info("Project management MCP tools registered successfully")
