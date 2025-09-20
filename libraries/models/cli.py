"""
CLI interface for model validation and testing.

Follows Article II: CLI Interface Mandate - All functionality accessible through CLI.
"""
import json
import logging
import sys
import argparse
from .factories import ModelFactory
from . import Project, StaffTime, Person, Equipment, Ticket, Planning

# Set up logger for CLI
logger = logging.getLogger(__name__)


def validate_sample_data() -> None:
    """Validate all models with sample data."""
    try:
        # Test Project model
        project_data = ModelFactory.create_sample_project_data()
        project = Project.model_validate(project_data)
        logger.info("✅ Project model validation passed")
        
        # Test StaffTime model
        staff_time_data = ModelFactory.create_sample_staff_time_data()
        staff_time = StaffTime.model_validate(staff_time_data)
        logger.info("✅ StaffTime model validation passed")
        
        # Test Person model
        person_data = ModelFactory.create_sample_person_data()
        person = Person.model_validate(person_data)
        logger.info("✅ Person model validation passed")
        
        # Test Equipment model
        equipment_data = ModelFactory.create_sample_equipment_data()
        equipment = Equipment.model_validate(equipment_data)
        logger.info("✅ Equipment model validation passed")
        
        # Test Ticket model
        ticket_data = ModelFactory.create_sample_ticket_data()
        ticket = Ticket.model_validate(ticket_data)
        logger.info("✅ Ticket model validation passed")
        
        # Test Planning model
        planning_data = ModelFactory.create_sample_planning_data()
        planning = Planning.model_validate(planning_data)
        logger.info("✅ Planning model validation passed")
        
        logger.info("\n🎉 All model validations passed successfully!")
        
    except Exception as e:
        logger.info(f"❌ Model validation failed: {e}")
        sys.exit(1)


def validate_json_data(json_file: str) -> None:
    """Validate JSON data against models."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Determine model type based on data structure
        if 'project_id' in data and 'person_id' in data:
            model = StaffTime.model_validate(data)
            logger.info(f"✅ Valid StaffTime data: {model.id}")
        elif 'name' in data and 'type' in data and 'location' in data:
            model = Equipment.model_validate(data)
            logger.info(f"✅ Valid Equipment data: {model.id}")
        elif 'title' in data and 'status' in data:
            model = Ticket.model_validate(data)
            logger.info(f"✅ Valid Ticket data: {model.id}")
        elif 'milestone' in data and 'project_id' in data:
            model = Planning.model_validate(data)
            logger.info(f"✅ Valid Planning data: {model.id}")
        elif 'email' in data or 'role' in data:
            model = Person.model_validate(data)
            logger.info(f"✅ Valid Person data: {model.id}")
        else:
            model = Project.model_validate(data)
            logger.info(f"✅ Valid Project data: {model.id}")
            
    except Exception as e:
        logger.info(f"❌ JSON validation failed: {e}")
        sys.exit(1)


def serialize_model(model_type: str, data: str) -> None:
    """Serialize model data to JSON."""
    try:
        # Parse input data
        input_data = json.loads(data)
        
        # Create model instance
        if model_type == "project":
            model = Project.model_validate(input_data)
        elif model_type == "staff_time":
            model = StaffTime.model_validate(input_data)
        elif model_type == "person":
            model = Person.model_validate(input_data)
        elif model_type == "equipment":
            model = Equipment.model_validate(input_data)
        elif model_type == "ticket":
            model = Ticket.model_validate(input_data)
        elif model_type == "planning":
            model = Planning.model_validate(input_data)
        else:
            logger.info(f"❌ Unknown model type: {model_type}")
            sys.exit(1)
        
        # Serialize to JSON
        result = model.model_dump_json(indent=2)
        logger.info(result)
        
    except Exception as e:
        logger.info(f"❌ Serialization failed: {e}")
        sys.exit(1)


def create_sample_data(model_type: str) -> None:
    """Create sample data for a specific model type."""
    try:
        if model_type == "project":
            data = ModelFactory.create_sample_project_data()
        elif model_type == "staff_time":
            data = ModelFactory.create_sample_staff_time_data()
        elif model_type == "person":
            data = ModelFactory.create_sample_person_data()
        elif model_type == "equipment":
            data = ModelFactory.create_sample_equipment_data()
        elif model_type == "ticket":
            data = ModelFactory.create_sample_ticket_data()
        elif model_type == "planning":
            data = ModelFactory.create_sample_planning_data()
        else:
            logger.info(f"❌ Unknown model type: {model_type}")
            sys.exit(1)
        
        logger.info(json.dumps(data, indent=2, default=str))
        
    except Exception as e:
        logger.info(f"❌ Sample data creation failed: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Model Validation CLI")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Validate sample data command
    subparsers.add_parser("validate-sample-data", help="Validate all models with sample data")
    
    # Validate JSON file command
    validate_parser = subparsers.add_parser("validate-json", help="Validate JSON data against models")
    validate_parser.add_argument("--file", required=True, help="JSON file to validate")
    
    # Serialize model command
    serialize_parser = subparsers.add_parser("serialize", help="Serialize model data to JSON")
    serialize_parser.add_argument("--model", required=True, 
                                choices=["project", "staff_time", "person", "equipment", "ticket", "planning"],
                                help="Model type")
    serialize_parser.add_argument("--data", required=True, help="JSON data to serialize")
    
    # Create sample data command
    sample_parser = subparsers.add_parser("create-sample", help="Create sample data for a model")
    sample_parser.add_argument("--model", required=True,
                             choices=["project", "staff_time", "person", "equipment", "ticket", "planning"],
                             help="Model type")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "validate-sample-data":
        validate_sample_data()
    elif args.command == "validate-json":
        validate_json_data(args.file)
    elif args.command == "serialize":
        serialize_model(args.model, args.data)
    elif args.command == "create-sample":
        create_sample_data(args.model)


if __name__ == "__main__":
    main()
