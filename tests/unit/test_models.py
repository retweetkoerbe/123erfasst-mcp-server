"""
Unit tests for data models library.

Follows Article III: Test-First Imperative - Tests written before implementation.
"""
import pytest
from datetime import datetime, date
from decimal import Decimal
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "libraries"))

from models import Project, StaffTime, Person, Equipment, Ticket, Planning, ModelFactory


class TestProject:
    """Test cases for Project model."""
    
    def test_project_creation_with_valid_data(self):
        """Test creating project with valid data."""
        project = Project(
            id="proj-123",
            name="Test Construction Project",
            status="active",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            description="A test construction project"
        )
        assert project.id == "proj-123"
        assert project.name == "Test Construction Project"
        assert project.status == "active"
    
    def test_project_creation_with_minimal_data(self):
        """Test creating project with minimal required data."""
        project = Project(
            id="proj-456",
            name="Minimal Project"
        )
        assert project.id == "proj-456"
        assert project.name == "Minimal Project"
        assert project.status is None
        assert project.start_date is None
    
    def test_project_validation_fails_without_id(self):
        """Test that project creation fails without ID."""
        with pytest.raises(ValueError):
            Project(name="Test Project")
    
    def test_project_validation_fails_without_name(self):
        """Test that project creation fails without name."""
        with pytest.raises(ValueError):
            Project(id="proj-123")


class TestStaffTime:
    """Test cases for StaffTime model."""
    
    def test_staff_time_creation_with_valid_data(self):
        """Test creating staff time with valid data."""
        start_time = datetime(2024, 1, 1, 9, 0, 0)
        end_time = datetime(2024, 1, 1, 17, 0, 0)
        
        staff_time = StaffTime(
            id="time-123",
            project_id="proj-123",
            person_id="person-456",
            start_time=start_time,
            end_time=end_time,
            duration_hours=8.0
        )
        assert staff_time.id == "time-123"
        assert staff_time.project_id == "proj-123"
        assert staff_time.person_id == "person-456"
        assert staff_time.duration_hours == 8.0
    
    def test_staff_time_validation_requires_project_id(self):
        """Test that staff time requires project ID."""
        with pytest.raises(ValueError):
            StaffTime(
                id="time-123",
                person_id="person-456",
                start_time=datetime.now()
            )
    
    def test_staff_time_validation_requires_person_id(self):
        """Test that staff time requires person ID."""
        with pytest.raises(ValueError):
            StaffTime(
                id="time-123",
                project_id="proj-123",
                start_time=datetime.now()
            )


class TestPerson:
    """Test cases for Person model."""
    
    def test_person_creation_with_valid_data(self):
        """Test creating person with valid data."""
        person = Person(
            id="person-123",
            name="John Doe",
            role="Site Manager",
            email="john.doe@example.com",
            phone="+1234567890"
        )
        assert person.id == "person-123"
        assert person.name == "John Doe"
        assert person.role == "Site Manager"
    
    def test_person_creation_with_minimal_data(self):
        """Test creating person with minimal data."""
        person = Person(
            id="person-456",
            name="Jane Smith"
        )
        assert person.id == "person-456"
        assert person.name == "Jane Smith"
        assert person.role is None


class TestEquipment:
    """Test cases for Equipment model."""
    
    def test_equipment_creation_with_valid_data(self):
        """Test creating equipment with valid data."""
        equipment = Equipment(
            id="eq-123",
            name="Excavator EX-001",
            type="Heavy Machinery",
            location="Site A",
            status="operational"
        )
        assert equipment.id == "eq-123"
        assert equipment.name == "Excavator EX-001"
        assert equipment.type == "Heavy Machinery"
        assert equipment.location == "Site A"
        assert equipment.status == "operational"
    
    def test_equipment_validation_requires_id(self):
        """Test that equipment requires ID."""
        with pytest.raises(ValueError):
            Equipment(name="Test Equipment")


class TestTicket:
    """Test cases for Ticket model."""
    
    def test_ticket_creation_with_valid_data(self):
        """Test creating ticket with valid data."""
        ticket = Ticket(
            id="ticket-123",
            title="Safety Issue",
            description="Broken safety railing on level 2",
            status="open",
            priority="high",
            assigned_person_id="person-456"
        )
        assert ticket.id == "ticket-123"
        assert ticket.title == "Safety Issue"
        assert ticket.status == "open"
        assert ticket.priority == "high"
    
    def test_ticket_validation_requires_id(self):
        """Test that ticket requires ID."""
        with pytest.raises(ValueError):
            Ticket(title="Test Ticket")


class TestPlanning:
    """Test cases for Planning model."""
    
    def test_planning_creation_with_valid_data(self):
        """Test creating planning with valid data."""
        planning = Planning(
            id="plan-123",
            project_id="proj-123",
            milestone="Foundation Complete",
            planned_date=date(2024, 2, 15),
            actual_date=date(2024, 2, 14),
            status="completed"
        )
        assert planning.id == "plan-123"
        assert planning.project_id == "proj-123"
        assert planning.milestone == "Foundation Complete"
        assert planning.status == "completed"


class TestModelFactory:
    """Test cases for ModelFactory."""
    
    def test_create_project(self):
        """Test creating project using factory."""
        project = ModelFactory.create_project(
            id="factory-proj-123",
            name="Factory Project"
        )
        assert isinstance(project, Project)
        assert project.id == "factory-proj-123"
        assert project.name == "Factory Project"
    
    def test_create_staff_time(self):
        """Test creating staff time using factory."""
        staff_time = ModelFactory.create_staff_time(
            id="factory-time-123",
            project_id="proj-123",
            person_id="person-456"
        )
        assert isinstance(staff_time, StaffTime)
        assert staff_time.id == "factory-time-123"
        assert staff_time.project_id == "proj-123"
        assert staff_time.person_id == "person-456"
    
    def test_create_person(self):
        """Test creating person using factory."""
        person = ModelFactory.create_person(
            id="factory-person-123",
            name="Factory Person"
        )
        assert isinstance(person, Person)
        assert person.id == "factory-person-123"
        assert person.name == "Factory Person"
    
    def test_create_equipment(self):
        """Test creating equipment using factory."""
        equipment = ModelFactory.create_equipment(
            id="factory-eq-123",
            name="Factory Equipment"
        )
        assert isinstance(equipment, Equipment)
        assert equipment.id == "factory-eq-123"
        assert equipment.name == "Factory Equipment"
    
    def test_create_ticket(self):
        """Test creating ticket using factory."""
        ticket = ModelFactory.create_ticket(
            id="factory-ticket-123",
            title="Factory Ticket"
        )
        assert isinstance(ticket, Ticket)
        assert ticket.id == "factory-ticket-123"
        assert ticket.title == "Factory Ticket"
    
    def test_create_planning(self):
        """Test creating planning using factory."""
        planning = ModelFactory.create_planning(
            id="factory-plan-123",
            project_id="proj-123",
            milestone="Factory Milestone"
        )
        assert isinstance(planning, Planning)
        assert planning.id == "factory-plan-123"
        assert planning.project_id == "proj-123"
        assert planning.milestone == "Factory Milestone"


class TestModelSerialization:
    """Test cases for model serialization."""
    
    def test_project_serialization(self):
        """Test project model serialization."""
        project = Project(
            id="serialize-123",
            name="Serialization Test",
            status="active"
        )
        data = project.model_dump()
        assert data["id"] == "serialize-123"
        assert data["name"] == "Serialization Test"
        assert data["status"] == "active"
    
    def test_project_deserialization(self):
        """Test project model deserialization."""
        data = {
            "id": "deserialize-123",
            "name": "Deserialization Test",
            "status": "active"
        }
        project = Project.model_validate(data)
        assert project.id == "deserialize-123"
        assert project.name == "Deserialization Test"
        assert project.status == "active"
