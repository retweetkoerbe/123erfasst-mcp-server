"""
Unit tests for equipment management library.

Follows Article III: Test-First Imperative - Tests written before implementation.
"""
import pytest
from unittest.mock import Mock, AsyncMock
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "libraries"))

from equipment_management import EquipmentManager, EquipmentManagementError, EquipmentNotFoundError, InvalidEquipmentDataError


class TestEquipmentManager:
    """Test cases for EquipmentManager class."""
    
    def test_init_with_valid_client(self):
        """Test EquipmentManager initialization with valid GraphQL client."""
        mock_client = Mock()
        manager = EquipmentManager(mock_client)
        assert manager.client == mock_client
    
    @pytest.mark.asyncio
    async def test_list_equipment_success(self):
        """Test successful equipment listing."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "type": "Heavy Machinery",
                    "status": "operational",
                    "location": "Site A",
                    "model": "CAT 320",
                    "serialNumber": "CAT320-12345"
                },
                {
                    "id": "eq-456",
                    "name": "Crane CR-001",
                    "type": "Heavy Machinery",
                    "status": "maintenance",
                    "location": "Site B",
                    "model": "Liebherr LTM",
                    "serialNumber": "LTM-67890"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.list_equipment()
        
        assert len(result) == 2
        assert result[0]["id"] == "eq-123"
        assert result[0]["name"] == "Excavator EX-001"
        assert result[0]["status"] == "operational"
        assert result[1]["id"] == "eq-456"
        assert result[1]["status"] == "maintenance"
    
    @pytest.mark.asyncio
    async def test_list_equipment_with_filters(self):
        """Test equipment listing with status filter."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "status": "operational"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.list_equipment(status="operational")
        
        assert len(result) == 1
        assert result[0]["status"] == "operational"
    
    @pytest.mark.asyncio
    async def test_list_equipment_empty(self):
        """Test equipment listing when no equipment exists."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"equipment": []})
        
        manager = EquipmentManager(mock_client)
        result = await manager.list_equipment()
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_equipment_details_success(self):
        """Test successful equipment details retrieval."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": {
                "id": "eq-123",
                "name": "Excavator EX-001",
                "type": "Heavy Machinery",
                "status": "operational",
                "location": "Site A",
                "model": "CAT 320",
                "serialNumber": "CAT320-12345",
                "purchaseDate": "2023-01-15",
                "lastMaintenance": "2024-01-10",
                "nextMaintenance": "2024-04-10",
                "assignedProjectId": "proj-123",
                "assignedPersonId": "person-456"
            }
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.get_equipment_details("eq-123")
        
        assert result["id"] == "eq-123"
        assert result["name"] == "Excavator EX-001"
        assert result["status"] == "operational"
        assert result["model"] == "CAT 320"
    
    @pytest.mark.asyncio
    async def test_get_equipment_details_not_found(self):
        """Test equipment details retrieval when equipment doesn't exist."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"equipment": None})
        
        manager = EquipmentManager(mock_client)
        
        with pytest.raises(EquipmentNotFoundError):
            await manager.get_equipment_details("invalid-eq")
    
    @pytest.mark.asyncio
    async def test_search_equipment_by_name(self):
        """Test searching equipment by name."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "type": "Heavy Machinery",
                    "status": "operational"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.search_equipment(query="Excavator")
        
        assert len(result) == 1
        assert "Excavator" in result[0]["name"]
    
    @pytest.mark.asyncio
    async def test_search_equipment_by_type(self):
        """Test searching equipment by type."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "type": "Heavy Machinery",
                    "status": "operational"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.search_equipment(query="Heavy Machinery")
        
        assert len(result) == 1
        assert result[0]["type"] == "Heavy Machinery"
    
    @pytest.mark.asyncio
    async def test_search_equipment_empty(self):
        """Test searching equipment when no matches found."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"equipment": []})
        
        manager = EquipmentManager(mock_client)
        result = await manager.search_equipment(query="NonExistent")
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_equipment_by_status(self):
        """Test getting equipment filtered by status."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "status": "operational"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.get_equipment_by_status("operational")
        
        assert len(result) == 1
        assert result[0]["status"] == "operational"
    
    @pytest.mark.asyncio
    async def test_get_equipment_by_type(self):
        """Test getting equipment filtered by type."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "type": "Heavy Machinery"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.get_equipment_by_type("Heavy Machinery")
        
        assert len(result) == 1
        assert result[0]["type"] == "Heavy Machinery"
    
    @pytest.mark.asyncio
    async def test_get_equipment_by_location(self):
        """Test getting equipment filtered by location."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "location": "Site A"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.get_equipment_by_location("Site A")
        
        assert len(result) == 1
        assert result[0]["location"] == "Site A"
    
    @pytest.mark.asyncio
    async def test_get_equipment_statistics(self):
        """Test getting equipment statistics."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipmentStats": {
                "totalEquipment": 25,
                "operationalEquipment": 20,
                "maintenanceEquipment": 3,
                "outOfServiceEquipment": 2,
                "equipmentByType": [
                    {"type": "Heavy Machinery", "count": 15},
                    {"type": "Tools", "count": 10}
                ],
                "equipmentByStatus": [
                    {"status": "operational", "count": 20},
                    {"status": "maintenance", "count": 3},
                    {"status": "out_of_service", "count": 2}
                ]
            }
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.get_equipment_statistics()
        
        assert result["totalEquipment"] == 25
        assert result["operationalEquipment"] == 20
        assert result["maintenanceEquipment"] == 3
        assert result["outOfServiceEquipment"] == 2
    
    @pytest.mark.asyncio
    async def test_create_equipment_success(self):
        """Test successful equipment creation."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "createEquipment": {
                "id": "eq-new-123",
                "name": "New Excavator",
                "type": "Heavy Machinery",
                "status": "operational"
            }
        })
        
        manager = EquipmentManager(mock_client)
        equipment_data = {
            "name": "New Excavator",
            "type": "Heavy Machinery",
            "status": "operational",
            "model": "CAT 320",
            "serialNumber": "CAT320-NEW"
        }
        
        result = await manager.create_equipment(equipment_data)
        
        assert result["id"] == "eq-new-123"
        assert result["name"] == "New Excavator"
        assert result["type"] == "Heavy Machinery"
    
    @pytest.mark.asyncio
    async def test_create_equipment_invalid_data(self):
        """Test equipment creation with invalid data."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(side_effect=Exception("Invalid equipment data"))
        
        manager = EquipmentManager(mock_client)
        equipment_data = {"name": ""}  # Invalid: empty name
        
        with pytest.raises(InvalidEquipmentDataError):
            await manager.create_equipment(equipment_data)
    
    @pytest.mark.asyncio
    async def test_update_equipment_success(self):
        """Test successful equipment update."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "updateEquipment": {
                "id": "eq-123",
                "name": "Updated Excavator",
                "status": "maintenance"
            }
        })
        
        manager = EquipmentManager(mock_client)
        update_data = {
            "name": "Updated Excavator",
            "status": "maintenance"
        }
        
        result = await manager.update_equipment("eq-123", update_data)
        
        assert result["id"] == "eq-123"
        assert result["name"] == "Updated Excavator"
        assert result["status"] == "maintenance"
    
    @pytest.mark.asyncio
    async def test_update_equipment_not_found(self):
        """Test equipment update when equipment doesn't exist."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(side_effect=Exception("Equipment not found"))
        
        manager = EquipmentManager(mock_client)
        update_data = {"name": "Updated Name"}
        
        with pytest.raises(EquipmentNotFoundError):
            await manager.update_equipment("invalid-eq", update_data)
    
    @pytest.mark.asyncio
    async def test_assign_equipment_to_project(self):
        """Test assigning equipment to a project."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "assignEquipmentToProject": {
                "success": True,
                "message": "Equipment assigned successfully"
            }
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.assign_equipment_to_project("eq-123", "proj-456")
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_assign_equipment_to_person(self):
        """Test assigning equipment to a person."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "assignEquipmentToPerson": {
                "success": True,
                "message": "Equipment assigned successfully"
            }
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.assign_equipment_to_person("eq-123", "person-456")
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_get_equipment_by_project(self):
        """Test getting equipment assigned to a specific project."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "assignedProjectId": "proj-123"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.get_equipment_by_project("proj-123")
        
        assert len(result) == 1
        assert result[0]["assignedProjectId"] == "proj-123"
    
    @pytest.mark.asyncio
    async def test_get_equipment_by_person(self):
        """Test getting equipment assigned to a specific person."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "equipment": [
                {
                    "id": "eq-123",
                    "name": "Excavator EX-001",
                    "assignedPersonId": "person-123"
                }
            ]
        })
        
        manager = EquipmentManager(mock_client)
        result = await manager.get_equipment_by_person("person-123")
        
        assert len(result) == 1
        assert result[0]["assignedPersonId"] == "person-123"
