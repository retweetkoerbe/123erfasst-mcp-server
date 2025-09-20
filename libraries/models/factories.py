"""
Model factories for creating test data.

Follows Article III.2: Test Categories - Factory methods for test data generation.
"""
from datetime import datetime, date
from .project import Project
from .staff_time import StaffTime
from .person import Person
from .equipment import Equipment
from .ticket import Ticket
from .planning import Planning


class ModelFactory:
    """
    Factory class for creating model instances with test data.
    
    Provides methods to create realistic test data for all model types.
    """
    
    @staticmethod
    def create_project(
        id: str,
        name: str,
        status: str = "active",
        start_date: date = None,
        end_date: date = None,
        **kwargs
    ) -> Project:
        """Create a Project instance with test data."""
        return Project(
            id=id,
            name=name,
            status=status,
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )
    
    @staticmethod
    def create_staff_time(
        id: str,
        project_id: str,
        person_id: str,
        start_time: datetime = None,
        end_time: datetime = None,
        **kwargs
    ) -> StaffTime:
        """Create a StaffTime instance with test data."""
        return StaffTime(
            id=id,
            project_id=project_id,
            person_id=person_id,
            start_time=start_time,
            end_time=end_time,
            **kwargs
        )
    
    @staticmethod
    def create_person(
        id: str,
        name: str,
        role: str = None,
        email: str = None,
        **kwargs
    ) -> Person:
        """Create a Person instance with test data."""
        return Person(
            id=id,
            name=name,
            role=role,
            email=email,
            **kwargs
        )
    
    @staticmethod
    def create_equipment(
        id: str,
        name: str,
        type: str = None,
        location: str = None,
        status: str = "operational",
        **kwargs
    ) -> Equipment:
        """Create an Equipment instance with test data."""
        return Equipment(
            id=id,
            name=name,
            type=type,
            location=location,
            status=status,
            **kwargs
        )
    
    @staticmethod
    def create_ticket(
        id: str,
        title: str,
        description: str = None,
        status: str = "open",
        priority: str = "medium",
        **kwargs
    ) -> Ticket:
        """Create a Ticket instance with test data."""
        return Ticket(
            id=id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            **kwargs
        )
    
    @staticmethod
    def create_planning(
        id: str,
        project_id: str,
        milestone: str = None,
        planned_date: date = None,
        status: str = "planned",
        **kwargs
    ) -> Planning:
        """Create a Planning instance with test data."""
        return Planning(
            id=id,
            project_id=project_id,
            milestone=milestone,
            planned_date=planned_date,
            status=status,
            **kwargs
        )
    
    @staticmethod
    def create_sample_project_data() -> dict:
        """Create sample project data for testing."""
        return {
            "id": "sample-proj-123",
            "name": "Sample Construction Project",
            "status": "active",
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31),
            "description": "A sample construction project for testing",
            "client_name": "Test Client Inc.",
            "budget": 1000000.0,
            "location": "123 Test Street, Test City"
        }
    
    @staticmethod
    def create_sample_staff_time_data() -> dict:
        """Create sample staff time data for testing."""
        return {
            "id": "sample-time-123",
            "project_id": "sample-proj-123",
            "person_id": "sample-person-456",
            "start_time": datetime(2024, 1, 15, 9, 0, 0),
            "end_time": datetime(2024, 1, 15, 17, 0, 0),
            "duration_hours": 8.0,
            "description": "Foundation work",
            "is_active": False
        }
    
    @staticmethod
    def create_sample_person_data() -> dict:
        """Create sample person data for testing."""
        return {
            "id": "sample-person-456",
            "name": "John Doe",
            "role": "Site Manager",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "department": "Construction",
            "is_active": True
        }
    
    @staticmethod
    def create_sample_equipment_data() -> dict:
        """Create sample equipment data for testing."""
        return {
            "id": "sample-eq-789",
            "name": "Excavator EX-001",
            "type": "Heavy Machinery",
            "location": "Site A",
            "status": "operational",
            "model": "CAT 320",
            "serial_number": "CAT320-12345"
        }
    
    @staticmethod
    def create_sample_ticket_data() -> dict:
        """Create sample ticket data for testing."""
        return {
            "id": "sample-ticket-101",
            "title": "Safety Issue - Broken Railing",
            "description": "Safety railing on level 2 is broken and needs immediate repair",
            "status": "open",
            "priority": "high",
            "category": "safety",
            "project_id": "sample-proj-123",
            "assigned_person_id": "sample-person-456"
        }
    
    @staticmethod
    def create_sample_planning_data() -> dict:
        """Create sample planning data for testing."""
        return {
            "id": "sample-plan-202",
            "project_id": "sample-proj-123",
            "milestone": "Foundation Complete",
            "planned_date": date(2024, 2, 15),
            "actual_date": date(2024, 2, 14),
            "status": "completed",
            "description": "Complete foundation work including excavation and concrete pouring",
            "estimated_hours": 40.0,
            "actual_hours": 38.5,
            "priority": "high"
        }
