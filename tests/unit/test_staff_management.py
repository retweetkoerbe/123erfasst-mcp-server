"""
Unit tests for staff management library.

Follows Article III: Test-First Imperative - Tests written before implementation.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "libraries"))

from staff_management import StaffManager, StaffManagementError, PersonNotFoundError, InvalidPersonDataError


class TestStaffManager:
    """Test cases for StaffManager class."""
    
    def test_init_with_valid_client(self):
        """Test StaffManager initialization with valid GraphQL client."""
        mock_client = Mock()
        manager = StaffManager(mock_client)
        assert manager.client == mock_client
    
    @pytest.mark.asyncio
    async def test_list_staff_success(self):
        """Test successful staff listing."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "people": [
                {
                    "id": "person-123",
                    "name": "John Doe",
                    "role": "Site Manager",
                    "email": "john.doe@example.com",
                    "phone": "+1234567890",
                    "isActive": True
                },
                {
                    "id": "person-456",
                    "name": "Jane Smith",
                    "role": "Engineer",
                    "email": "jane.smith@example.com",
                    "phone": "+0987654321",
                    "isActive": True
                }
            ]
        })
        
        manager = StaffManager(mock_client)
        result = await manager.list_staff()
        
        assert len(result) == 2
        assert result[0]["id"] == "person-123"
        assert result[0]["name"] == "John Doe"
        assert result[0]["role"] == "Site Manager"
        assert result[1]["id"] == "person-456"
        assert result[1]["name"] == "Jane Smith"
    
    @pytest.mark.asyncio
    async def test_list_staff_with_filters(self):
        """Test staff listing with role filter."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "people": [
                {
                    "id": "person-123",
                    "name": "John Doe",
                    "role": "Site Manager",
                    "isActive": True
                }
            ]
        })
        
        manager = StaffManager(mock_client)
        result = await manager.list_staff(role="Site Manager")
        
        assert len(result) == 1
        assert result[0]["role"] == "Site Manager"
    
    @pytest.mark.asyncio
    async def test_list_staff_empty(self):
        """Test staff listing when no staff exist."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"people": []})
        
        manager = StaffManager(mock_client)
        result = await manager.list_staff()
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_person_details_success(self):
        """Test successful person details retrieval."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "person": {
                "id": "person-123",
                "name": "John Doe",
                "role": "Site Manager",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "department": "Construction",
                "isActive": True,
                "hireDate": "2023-01-15",
                "skills": ["Project Management", "Safety Training"]
            }
        })
        
        manager = StaffManager(mock_client)
        result = await manager.get_person_details("person-123")
        
        assert result["id"] == "person-123"
        assert result["name"] == "John Doe"
        assert result["role"] == "Site Manager"
        assert result["email"] == "john.doe@example.com"
        assert result["isActive"] is True
    
    @pytest.mark.asyncio
    async def test_get_person_details_not_found(self):
        """Test person details retrieval when person doesn't exist."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"person": None})
        
        manager = StaffManager(mock_client)
        
        with pytest.raises(PersonNotFoundError):
            await manager.get_person_details("invalid-person")
    
    @pytest.mark.asyncio
    async def test_search_staff_by_name(self):
        """Test searching staff by name."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "people": [
                {
                    "id": "person-123",
                    "name": "John Doe",
                    "role": "Site Manager",
                    "isActive": True
                }
            ]
        })
        
        manager = StaffManager(mock_client)
        result = await manager.search_staff(query="John")
        
        assert len(result) == 1
        assert "John" in result[0]["name"]
    
    @pytest.mark.asyncio
    async def test_search_staff_by_role(self):
        """Test searching staff by role."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "people": [
                {
                    "id": "person-123",
                    "name": "John Doe",
                    "role": "Site Manager",
                    "isActive": True
                }
            ]
        })
        
        manager = StaffManager(mock_client)
        result = await manager.search_staff(query="Site Manager")
        
        assert len(result) == 1
        assert result[0]["role"] == "Site Manager"
    
    @pytest.mark.asyncio
    async def test_search_staff_empty(self):
        """Test searching staff when no matches found."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"people": []})
        
        manager = StaffManager(mock_client)
        result = await manager.search_staff(query="NonExistent")
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_staff_by_role(self):
        """Test getting staff filtered by role."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "people": [
                {
                    "id": "person-123",
                    "name": "John Doe",
                    "role": "Site Manager",
                    "isActive": True
                }
            ]
        })
        
        manager = StaffManager(mock_client)
        result = await manager.get_staff_by_role("Site Manager")
        
        assert len(result) == 1
        assert result[0]["role"] == "Site Manager"
    
    @pytest.mark.asyncio
    async def test_get_active_staff(self):
        """Test getting active staff members."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "people": [
                {
                    "id": "person-123",
                    "name": "John Doe",
                    "role": "Site Manager",
                    "isActive": True
                }
            ]
        })
        
        manager = StaffManager(mock_client)
        result = await manager.get_active_staff()
        
        assert len(result) == 1
        assert result[0]["isActive"] is True
    
    @pytest.mark.asyncio
    async def test_get_staff_statistics(self):
        """Test getting staff statistics."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "staffStats": {
                "totalStaff": 25,
                "activeStaff": 20,
                "inactiveStaff": 5,
                "staffByRole": [
                    {"role": "Site Manager", "count": 3},
                    {"role": "Engineer", "count": 8},
                    {"role": "Worker", "count": 9}
                ],
                "averageTenure": 2.5
            }
        })
        
        manager = StaffManager(mock_client)
        result = await manager.get_staff_statistics()
        
        assert result["totalStaff"] == 25
        assert result["activeStaff"] == 20
        assert result["inactiveStaff"] == 5
        assert result["averageTenure"] == 2.5
    
    @pytest.mark.asyncio
    async def test_create_person_success(self):
        """Test successful person creation."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "createPerson": {
                "id": "person-new-123",
                "name": "New Person",
                "role": "Engineer",
                "email": "new.person@example.com",
                "isActive": True
            }
        })
        
        manager = StaffManager(mock_client)
        person_data = {
            "name": "New Person",
            "role": "Engineer",
            "email": "new.person@example.com",
            "phone": "+1234567890"
        }
        
        result = await manager.create_person(person_data)
        
        assert result["id"] == "person-new-123"
        assert result["name"] == "New Person"
        assert result["role"] == "Engineer"
    
    @pytest.mark.asyncio
    async def test_create_person_invalid_data(self):
        """Test person creation with invalid data."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(side_effect=Exception("Invalid person data"))
        
        manager = StaffManager(mock_client)
        person_data = {"name": ""}  # Invalid: empty name
        
        with pytest.raises(InvalidPersonDataError):
            await manager.create_person(person_data)
    
    @pytest.mark.asyncio
    async def test_update_person_success(self):
        """Test successful person update."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "updatePerson": {
                "id": "person-123",
                "name": "Updated Name",
                "role": "Senior Engineer"
            }
        })
        
        manager = StaffManager(mock_client)
        update_data = {
            "name": "Updated Name",
            "role": "Senior Engineer"
        }
        
        result = await manager.update_person("person-123", update_data)
        
        assert result["id"] == "person-123"
        assert result["name"] == "Updated Name"
        assert result["role"] == "Senior Engineer"
    
    @pytest.mark.asyncio
    async def test_update_person_not_found(self):
        """Test person update when person doesn't exist."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(side_effect=Exception("Person not found"))
        
        manager = StaffManager(mock_client)
        update_data = {"name": "Updated Name"}
        
        with pytest.raises(PersonNotFoundError):
            await manager.update_person("invalid-person", update_data)
    
    @pytest.mark.asyncio
    async def test_get_staff_by_project(self):
        """Test getting staff assigned to a specific project."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "people": [
                {
                    "id": "person-123",
                    "name": "John Doe",
                    "role": "Site Manager",
                    "assignedProjects": ["proj-123"]
                }
            ]
        })
        
        manager = StaffManager(mock_client)
        result = await manager.get_staff_by_project("proj-123")
        
        assert len(result) == 1
        assert result[0]["id"] == "person-123"
        assert "proj-123" in result[0]["assignedProjects"]
