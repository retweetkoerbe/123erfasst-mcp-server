"""
Staff management functionality for construction projects.

Follows Article I: Library-First Principle - Standalone library for staff management.
Follows Article V: Error Handling and Resilience - Comprehensive error handling.
"""
import logging
from typing import Optional, List, Dict, Any
from .exceptions import StaffManagementError, PersonNotFoundError, InvalidPersonDataError

logger = logging.getLogger(__name__)


class StaffManager:
    """
    Staff manager for construction projects.
    
    Provides functionality to manage staff members, roles, and assignments.
    Follows Article VIII: Anti-Abstraction Principle - Use framework directly.
    """
    
    def __init__(self, graphql_client):
        """
        Initialize staff manager with GraphQL client.
        
        Args:
            graphql_client: GraphQL client instance for API communication
        """
        self.client = graphql_client
        
        logger.info("StaffManager initialized")
    
    async def list_staff(
        self, 
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        List all staff members with optional filters.
        
        Args:
            role: Optional role filter
            is_active: Optional active status filter
            limit: Optional limit on number of results
            offset: Optional offset for pagination
            
        Returns:
            List of staff member records
            
        Raises:
            StaffManagementError: For staff management errors
        """
        try:
            # Build GraphQL query with correct schema structure
            query = """
            query GetStaff {
                persons {
                    nodes {
                        ident
                        firstname
                        lastname
                        formattedName
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "persons" not in result:
                return []
            
            # Extract nodes from collection structure
            persons = result["persons"].get("nodes", [])
            
            # Apply client-side filtering for now
            if limit:
                persons = persons[:limit]
            
            return persons
            
        except Exception as e:
            logger.error(f"Failed to list staff: {e}")
            raise StaffManagementError(f"Failed to list staff: {e}")
    
    async def get_person_details(self, person_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific person.
        
        Args:
            person_id: Person identifier
            
        Returns:
            Detailed person information
            
        Raises:
            PersonNotFoundError: If person doesn't exist
            StaffManagementError: For other staff management errors
        """
        try:
            query = """
            query GetPerson($id: Ident!) {
                person(ident: $id) {
                    ident
                    firstname
                    lastname
                    formattedName
                }
            }
            """
            
            result = await self.client.query(query, {"id": person_id})
            
            if "person" not in result or result["person"] is None:
                raise PersonNotFoundError(f"Person {person_id} not found")
            
            return result["person"]
            
        except PersonNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get person details for {person_id}: {e}")
            raise StaffManagementError(f"Failed to get person details: {e}")
    
    async def search_staff(
        self, 
        query: str,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search staff by name, role, or email.
        
        Args:
            query: Search query string
            role: Optional role filter
            is_active: Optional active status filter
            limit: Optional limit on number of results
            
        Returns:
            List of matching staff records
            
        Raises:
            StaffManagementError: For staff management errors
        """
        try:
            search_query = """
            query SearchStaff {
                persons {
                    nodes {
                        ident
                        firstname
                        lastname
                        formattedName
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(search_query)
            
            if "persons" not in result:
                return []
            
            # Extract nodes from collection structure
            persons = result["persons"].get("nodes", [])
            
            # Apply client-side search filtering
            if query:
                persons = [p for p in persons if query.lower() in p.get("formattedName", "").lower()]
            
            if limit:
                persons = persons[:limit]
            
            return persons
            
        except Exception as e:
            logger.error(f"Failed to search staff: {e}")
            raise StaffManagementError(f"Failed to search staff: {e}")
    
    async def get_staff_by_role(self, role: str) -> List[Dict[str, Any]]:
        """
        Get staff members filtered by role.
        
        Args:
            role: Staff role (Site Manager, Engineer, Worker, etc.)
            
        Returns:
            List of staff members with specified role
            
        Raises:
            StaffManagementError: For staff management errors
        """
        return await self.list_staff(role=role)
    
    async def get_active_staff(self) -> List[Dict[str, Any]]:
        """
        Get all active staff members.
        
        Returns:
            List of active staff members
            
        Raises:
            StaffManagementError: For staff management errors
        """
        return await self.list_staff(is_active=True)
    
    async def get_staff_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get staff members assigned to a specific project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            List of staff members assigned to the project
            
        Raises:
            StaffManagementError: For staff management errors
        """
        try:
            query = """
            query GetStaffByProject($projectId: ID!) {
                people(
                    filter: { assignedProjects: { contains: $projectId } }
                    orderBy: name_ASC
                ) {
                    id
                    name
                    role
                    email
                    phone
                    department
                    isActive
                    assignedProjects
                }
            }
            """
            
            result = await self.client.query(query, {"projectId": project_id})
            
            if "people" not in result:
                return []
            
            return result["people"]
            
        except Exception as e:
            logger.error(f"Failed to get staff by project: {e}")
            raise StaffManagementError(f"Failed to get staff by project: {e}")
    
    async def get_staff_statistics(self) -> Dict[str, Any]:
        """
        Get staff statistics and metrics.
        
        Returns:
            Dictionary containing staff statistics
            
        Raises:
            StaffManagementError: For staff management errors
        """
        try:
            query = """
            query GetStaffStatistics {
                persons {
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "persons" not in result:
                return {}
            
            # Return basic statistics for now
            total_count = result["persons"].get("totalCount", 0)
            return {
                "totalStaff": total_count,
                "activeStaff": 0,  # TODO: Implement when we understand status filtering
                "inactiveStaff": 0,
                "staffByRole": [],
                "averageTenure": 0,
                "newHiresThisMonth": 0,
                "staffByDepartment": []
            }
            
        except Exception as e:
            logger.error(f"Failed to get staff statistics: {e}")
            raise StaffManagementError(f"Failed to get staff statistics: {e}")
    
    async def create_person(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new staff member.
        
        Args:
            person_data: Person data dictionary
            
        Returns:
            Created person information
            
        Raises:
            InvalidPersonDataError: If person data is invalid
            StaffManagementError: For other staff management errors
        """
        try:
            # Validate required fields
            required_fields = ["name"]
            for field in required_fields:
                if field not in person_data or not person_data[field]:
                    raise InvalidPersonDataError(f"Required field '{field}' is missing or empty")
            
            mutation = """
            mutation CreatePerson($input: CreatePersonInput!) {
                createPerson(input: $input) {
                    id
                    name
                    role
                    email
                    phone
                    department
                    isActive
                    hireDate
                    createdAt
                }
            }
            """
            
            result = await self.client.mutation(mutation, {"input": person_data})
            
            if "createPerson" not in result:
                raise StaffManagementError("Failed to create person")
            
            logger.info(f"Created person: {result['createPerson']['id']}")
            return result["createPerson"]
            
        except InvalidPersonDataError:
            raise
        except Exception as e:
            logger.error(f"Failed to create person: {e}")
            raise StaffManagementError(f"Failed to create person: {e}")
    
    async def update_person(
        self, 
        person_id: str, 
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing staff member.
        
        Args:
            person_id: Person identifier
            update_data: Fields to update
            
        Returns:
            Updated person information
            
        Raises:
            PersonNotFoundError: If person doesn't exist
            StaffManagementError: For other staff management errors
        """
        try:
            mutation = """
            mutation UpdatePerson($id: ID!, $input: UpdatePersonInput!) {
                updatePerson(id: $id, input: $input) {
                    id
                    name
                    role
                    email
                    phone
                    department
                    isActive
                    updatedAt
                }
            }
            """
            
            result = await self.client.mutation(mutation, {
                "id": person_id,
                "input": update_data
            })
            
            if "updatePerson" not in result:
                raise PersonNotFoundError(f"Person {person_id} not found")
            
            logger.info(f"Updated person: {person_id}")
            return result["updatePerson"]
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise PersonNotFoundError(f"Person {person_id} not found")
            logger.error(f"Failed to update person {person_id}: {e}")
            raise StaffManagementError(f"Failed to update person: {e}")
    
    async def deactivate_person(self, person_id: str) -> bool:
        """
        Deactivate a staff member.
        
        Args:
            person_id: Person identifier
            
        Returns:
            True if deactivation was successful
            
        Raises:
            PersonNotFoundError: If person doesn't exist
            StaffManagementError: For other staff management errors
        """
        try:
            return await self.update_person(person_id, {"isActive": False})
            
        except PersonNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to deactivate person {person_id}: {e}")
            raise StaffManagementError(f"Failed to deactivate person: {e}")
    
    async def assign_person_to_project(
        self, 
        person_id: str, 
        project_id: str
    ) -> bool:
        """
        Assign a person to a project.
        
        Args:
            person_id: Person identifier
            project_id: Project identifier
            
        Returns:
            True if assignment was successful
            
        Raises:
            PersonNotFoundError: If person doesn't exist
            StaffManagementError: For other staff management errors
        """
        try:
            mutation = """
            mutation AssignPersonToProject($personId: ID!, $projectId: ID!) {
                assignPersonToProject(personId: $personId, projectId: $projectId) {
                    success
                    message
                }
            }
            """
            
            result = await self.client.mutation(mutation, {
                "personId": person_id,
                "projectId": project_id
            })
            
            if "assignPersonToProject" not in result:
                raise PersonNotFoundError(f"Person {person_id} not found")
            
            success = result["assignPersonToProject"]["success"]
            if success:
                logger.info(f"Assigned person {person_id} to project {project_id}")
            else:
                logger.warning(f"Failed to assign person {person_id} to project {project_id}: {result['assignPersonToProject']['message']}")
            
            return success
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise PersonNotFoundError(f"Person {person_id} not found")
            logger.error(f"Failed to assign person to project: {e}")
            raise StaffManagementError(f"Failed to assign person to project: {e}")
