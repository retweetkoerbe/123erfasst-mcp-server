"""
Equipment management functionality for construction projects.

Follows Article I: Library-First Principle - Standalone library for equipment management.
Follows Article V: Error Handling and Resilience - Comprehensive error handling.
"""
import logging
from typing import Optional, List, Dict, Any
from .exceptions import EquipmentManagementError, EquipmentNotFoundError, InvalidEquipmentDataError

logger = logging.getLogger(__name__)


class EquipmentManager:
    """
    Equipment manager for construction projects.
    
    Provides functionality to manage equipment, assignments, and maintenance.
    Follows Article VIII: Anti-Abstraction Principle - Use framework directly.
    """
    
    def __init__(self, graphql_client):
        """
        Initialize equipment manager with GraphQL client.
        
        Args:
            graphql_client: GraphQL client instance for API communication
        """
        self.client = graphql_client
        
        logger.info("EquipmentManager initialized")
    
    async def list_equipment(
        self, 
        status: Optional[str] = None,
        equipment_type: Optional[str] = None,
        location: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        List all equipment with optional filters.
        
        Args:
            status: Optional status filter (operational, maintenance, out_of_service, reserved)
            equipment_type: Optional type filter (Heavy Machinery, Tools, etc.)
            location: Optional location filter
            limit: Optional limit on number of results
            offset: Optional offset for pagination
            
        Returns:
            List of equipment records
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        try:
            # Build GraphQL query with correct schema structure
            query = """
            query GetEquipment {
                equipments {
                    nodes {
                        ident
                        name
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "equipments" not in result:
                return []
            
            # Extract nodes from collection structure
            equipment = result["equipments"].get("nodes", [])
            
            # Apply client-side filtering for now
            if limit:
                equipment = equipment[:limit]
            
            return equipment
            
        except Exception as e:
            logger.error(f"Failed to list equipment: {e}")
            raise EquipmentManagementError(f"Failed to list equipment: {e}")
    
    async def get_equipment_details(self, equipment_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific equipment.
        
        Args:
            equipment_id: Equipment identifier
            
        Returns:
            Detailed equipment information
            
        Raises:
            EquipmentNotFoundError: If equipment doesn't exist
            EquipmentManagementError: For other equipment management errors
        """
        try:
            query = """
            query GetEquipment($id: ID!) {
                equipment(id: $id) {
                    id
                    name
                    type
                    status
                    location
                    model
                    serialNumber
                    purchaseDate
                    lastMaintenance
                    nextMaintenance
                    assignedProjectId
                    assignedPersonId
                    maintenanceHistory {
                        id
                        date
                        description
                        cost
                        performedBy
                    }
                    createdAt
                    updatedAt
                }
            }
            """
            
            result = await self.client.query(query, {"id": equipment_id})
            
            if "equipment" not in result or result["equipment"] is None:
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            
            return result["equipment"]
            
        except EquipmentNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get equipment details for {equipment_id}: {e}")
            raise EquipmentManagementError(f"Failed to get equipment details: {e}")
    
    async def search_equipment(
        self, 
        query: str,
        status: Optional[str] = None,
        equipment_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search equipment by name, model, or serial number.
        
        Args:
            query: Search query string
            status: Optional status filter
            equipment_type: Optional type filter
            limit: Optional limit on number of results
            
        Returns:
            List of matching equipment records
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        try:
            search_query = """
            query SearchEquipment($query: String!, $status: String, $type: String, $limit: Int) {
                equipment(
                    filter: { 
                        search: $query
                        status: $status
                        type: $type
                    }
                    limit: $limit
                    orderBy: relevance_DESC
                ) {
                    id
                    name
                    type
                    status
                    location
                    model
                    serialNumber
                }
            }
            """
            
            variables = {"query": query}
            if status:
                variables["status"] = status
            if equipment_type:
                variables["type"] = equipment_type
            if limit:
                variables["limit"] = limit
            
            result = await self.client.query(search_query, variables)
            
            if "equipment" not in result:
                return []
            
            return result["equipment"]
            
        except Exception as e:
            logger.error(f"Failed to search equipment: {e}")
            raise EquipmentManagementError(f"Failed to search equipment: {e}")
    
    async def get_equipment_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get equipment filtered by status.
        
        Args:
            status: Equipment status (operational, maintenance, out_of_service, reserved)
            
        Returns:
            List of equipment with specified status
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        return await self.list_equipment(status=status)
    
    async def get_equipment_by_type(self, equipment_type: str) -> List[Dict[str, Any]]:
        """
        Get equipment filtered by type.
        
        Args:
            equipment_type: Equipment type (Heavy Machinery, Tools, etc.)
            
        Returns:
            List of equipment with specified type
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        return await self.list_equipment(equipment_type=equipment_type)
    
    async def get_equipment_by_location(self, location: str) -> List[Dict[str, Any]]:
        """
        Get equipment filtered by location.
        
        Args:
            location: Equipment location
            
        Returns:
            List of equipment at specified location
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        return await self.list_equipment(location=location)
    
    async def get_equipment_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get equipment assigned to a specific project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            List of equipment assigned to the project
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        try:
            query = """
            query GetEquipmentByProject($projectId: ID!) {
                equipment(
                    filter: { assignedProjectId: $projectId }
                    orderBy: name_ASC
                ) {
                    id
                    name
                    type
                    status
                    location
                    model
                    assignedProjectId
                    assignedPersonId
                }
            }
            """
            
            result = await self.client.query(query, {"projectId": project_id})
            
            if "equipment" not in result:
                return []
            
            return result["equipment"]
            
        except Exception as e:
            logger.error(f"Failed to get equipment by project: {e}")
            raise EquipmentManagementError(f"Failed to get equipment by project: {e}")
    
    async def get_equipment_by_person(self, person_id: str) -> List[Dict[str, Any]]:
        """
        Get equipment assigned to a specific person.
        
        Args:
            person_id: Person identifier
            
        Returns:
            List of equipment assigned to the person
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        try:
            query = """
            query GetEquipmentByPerson($personId: ID!) {
                equipment(
                    filter: { assignedPersonId: $personId }
                    orderBy: name_ASC
                ) {
                    id
                    name
                    type
                    status
                    location
                    model
                    assignedProjectId
                    assignedPersonId
                }
            }
            """
            
            result = await self.client.query(query, {"personId": person_id})
            
            if "equipment" not in result:
                return []
            
            return result["equipment"]
            
        except Exception as e:
            logger.error(f"Failed to get equipment by person: {e}")
            raise EquipmentManagementError(f"Failed to get equipment by person: {e}")
    
    async def get_equipment_statistics(self) -> Dict[str, Any]:
        """
        Get equipment statistics and metrics.
        
        Returns:
            Dictionary containing equipment statistics
            
        Raises:
            EquipmentManagementError: For equipment management errors
        """
        try:
            query = """
            query GetEquipmentStatistics {
                equipmentStats {
                    totalEquipment
                    operationalEquipment
                    maintenanceEquipment
                    outOfServiceEquipment
                    reservedEquipment
                    equipmentByType {
                        type
                        count
                    }
                    equipmentByStatus {
                        status
                        count
                    }
                    equipmentByLocation {
                        location
                        count
                    }
                    maintenanceDueCount
                    averageMaintenanceCost
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "equipmentStats" not in result:
                return {}
            
            return result["equipmentStats"]
            
        except Exception as e:
            logger.error(f"Failed to get equipment statistics: {e}")
            raise EquipmentManagementError(f"Failed to get equipment statistics: {e}")
    
    async def create_equipment(self, equipment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new equipment.
        
        Args:
            equipment_data: Equipment data dictionary
            
        Returns:
            Created equipment information
            
        Raises:
            InvalidEquipmentDataError: If equipment data is invalid
            EquipmentManagementError: For other equipment management errors
        """
        try:
            # Validate required fields
            required_fields = ["name"]
            for field in required_fields:
                if field not in equipment_data or not equipment_data[field]:
                    raise InvalidEquipmentDataError(f"Required field '{field}' is missing or empty")
            
            mutation = """
            mutation CreateEquipment($input: CreateEquipmentInput!) {
                createEquipment(input: $input) {
                    id
                    name
                    type
                    status
                    location
                    model
                    serialNumber
                    purchaseDate
                    createdAt
                }
            }
            """
            
            result = await self.client.mutation(mutation, {"input": equipment_data})
            
            if "createEquipment" not in result:
                raise EquipmentManagementError("Failed to create equipment")
            
            logger.info(f"Created equipment: {result['createEquipment']['id']}")
            return result["createEquipment"]
            
        except InvalidEquipmentDataError:
            raise
        except Exception as e:
            logger.error(f"Failed to create equipment: {e}")
            raise EquipmentManagementError(f"Failed to create equipment: {e}")
    
    async def update_equipment(
        self, 
        equipment_id: str, 
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing equipment.
        
        Args:
            equipment_id: Equipment identifier
            update_data: Fields to update
            
        Returns:
            Updated equipment information
            
        Raises:
            EquipmentNotFoundError: If equipment doesn't exist
            EquipmentManagementError: For other equipment management errors
        """
        try:
            mutation = """
            mutation UpdateEquipment($id: ID!, $input: UpdateEquipmentInput!) {
                updateEquipment(id: $id, input: $input) {
                    id
                    name
                    type
                    status
                    location
                    model
                    serialNumber
                    updatedAt
                }
            }
            """
            
            result = await self.client.mutation(mutation, {
                "id": equipment_id,
                "input": update_data
            })
            
            if "updateEquipment" not in result:
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            
            logger.info(f"Updated equipment: {equipment_id}")
            return result["updateEquipment"]
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            logger.error(f"Failed to update equipment {equipment_id}: {e}")
            raise EquipmentManagementError(f"Failed to update equipment: {e}")
    
    async def assign_equipment_to_project(
        self, 
        equipment_id: str, 
        project_id: str
    ) -> bool:
        """
        Assign equipment to a project.
        
        Args:
            equipment_id: Equipment identifier
            project_id: Project identifier
            
        Returns:
            True if assignment was successful
            
        Raises:
            EquipmentNotFoundError: If equipment doesn't exist
            EquipmentManagementError: For other equipment management errors
        """
        try:
            mutation = """
            mutation AssignEquipmentToProject($equipmentId: ID!, $projectId: ID!) {
                assignEquipmentToProject(equipmentId: $equipmentId, projectId: $projectId) {
                    success
                    message
                }
            }
            """
            
            result = await self.client.mutation(mutation, {
                "equipmentId": equipment_id,
                "projectId": project_id
            })
            
            if "assignEquipmentToProject" not in result:
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            
            success = result["assignEquipmentToProject"]["success"]
            if success:
                logger.info(f"Assigned equipment {equipment_id} to project {project_id}")
            else:
                logger.warning(f"Failed to assign equipment {equipment_id} to project {project_id}: {result['assignEquipmentToProject']['message']}")
            
            return success
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            logger.error(f"Failed to assign equipment to project: {e}")
            raise EquipmentManagementError(f"Failed to assign equipment to project: {e}")
    
    async def assign_equipment_to_person(
        self, 
        equipment_id: str, 
        person_id: str
    ) -> bool:
        """
        Assign equipment to a person.
        
        Args:
            equipment_id: Equipment identifier
            person_id: Person identifier
            
        Returns:
            True if assignment was successful
            
        Raises:
            EquipmentNotFoundError: If equipment doesn't exist
            EquipmentManagementError: For other equipment management errors
        """
        try:
            mutation = """
            mutation AssignEquipmentToPerson($equipmentId: ID!, $personId: ID!) {
                assignEquipmentToPerson(equipmentId: $equipmentId, personId: $personId) {
                    success
                    message
                }
            }
            """
            
            result = await self.client.mutation(mutation, {
                "equipmentId": equipment_id,
                "personId": person_id
            })
            
            if "assignEquipmentToPerson" not in result:
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            
            success = result["assignEquipmentToPerson"]["success"]
            if success:
                logger.info(f"Assigned equipment {equipment_id} to person {person_id}")
            else:
                logger.warning(f"Failed to assign equipment {equipment_id} to person {person_id}: {result['assignEquipmentToPerson']['message']}")
            
            return success
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            logger.error(f"Failed to assign equipment to person: {e}")
            raise EquipmentManagementError(f"Failed to assign equipment to person: {e}")
    
    async def unassign_equipment(self, equipment_id: str) -> bool:
        """
        Unassign equipment from project and person.
        
        Args:
            equipment_id: Equipment identifier
            
        Returns:
            True if unassignment was successful
            
        Raises:
            EquipmentNotFoundError: If equipment doesn't exist
            EquipmentManagementError: For other equipment management errors
        """
        try:
            mutation = """
            mutation UnassignEquipment($equipmentId: ID!) {
                unassignEquipment(equipmentId: $equipmentId) {
                    success
                    message
                }
            }
            """
            
            result = await self.client.mutation(mutation, {"equipmentId": equipment_id})
            
            if "unassignEquipment" not in result:
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            
            success = result["unassignEquipment"]["success"]
            if success:
                logger.info(f"Unassigned equipment {equipment_id}")
            else:
                logger.warning(f"Failed to unassign equipment {equipment_id}: {result['unassignEquipment']['message']}")
            
            return success
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise EquipmentNotFoundError(f"Equipment {equipment_id} not found")
            logger.error(f"Failed to unassign equipment: {e}")
            raise EquipmentManagementError(f"Failed to unassign equipment: {e}")
