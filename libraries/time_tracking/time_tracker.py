"""
Time tracking functionality for construction projects.

Follows Article I: Library-First Principle - Standalone library for time tracking.
Follows Article V: Error Handling and Resilience - Comprehensive error handling.
"""
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from .exceptions import TimeTrackingError, InvalidProjectError, TimeTrackingActiveError, TimeTrackingNotActiveError

logger = logging.getLogger(__name__)


class TimeTracker:
    """
    Time tracking manager for construction projects.
    
    Provides functionality to start, stop, and query time tracking records.
    Follows Article VIII: Anti-Abstraction Principle - Use framework directly.
    """
    
    def __init__(self, graphql_client):
        """
        Initialize time tracker with GraphQL client.
        
        Args:
            graphql_client: GraphQL client instance for API communication
        """
        self.client = graphql_client
        self.active_tracking: Optional[str] = None
        
        logger.info("TimeTracker initialized")
    
    async def start_time_tracking(self, project_id: str, person_id: str, description: str = None) -> Dict[str, Any]:
        """
        Start time tracking for a project and person.
        
        Args:
            project_id: Project identifier
            person_id: Person identifier
            description: Optional work description
            
        Returns:
            Time tracking record data
            
        Raises:
            TimeTrackingActiveError: If time tracking is already active
            InvalidProjectError: If project ID is invalid
            TimeTrackingError: For other time tracking errors
        """
        if self.active_tracking:
            raise TimeTrackingActiveError("Time tracking is already active. Stop current tracking first.")
        
        try:
            # GraphQL mutation to create time tracking record
            mutation = """
            mutation CreateStaffTime($projectId: ID!, $personId: ID!, $description: String) {
                createStaffTime(input: {
                    projectId: $projectId
                    personId: $personId
                    description: $description
                    startTime: $startTime
                    isActive: true
                }) {
                    id
                    projectId
                    personId
                    startTime
                    isActive
                }
            }
            """
            
            variables = {
                "projectId": project_id,
                "personId": person_id,
                "description": description,
                "startTime": datetime.now().isoformat()
            }
            
            result = await self.client.mutation(mutation, variables)
            
            if "createStaffTime" not in result:
                raise TimeTrackingError("Failed to create time tracking record")
            
            time_record = result["createStaffTime"]
            self.active_tracking = time_record["id"]
            
            logger.info(f"Started time tracking for project {project_id}, person {person_id}")
            return time_record
            
        except Exception as e:
            if "Project not found" in str(e) or "Invalid project" in str(e):
                raise InvalidProjectError(f"Project {project_id} not found or invalid")
            raise TimeTrackingError(f"Failed to start time tracking: {e}")
    
    async def stop_time_tracking(self) -> Dict[str, Any]:
        """
        Stop the currently active time tracking.
        
        Returns:
            Updated time tracking record data
            
        Raises:
            TimeTrackingNotActiveError: If no time tracking is active
            TimeTrackingError: For other time tracking errors
        """
        if not self.active_tracking:
            raise TimeTrackingNotActiveError("No active time tracking to stop")
        
        try:
            # GraphQL mutation to update time tracking record
            mutation = """
            mutation UpdateStaffTime($id: ID!, $endTime: String!) {
                updateStaffTime(id: $id, input: {
                    endTime: $endTime
                    isActive: false
                }) {
                    id
                    endTime
                    durationHours
                    isActive
                }
            }
            """
            
            variables = {
                "id": self.active_tracking,
                "endTime": datetime.now().isoformat()
            }
            
            result = await self.client.mutation(mutation, variables)
            
            if "updateStaffTime" not in result:
                raise TimeTrackingError("Failed to update time tracking record")
            
            time_record = result["updateStaffTime"]
            self.active_tracking = None
            
            logger.info(f"Stopped time tracking record {time_record['id']}")
            return time_record
            
        except Exception as e:
            raise TimeTrackingError(f"Failed to stop time tracking: {e}")
    
    async def get_current_times(self, project_id: str = None, person_id: str = None) -> List[Dict[str, Any]]:
        """
        Get currently active time tracking records.
        
        Args:
            project_id: Optional project filter
            person_id: Optional person filter
            
        Returns:
            List of active time tracking records
        """
        try:
            # Build GraphQL query with correct schema
            query = """
            query GetCurrentStaffTimes {
                times {
                    nodes {
                        ident
                        person {
                            firstname
                            lastname
                            formattedName
                        }
                        project {
                            name
                        }
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "times" not in result:
                return []
            
            # Extract nodes from collection structure
            times = result["times"].get("nodes", [])
            
            # For now, return all times since we don't have active filtering
            # TODO: Implement proper active filtering when we understand the schema
            return times
            
        except Exception as e:
            logger.error(f"Failed to get current times: {e}")
            raise TimeTrackingError(f"Failed to get current times: {e}")
    
    async def get_time_tracking_history(
        self, 
        project_id: str = None, 
        person_id: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get time tracking history with optional filters.
        
        Args:
            project_id: Optional project filter
            person_id: Optional person filter
            start_date: Optional start date filter (ISO format)
            end_date: Optional end date filter (ISO format)
            
        Returns:
            List of time tracking records
        """
        try:
            # Build GraphQL query with correct schema
            query = """
            query GetStaffTimeHistory {
                times {
                    nodes {
                        ident
                        person {
                            firstname
                            lastname
                            formattedName
                        }
                        project {
                            name
                        }
                    }
                    totalCount
                }
            }
            """
            
            result = await self.client.query(query)
            
            if "times" not in result:
                return []
            
            # Extract nodes from collection structure
            times = result["times"].get("nodes", [])
            
            # For now, return all times since we don't have date filtering
            # TODO: Implement proper date filtering when we understand the schema
            return times
            
        except Exception as e:
            logger.error(f"Failed to get time tracking history: {e}")
            raise TimeTrackingError(f"Failed to get time tracking history: {e}")
    
    def is_tracking_active(self) -> bool:
        """
        Check if time tracking is currently active.
        
        Returns:
            True if time tracking is active, False otherwise
        """
        return self.active_tracking is not None
    
    def get_active_tracking_id(self) -> Optional[str]:
        """
        Get the ID of the currently active time tracking record.
        
        Returns:
            Active tracking ID or None if not tracking
        """
        return self.active_tracking
