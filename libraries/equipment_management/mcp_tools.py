"""
MCP tools for equipment management functionality.

Follows Article I: Library-First Principle - MCP tools use standalone libraries.
"""
import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .equipment_manager import EquipmentManager
from .exceptions import EquipmentManagementError, EquipmentNotFoundError, InvalidEquipmentDataError

logger = logging.getLogger(__name__)


def register_equipment_management_tools(mcp: FastMCP, graphql_client) -> None:
    """
    Register equipment management MCP tools.
    
    Args:
        mcp: FastMCP server instance
        graphql_client: GraphQL client for API communication
    """
    
    @mcp.tool()
    async def list_equipment(
        status: Optional[str] = None,
        equipment_type: Optional[str] = None,
        location: Optional[str] = None,
        limit: Optional[int] = None
    ) -> str:
        """
        List all equipment with optional filters.
        
        Args:
            status: Optional status filter (operational, maintenance, out_of_service, reserved)
            equipment_type: Optional type filter (Heavy Machinery, Tools, etc.)
            location: Optional location filter
            limit: Optional limit on number of results
            
        Returns:
            List of equipment with details
        """
        try:
            manager = EquipmentManager(graphql_client)
            equipment = await manager.list_equipment(
                status=status, 
                equipment_type=equipment_type, 
                location=location, 
                limit=limit
            )
            
            if not equipment:
                filters = []
                if status:
                    filters.append(f"status: {status}")
                if equipment_type:
                    filters.append(f"type: {equipment_type}")
                if location:
                    filters.append(f"location: {location}")
                
                filter_text = f" with filters: {', '.join(filters)}" if filters else ""
                return f"🔧 No equipment found{filter_text}."
            
            result = f"🔧 Equipment ({len(equipment)}):\n\n"
            
            for i, item in enumerate(equipment, 1):
                result += f"{i}. **{item.get('name', 'Unknown Equipment')}**\n"
                result += f"   • ID: {item.get('ident', 'N/A')}\n"
                result += f"   • Type: N/A (not available in current schema)\n"
                result += f"   • Status: N/A (not available in current schema)\n"
                result += f"   • Location: N/A (not available in current schema)\n"
                result += f"   • Model: N/A (not available in current schema)\n"
                result += f"   • Serial: N/A (not available in current schema)\n"
                result += "\n"
            
            return result
            
        except EquipmentManagementError as e:
            return f"❌ Failed to list equipment: {e}"
    
    @mcp.tool()
    async def get_equipment_details(equipment_id: str) -> str:
        """
        Get detailed information for a specific equipment.
        
        Args:
            equipment_id: Equipment identifier
            
        Returns:
            Detailed equipment information
        """
        try:
            manager = EquipmentManager(graphql_client)
            equipment = await manager.get_equipment_details(equipment_id)
            
            status_icon = {
                'operational': '🟢',
                'maintenance': '🔧',
                'out_of_service': '🔴',
                'reserved': '⏸️'
            }.get(equipment.get('status', ''), '❓')
            
            result = f"🔧 **{equipment['name']}** {status_icon}\n\n"
            
            result += f"**Basic Information:**\n"
            result += f"• ID: {equipment['id']}\n"
            result += f"• Type: {equipment.get('type', 'N/A')}\n"
            result += f"• Status: {equipment.get('status', 'N/A')}\n"
            result += f"• Location: {equipment.get('location', 'N/A')}\n"
            result += f"• Model: {equipment.get('model', 'N/A')}\n"
            result += f"• Serial Number: {equipment.get('serialNumber', 'N/A')}\n"
            result += f"• Purchase Date: {equipment.get('purchaseDate', 'N/A')}\n"
            
            if equipment.get('assignedProjectId'):
                result += f"• Assigned Project: {equipment['assignedProjectId']}\n"
            if equipment.get('assignedPersonId'):
                result += f"• Assigned Person: {equipment['assignedPersonId']}\n"
            
            if equipment.get('lastMaintenance'):
                result += f"\n**Maintenance:**\n"
                result += f"• Last Maintenance: {equipment['lastMaintenance']}\n"
                if equipment.get('nextMaintenance'):
                    result += f"• Next Maintenance: {equipment['nextMaintenance']}\n"
            
            if equipment.get('maintenanceHistory'):
                result += f"\n**Maintenance History ({len(equipment['maintenanceHistory'])}):**\n"
                for maintenance in equipment['maintenanceHistory'][:5]:  # Show last 5
                    result += f"• {maintenance.get('date', 'N/A')}: {maintenance.get('description', 'N/A')}\n"
            
            return result
            
        except EquipmentNotFoundError as e:
            return f"❌ {e}"
        except EquipmentManagementError as e:
            return f"❌ Failed to get equipment details: {e}"
    
    @mcp.tool()
    async def search_equipment(
        query: str,
        status: Optional[str] = None,
        equipment_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> str:
        """
        Search equipment by name, model, or serial number.
        
        Args:
            query: Search query string
            status: Optional status filter
            equipment_type: Optional type filter
            limit: Optional limit on number of results
            
        Returns:
            List of matching equipment
        """
        try:
            manager = EquipmentManager(graphql_client)
            equipment = await manager.search_equipment(
                query, 
                status=status, 
                equipment_type=equipment_type, 
                limit=limit
            )
            
            if not equipment:
                filters = []
                if status:
                    filters.append(f"status: {status}")
                if equipment_type:
                    filters.append(f"type: {equipment_type}")
                
                filter_text = f" with filters: {', '.join(filters)}" if filters else ""
                return f"🔍 No equipment found matching '{query}'{filter_text}."
            
            result = f"🔍 Search Results for '{query}' ({len(equipment)}):\n\n"
            
            for i, item in enumerate(equipment, 1):
                status_icon = {
                    'operational': '🟢',
                    'maintenance': '🔧',
                    'out_of_service': '🔴',
                    'reserved': '⏸️'
                }.get(item.get('status', ''), '❓')
                
                result += f"{i}. **{item['name']}** {status_icon}\n"
                result += f"   • ID: {item['id']}\n"
                result += f"   • Type: {item.get('type', 'N/A')}\n"
                result += f"   • Status: {item.get('status', 'N/A')}\n"
                result += f"   • Location: {item.get('location', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except EquipmentManagementError as e:
            return f"❌ Failed to search equipment: {e}"
    
    @mcp.tool()
    async def get_equipment_statistics() -> str:
        """
        Get equipment statistics and metrics.
        
        Returns:
            Equipment statistics summary
        """
        try:
            manager = EquipmentManager(graphql_client)
            stats = await manager.get_equipment_statistics()
            
            result = "📊 **Equipment Statistics**\n\n"
            result += f"**Overview:**\n"
            result += f"• Total Equipment: {stats.get('totalEquipment', 0)}\n"
            result += f"• Operational: {stats.get('operationalEquipment', 0)} 🟢\n"
            result += f"• Maintenance: {stats.get('maintenanceEquipment', 0)} 🔧\n"
            result += f"• Out of Service: {stats.get('outOfServiceEquipment', 0)} 🔴\n"
            result += f"• Reserved: {stats.get('reservedEquipment', 0)} ⏸️\n"
            result += f"• Maintenance Due: {stats.get('maintenanceDueCount', 0)}\n"
            result += f"• Avg Maintenance Cost: ${stats.get('averageMaintenanceCost', 0):,.2f}\n\n"
            
            if stats.get('equipmentByType'):
                result += f"**Equipment by Type:**\n"
                for type_info in stats['equipmentByType']:
                    result += f"• {type_info['type']}: {type_info['count']}\n"
                result += "\n"
            
            if stats.get('equipmentByStatus'):
                result += f"**Equipment by Status:**\n"
                for status_info in stats['equipmentByStatus']:
                    status_icon = {
                        'operational': '🟢',
                        'maintenance': '🔧',
                        'out_of_service': '🔴',
                        'reserved': '⏸️'
                    }.get(status_info['status'], '❓')
                    result += f"• {status_info['status'].title()}: {status_info['count']} {status_icon}\n"
                result += "\n"
            
            if stats.get('equipmentByLocation'):
                result += f"**Equipment by Location:**\n"
                for location_info in stats['equipmentByLocation']:
                    result += f"• {location_info['location']}: {location_info['count']}\n"
            
            return result
            
        except EquipmentManagementError as e:
            return f"❌ Failed to get equipment statistics: {e}"
    
    @mcp.tool()
    async def get_operational_equipment() -> str:
        """
        Get all operational equipment.
        
        Returns:
            List of operational equipment
        """
        try:
            manager = EquipmentManager(graphql_client)
            equipment = await manager.get_equipment_by_status("operational")
            
            if not equipment:
                return "🟢 No operational equipment found."
            
            result = f"🟢 **Operational Equipment** ({len(equipment)}):\n\n"
            
            for i, item in enumerate(equipment, 1):
                result += f"{i}. **{item['name']}**\n"
                result += f"   • ID: {item['id']}\n"
                result += f"   • Type: {item.get('type', 'N/A')}\n"
                result += f"   • Location: {item.get('location', 'N/A')}\n"
                if item.get('model'):
                    result += f"   • Model: {item['model']}\n"
                result += "\n"
            
            return result
            
        except EquipmentManagementError as e:
            return f"❌ Failed to get operational equipment: {e}"
    
    @mcp.tool()
    async def get_equipment_by_project(project_id: str) -> str:
        """
        Get equipment assigned to a specific project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            List of equipment assigned to the project
        """
        try:
            manager = EquipmentManager(graphql_client)
            equipment = await manager.get_equipment_by_project(project_id)
            
            if not equipment:
                return f"🔧 No equipment assigned to project {project_id}."
            
            result = f"🔧 **Equipment Assigned to Project {project_id}** ({len(equipment)}):\n\n"
            
            for i, item in enumerate(equipment, 1):
                status_icon = {
                    'operational': '🟢',
                    'maintenance': '🔧',
                    'out_of_service': '🔴',
                    'reserved': '⏸️'
                }.get(item.get('status', ''), '❓')
                
                result += f"{i}. **{item['name']}** {status_icon}\n"
                result += f"   • ID: {item['id']}\n"
                result += f"   • Type: {item.get('type', 'N/A')}\n"
                result += f"   • Status: {item.get('status', 'N/A')}\n"
                result += f"   • Location: {item.get('location', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except EquipmentManagementError as e:
            return f"❌ Failed to get equipment by project: {e}"
    
    @mcp.tool()
    async def get_equipment_by_person(person_id: str) -> str:
        """
        Get equipment assigned to a specific person.
        
        Args:
            person_id: Person identifier
            
        Returns:
            List of equipment assigned to the person
        """
        try:
            manager = EquipmentManager(graphql_client)
            equipment = await manager.get_equipment_by_person(person_id)
            
            if not equipment:
                return f"🔧 No equipment assigned to person {person_id}."
            
            result = f"🔧 **Equipment Assigned to Person {person_id}** ({len(equipment)}):\n\n"
            
            for i, item in enumerate(equipment, 1):
                status_icon = {
                    'operational': '🟢',
                    'maintenance': '🔧',
                    'out_of_service': '🔴',
                    'reserved': '⏸️'
                }.get(item.get('status', ''), '❓')
                
                result += f"{i}. **{item['name']}** {status_icon}\n"
                result += f"   • ID: {item['id']}\n"
                result += f"   • Type: {item.get('type', 'N/A')}\n"
                result += f"   • Status: {item.get('status', 'N/A')}\n"
                result += f"   • Location: {item.get('location', 'N/A')}\n"
                result += "\n"
            
            return result
            
        except EquipmentManagementError as e:
            return f"❌ Failed to get equipment by person: {e}"
    
    @mcp.tool()
    async def get_maintenance_due_equipment() -> str:
        """
        Get equipment that is due for maintenance.
        
        Returns:
            List of equipment due for maintenance
        """
        try:
            manager = EquipmentManager(graphql_client)
            equipment = await manager.get_equipment_by_status("maintenance")
            
            if not equipment:
                return "🔧 No equipment currently in maintenance."
            
            result = f"🔧 **Equipment in Maintenance** ({len(equipment)}):\n\n"
            
            for i, item in enumerate(equipment, 1):
                result += f"{i}. **{item['name']}**\n"
                result += f"   • ID: {item['id']}\n"
                result += f"   • Type: {item.get('type', 'N/A')}\n"
                result += f"   • Location: {item.get('location', 'N/A')}\n"
                if item.get('lastMaintenance'):
                    result += f"   • Last Maintenance: {item['lastMaintenance']}\n"
                if item.get('nextMaintenance'):
                    result += f"   • Next Maintenance: {item['nextMaintenance']}\n"
                result += "\n"
            
            return result
            
        except EquipmentManagementError as e:
            return f"❌ Failed to get maintenance due equipment: {e}"
    
    logger.info("Equipment management MCP tools registered successfully")
