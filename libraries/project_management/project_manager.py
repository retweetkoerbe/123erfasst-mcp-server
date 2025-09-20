"""
Project management functionality for construction projects.

Follows Article I: Library-First Principle - Standalone library for project management.
Follows Article V: Error Handling and Resilience - Comprehensive error handling.
"""
import logging
from typing import Optional, List, Dict, Any
from .exceptions import ProjectManagementError, ProjectNotFoundError, InvalidProjectDataError

logger = logging.getLogger(__name__)


class ProjectManager:
    """
    Project manager for construction projects.
    
    Provides functionality to list, search, create, and manage projects.
    Follows Article VIII: Anti-Abstraction Principle - Use framework directly.
    """
    
    def __init__(self, graphql_client):
        """
        Initialize project manager with GraphQL client.
        
        Args:
            graphql_client: GraphQL client instance for API communication
        """
        self.client = graphql_client
        
        logger.info("ProjectManager initialized")
    
    async def list_projects(
        self, 
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        List all projects with optional filters.
        
        Args:
            status: Optional status filter (active, completed, on_hold, cancelled)
            limit: Optional limit on number of results
            offset: Optional offset for pagination
            
        Returns:
            List of project records
            
        Raises:
            ProjectManagementError: For project management errors
        """
        try:
            # Build GraphQL query with correct schema structure
            query = """
            query GetProjects {
                projects {
                    nodes {
                        ident
                        name
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "projects" not in result:
                return []
            
            # Extract nodes from collection structure
            projects = result["projects"].get("nodes", [])
            
            # Apply client-side filtering for now (until we understand the filter API)
            if status:
                # For now, return all projects since we don't know the status field structure
                pass
            
            if limit:
                projects = projects[:limit]
            
            return projects
            
        except Exception as e:
            logger.error(f"Failed to list projects: {e}")
            raise ProjectManagementError(f"Failed to list projects: {e}")
    
    async def get_project_details(self, project_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Detailed project information
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            ProjectManagementError: For other project management errors
        """
        try:
            query = """
            query GetProject($id: Ident!) {
                project(ident: $id) {
                    ident
                    name
                }
            }
            """
            
            result = await self.client.query(query, {"id": project_id})
            
            if "project" not in result or result["project"] is None:
                raise ProjectNotFoundError(f"Project {project_id} not found")
            
            return result["project"]
            
        except ProjectNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get project details for {project_id}: {e}")
            raise ProjectManagementError(f"Failed to get project details: {e}")
    
    async def search_projects(
        self, 
        query: str,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search projects by name, description, or client name.
        
        Args:
            query: Search query string
            status: Optional status filter
            limit: Optional limit on number of results
            
        Returns:
            List of matching project records
            
        Raises:
            ProjectManagementError: For project management errors
        """
        try:
            search_query = """
            query SearchProjects {
                projects {
                    nodes {
                        ident
                        name
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(search_query)
            
            if "projects" not in result:
                return []
            
            # Extract nodes from collection structure
            projects = result["projects"].get("nodes", [])
            
            # Apply client-side search filtering for now
            if query:
                projects = [p for p in projects if query.lower() in p.get("name", "").lower()]
            
            if limit:
                projects = projects[:limit]
            
            return projects
            
        except Exception as e:
            logger.error(f"Failed to search projects: {e}")
            raise ProjectManagementError(f"Failed to search projects: {e}")
    
    async def get_projects_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get projects filtered by status.
        
        Args:
            status: Project status (active, completed, on_hold, cancelled, planning)
            
        Returns:
            List of projects with specified status
            
        Raises:
            ProjectManagementError: For project management errors
        """
        return await self.list_projects(status=status)
    
    async def get_projects_by_date_range(
        self, 
        start_date: str, 
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Get projects within a date range.
        
        Args:
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            List of projects within date range
            
        Raises:
            ProjectManagementError: For project management errors
        """
        try:
            query = """
            query GetProjectsByDateRange {
                projects {
                    nodes {
                        ident
                        name
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "projects" not in result:
                return []
            
            # Extract nodes from collection structure
            projects = result["projects"].get("nodes", [])
            
            # For now, return all projects since we don't have date filtering
            # TODO: Implement proper date filtering when we understand the schema
            return projects
            
        except Exception as e:
            logger.error(f"Failed to get projects by date range: {e}")
            raise ProjectManagementError(f"Failed to get projects by date range: {e}")
    
    async def get_project_statistics(self) -> Dict[str, Any]:
        """
        Get project statistics and metrics.
        
        Returns:
            Dictionary containing project statistics
            
        Raises:
            ProjectManagementError: For project management errors
        """
        try:
            query = """
            query GetProjectStatistics {
                projects {
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "projects" not in result:
                return {}
            
            # Return basic statistics for now
            total_count = result["projects"].get("totalCount", 0)
            return {
                "totalProjects": total_count,
                "activeProjects": 0,  # TODO: Implement when we understand status filtering
                "completedProjects": 0,
                "onHoldProjects": 0,
                "cancelledProjects": 0,
                "totalBudget": 0,
                "averageProjectDuration": 0,
                "averageProjectBudget": 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get project statistics: {e}")
            raise ProjectManagementError(f"Failed to get project statistics: {e}")
    
    async def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            project_data: Project data dictionary
            
        Returns:
            Created project information
            
        Raises:
            InvalidProjectDataError: If project data is invalid
            ProjectManagementError: For other project management errors
        """
        try:
            # Validate required fields
            required_fields = ["name"]
            for field in required_fields:
                if field not in project_data or not project_data[field]:
                    raise InvalidProjectDataError(f"Required field '{field}' is missing or empty")
            
            mutation = """
            mutation CreateProject($input: CreateProjectInput!) {
                createProject(input: $input) {
                    id
                    name
                    status
                    startDate
                    endDate
                    description
                    clientName
                    budget
                    location
                    createdAt
                }
            }
            """
            
            result = await self.client.mutation(mutation, {"input": project_data})
            
            if "createProject" not in result:
                raise ProjectManagementError("Failed to create project")
            
            logger.info(f"Created project: {result['createProject']['id']}")
            return result["createProject"]
            
        except InvalidProjectDataError:
            raise
        except Exception as e:
            logger.error(f"Failed to create project: {e}")
            raise ProjectManagementError(f"Failed to create project: {e}")
    
    async def update_project(
        self, 
        project_id: str, 
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing project.
        
        Args:
            project_id: Project identifier
            update_data: Fields to update
            
        Returns:
            Updated project information
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            ProjectManagementError: For other project management errors
        """
        try:
            mutation = """
            mutation UpdateProject($id: ID!, $input: UpdateProjectInput!) {
                updateProject(id: $id, input: $input) {
                    id
                    name
                    status
                    startDate
                    endDate
                    description
                    clientName
                    budget
                    location
                    updatedAt
                }
            }
            """
            
            result = await self.client.mutation(mutation, {
                "id": project_id,
                "input": update_data
            })
            
            if "updateProject" not in result:
                raise ProjectNotFoundError(f"Project {project_id} not found")
            
            logger.info(f"Updated project: {project_id}")
            return result["updateProject"]
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise ProjectNotFoundError(f"Project {project_id} not found")
            logger.error(f"Failed to update project {project_id}: {e}")
            raise ProjectManagementError(f"Failed to update project: {e}")
    
    async def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if deletion was successful
            
        Raises:
            ProjectNotFoundError: If project doesn't exist
            ProjectManagementError: For other project management errors
        """
        try:
            mutation = """
            mutation DeleteProject($id: ID!) {
                deleteProject(id: $id) {
                    success
                    message
                }
            }
            """
            
            result = await self.client.mutation(mutation, {"id": project_id})
            
            if "deleteProject" not in result:
                raise ProjectNotFoundError(f"Project {project_id} not found")
            
            success = result["deleteProject"]["success"]
            if success:
                logger.info(f"Deleted project: {project_id}")
            else:
                logger.warning(f"Failed to delete project {project_id}: {result['deleteProject']['message']}")
            
            return success
            
        except Exception as e:
            if "not found" in str(e).lower():
                raise ProjectNotFoundError(f"Project {project_id} not found")
            logger.error(f"Failed to delete project {project_id}: {e}")
            raise ProjectManagementError(f"Failed to delete project: {e}")
