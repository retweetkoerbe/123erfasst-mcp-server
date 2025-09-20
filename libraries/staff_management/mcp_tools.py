"""
MCP tools for staff management functionality.

Follows Article I: Library-First Principle - MCP tools use standalone libraries.
"""
import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .staff_manager import StaffManager
from .exceptions import StaffManagementError, PersonNotFoundError, InvalidPersonDataError

logger = logging.getLogger(__name__)


def register_staff_management_tools(mcp: FastMCP, graphql_client) -> None:
    """
    Register staff management MCP tools.
    
    Args:
        mcp: FastMCP server instance
        graphql_client: GraphQL client for API communication
    """
    
    @mcp.tool()
    async def list_staff(
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: Optional[int] = None
    ) -> str:
        """
        List all staff members with optional filters.
        
        Args:
            role: Optional role filter (Site Manager, Engineer, Worker, etc.)
            is_active: Optional active status filter
            limit: Optional limit on number of results
            
        Returns:
            List of staff members with details
        """
        try:
            manager = StaffManager(graphql_client)
            staff = await manager.list_staff(role=role, is_active=is_active, limit=limit)
            
            if not staff:
                role_text = f" with role '{role}'" if role else ""
                active_text = " (active only)" if is_active else ""
                return f"👥 No staff members found{role_text}{active_text}."
            
            result = f"👥 Staff Members ({len(staff)}):\n\n"
            
            for i, person in enumerate(staff, 1):
                result += f"{i}. **{person.get('formattedName', 'Unknown Person')}**\n"
                result += f"   • ID: {person.get('ident', 'N/A')}\n"
                result += f"   • First Name: {person.get('firstname', 'N/A')}\n"
                result += f"   • Last Name: {person.get('lastname', 'N/A')}\n"
                result += f"   • Role: N/A (not available in current schema)\n"
                result += f"   • Email: N/A (not available in current schema)\n"
                result += f"   • Phone: N/A (not available in current schema)\n"
                result += "\n"
            
            return result
            
        except StaffManagementError as e:
            return f"❌ Failed to list staff: {e}"
    
    @mcp.tool()
    async def get_person_details(person_id: str) -> str:
        """
        Get detailed information for a specific staff member.
        
        Args:
            person_id: Person identifier
            
        Returns:
            Detailed person information
        """
        try:
            manager = StaffManager(graphql_client)
            person = await manager.get_person_details(person_id)
            
            status_icon = "🟢" if person.get('isActive', True) else "🔴"
            result = f"👤 **{person['name']}** {status_icon}\n\n"
            
            result += f"**Basic Information:**\n"
            result += f"• ID: {person['id']}\n"
            result += f"• Role: {person.get('role', 'N/A')}\n"
            result += f"• Email: {person.get('email', 'N/A')}\n"
            result += f"• Phone: {person.get('phone', 'N/A')}\n"
            result += f"• Department: {person.get('department', 'N/A')}\n"
            result += f"• Status: {'Active' if person.get('isActive', True) else 'Inactive'}\n"
            result += f"• Hire Date: {person.get('hireDate', 'N/A')}\n"
            
            if person.get('skills'):
                result += f"\n**Skills:**\n"
                for skill in person['skills']:
                    result += f"• {skill}\n"
            
            if person.get('assignedProjects'):
                result += f"\n**Assigned Projects ({len(person['assignedProjects'])}):**\n"
                for project in person['assignedProjects']:
                    status_icon = {
                        'active': '🟢',
                        'completed': '✅',
                        'on_hold': '⏸️',
                        'cancelled': '❌',
                        'planning': '📋'
                    }.get(project.get('status', ''), '❓')
                    result += f"• {project['name']} {status_icon}\n"
            
            if person.get('timeTracking'):
                result += f"\n**Recent Time Tracking ({len(person['timeTracking'])}):**\n"
                for tracking in person['timeTracking'][:5]:  # Show last 5
                    duration = tracking.get('durationHours', 'N/A')
                    result += f"• {tracking.get('projectId', 'N/A')}: {duration} hours\n"
            
            return result
            
        except PersonNotFoundError as e:
            return f"❌ {e}"
        except StaffManagementError as e:
            return f"❌ Failed to get person details: {e}"
    
    @mcp.tool()
    async def search_staff(
        query: str,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: Optional[int] = None
    ) -> str:
        """
        Search staff by name, role, or email.
        
        Args:
            query: Search query string
            role: Optional role filter
            is_active: Optional active status filter
            limit: Optional limit on number of results
            
        Returns:
            List of matching staff members
        """
        try:
            manager = StaffManager(graphql_client)
            staff = await manager.search_staff(query, role=role, is_active=is_active, limit=limit)
            
            if not staff:
                role_text = f" with role '{role}'" if role else ""
                active_text = " (active only)" if is_active else ""
                return f"🔍 No staff members found matching '{query}'{role_text}{active_text}."
            
            result = f"🔍 Search Results for '{query}' ({len(staff)}):\n\n"
            
            for i, person in enumerate(staff, 1):
                status_icon = "🟢" if person.get('isActive', True) else "🔴"
                result += f"{i}. **{person['name']}** {status_icon}\n"
                result += f"   • ID: {person['id']}\n"
                result += f"   • Role: {person.get('role', 'N/A')}\n"
                result += f"   • Email: {person.get('email', 'N/A')}\n"
                result += f"   • Department: {person.get('department', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except StaffManagementError as e:
            return f"❌ Failed to search staff: {e}"
    
    @mcp.tool()
    async def get_staff_statistics() -> str:
        """
        Get staff statistics and metrics.
        
        Returns:
            Staff statistics summary
        """
        try:
            manager = StaffManager(graphql_client)
            stats = await manager.get_staff_statistics()
            
            result = "📊 **Staff Statistics**\n\n"
            result += f"**Overview:**\n"
            result += f"• Total Staff: {stats.get('totalStaff', 0)}\n"
            result += f"• Active Staff: {stats.get('activeStaff', 0)} 🟢\n"
            result += f"• Inactive Staff: {stats.get('inactiveStaff', 0)} 🔴\n"
            result += f"• Average Tenure: {stats.get('averageTenure', 0)} years\n"
            result += f"• New Hires This Month: {stats.get('newHiresThisMonth', 0)}\n\n"
            
            if stats.get('staffByRole'):
                result += f"**Staff by Role:**\n"
                for role_info in stats['staffByRole']:
                    result += f"• {role_info['role']}: {role_info['count']}\n"
                result += "\n"
            
            if stats.get('staffByDepartment'):
                result += f"**Staff by Department:**\n"
                for dept_info in stats['staffByDepartment']:
                    result += f"• {dept_info['department']}: {dept_info['count']}\n"
            
            return result
            
        except StaffManagementError as e:
            return f"❌ Failed to get staff statistics: {e}"
    
    @mcp.tool()
    async def get_active_staff() -> str:
        """
        Get all active staff members.
        
        Returns:
            List of active staff members
        """
        try:
            manager = StaffManager(graphql_client)
            staff = await manager.get_active_staff()
            
            if not staff:
                return "⏸️ No active staff members found."
            
            result = f"🟢 **Active Staff** ({len(staff)}):\n\n"
            
            for i, person in enumerate(staff, 1):
                result += f"{i}. **{person['name']}**\n"
                result += f"   • ID: {person['id']}\n"
                result += f"   • Role: {person.get('role', 'N/A')}\n"
                result += f"   • Email: {person.get('email', 'N/A')}\n"
                if person.get('department'):
                    result += f"   • Department: {person['department']}\n"
                result += "\n"
            
            return result
            
        except StaffManagementError as e:
            return f"❌ Failed to get active staff: {e}"
    
    @mcp.tool()
    async def get_staff_by_role(role: str) -> str:
        """
        Get staff members filtered by role.
        
        Args:
            role: Staff role (Site Manager, Engineer, Worker, etc.)
            
        Returns:
            List of staff members with specified role
        """
        try:
            manager = StaffManager(graphql_client)
            staff = await manager.get_staff_by_role(role)
            
            if not staff:
                return f"👥 No staff members found with role '{role}'."
            
            result = f"👥 **Staff with Role '{role}'** ({len(staff)}):\n\n"
            
            for i, person in enumerate(staff, 1):
                status_icon = "🟢" if person.get('isActive', True) else "🔴"
                result += f"{i}. **{person['name']}** {status_icon}\n"
                result += f"   • ID: {person['id']}\n"
                result += f"   • Email: {person.get('email', 'N/A')}\n"
                result += f"   • Department: {person.get('department', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except StaffManagementError as e:
            return f"❌ Failed to get staff by role: {e}"
    
    @mcp.tool()
    async def get_staff_by_project(project_id: str) -> str:
        """
        Get staff members assigned to a specific project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            List of staff members assigned to the project
        """
        try:
            manager = StaffManager(graphql_client)
            staff = await manager.get_staff_by_project(project_id)
            
            if not staff:
                return f"👥 No staff members assigned to project {project_id}."
            
            result = f"👥 **Staff Assigned to Project {project_id}** ({len(staff)}):\n\n"
            
            for i, person in enumerate(staff, 1):
                status_icon = "🟢" if person.get('isActive', True) else "🔴"
                result += f"{i}. **{person['name']}** {status_icon}\n"
                result += f"   • ID: {person['id']}\n"
                result += f"   • Role: {person.get('role', 'N/A')}\n"
                result += f"   • Email: {person.get('email', 'N/A')}\n"
                result += f"   • Department: {person.get('department', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except StaffManagementError as e:
            return f"❌ Failed to get staff by project: {e}"
    
    logger.info("Staff management MCP tools registered successfully")
