"""
Unit tests for project management library.

Follows Article III: Test-First Imperative - Tests written before implementation.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "libraries"))

from project_management import ProjectManager, ProjectManagementError, ProjectNotFoundError, InvalidProjectDataError


class TestProjectManager:
    """Test cases for ProjectManager class."""
    
    def test_init_with_valid_client(self):
        """Test ProjectManager initialization with valid GraphQL client."""
        mock_client = Mock()
        manager = ProjectManager(mock_client)
        assert manager.client == mock_client
    
    @pytest.mark.asyncio
    async def test_list_projects_success(self):
        """Test successful project listing."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "projects": [
                {
                    "id": "proj-123",
                    "name": "Test Project 1",
                    "status": "active",
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31"
                },
                {
                    "id": "proj-456",
                    "name": "Test Project 2",
                    "status": "completed",
                    "startDate": "2023-01-01",
                    "endDate": "2023-12-31"
                }
            ]
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.list_projects()
        
        assert len(result) == 2
        assert result[0]["id"] == "proj-123"
        assert result[0]["name"] == "Test Project 1"
        assert result[1]["id"] == "proj-456"
        assert result[1]["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_list_projects_with_filters(self):
        """Test project listing with status filter."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "projects": [
                {
                    "id": "proj-123",
                    "name": "Active Project",
                    "status": "active"
                }
            ]
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.list_projects(status="active")
        
        assert len(result) == 1
        assert result[0]["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_list_projects_empty(self):
        """Test project listing when no projects exist."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"projects": []})
        
        manager = ProjectManager(mock_client)
        result = await manager.list_projects()
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_project_details_success(self):
        """Test successful project details retrieval."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "project": {
                "id": "proj-123",
                "name": "Test Project",
                "status": "active",
                "startDate": "2024-01-01",
                "endDate": "2024-12-31",
                "description": "A test construction project",
                "clientName": "Test Client Inc.",
                "budget": 1000000.0,
                "location": "123 Test Street"
            }
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.get_project_details("proj-123")
        
        assert result["id"] == "proj-123"
        assert result["name"] == "Test Project"
        assert result["status"] == "active"
        assert result["budget"] == 1000000.0
    
    @pytest.mark.asyncio
    async def test_get_project_details_not_found(self):
        """Test project details retrieval when project doesn't exist."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"project": None})
        
        manager = ProjectManager(mock_client)
        
        with pytest.raises(ProjectNotFoundError):
            await manager.get_project_details("invalid-proj")
    
    @pytest.mark.asyncio
    async def test_search_projects_by_name(self):
        """Test searching projects by name."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "projects": [
                {
                    "id": "proj-123",
                    "name": "Office Building Project",
                    "status": "active"
                }
            ]
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.search_projects(query="Office Building")
        
        assert len(result) == 1
        assert "Office Building" in result[0]["name"]
    
    @pytest.mark.asyncio
    async def test_search_projects_by_client(self):
        """Test searching projects by client name."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "projects": [
                {
                    "id": "proj-456",
                    "name": "Client Project",
                    "clientName": "ABC Corporation",
                    "status": "active"
                }
            ]
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.search_projects(query="ABC Corporation")
        
        assert len(result) == 1
        assert result[0]["clientName"] == "ABC Corporation"
    
    @pytest.mark.asyncio
    async def test_search_projects_empty(self):
        """Test searching projects when no matches found."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"projects": []})
        
        manager = ProjectManager(mock_client)
        result = await manager.search_projects(query="NonExistent")
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_projects_by_status(self):
        """Test getting projects filtered by status."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "projects": [
                {
                    "id": "proj-123",
                    "name": "Active Project",
                    "status": "active"
                }
            ]
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.get_projects_by_status("active")
        
        assert len(result) == 1
        assert result[0]["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_get_projects_by_date_range(self):
        """Test getting projects filtered by date range."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "projects": [
                {
                    "id": "proj-123",
                    "name": "Project in Range",
                    "startDate": "2024-06-01",
                    "endDate": "2024-08-31"
                }
            ]
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.get_projects_by_date_range("2024-05-01", "2024-09-30")
        
        assert len(result) == 1
        assert result[0]["id"] == "proj-123"
    
    @pytest.mark.asyncio
    async def test_get_project_statistics(self):
        """Test getting project statistics."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "projectStats": {
                "totalProjects": 10,
                "activeProjects": 5,
                "completedProjects": 3,
                "onHoldProjects": 2,
                "totalBudget": 5000000.0,
                "averageProjectDuration": 180.5
            }
        })
        
        manager = ProjectManager(mock_client)
        result = await manager.get_project_statistics()
        
        assert result["totalProjects"] == 10
        assert result["activeProjects"] == 5
        assert result["completedProjects"] == 3
        assert result["totalBudget"] == 5000000.0
    
    @pytest.mark.asyncio
    async def test_create_project_success(self):
        """Test successful project creation."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "createProject": {
                "id": "proj-new-123",
                "name": "New Project",
                "status": "planning",
                "startDate": "2024-01-01",
                "endDate": "2024-12-31"
            }
        })
        
        manager = ProjectManager(mock_client)
        project_data = {
            "name": "New Project",
            "status": "planning",
            "startDate": "2024-01-01",
            "endDate": "2024-12-31",
            "description": "A new construction project"
        }
        
        result = await manager.create_project(project_data)
        
        assert result["id"] == "proj-new-123"
        assert result["name"] == "New Project"
        assert result["status"] == "planning"
    
    @pytest.mark.asyncio
    async def test_create_project_invalid_data(self):
        """Test project creation with invalid data."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(side_effect=Exception("Invalid project data"))
        
        manager = ProjectManager(mock_client)
        project_data = {"name": ""}  # Invalid: empty name
        
        with pytest.raises(InvalidProjectDataError):
            await manager.create_project(project_data)
    
    @pytest.mark.asyncio
    async def test_update_project_success(self):
        """Test successful project update."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "updateProject": {
                "id": "proj-123",
                "name": "Updated Project Name",
                "status": "active"
            }
        })
        
        manager = ProjectManager(mock_client)
        update_data = {
            "name": "Updated Project Name",
            "status": "active"
        }
        
        result = await manager.update_project("proj-123", update_data)
        
        assert result["id"] == "proj-123"
        assert result["name"] == "Updated Project Name"
        assert result["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_update_project_not_found(self):
        """Test project update when project doesn't exist."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(side_effect=Exception("Project not found"))
        
        manager = ProjectManager(mock_client)
        update_data = {"name": "Updated Name"}
        
        with pytest.raises(ProjectNotFoundError):
            await manager.update_project("invalid-proj", update_data)
