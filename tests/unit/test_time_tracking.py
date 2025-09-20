"""
Unit tests for time tracking library.

Follows Article III: Test-First Imperative - Tests written before implementation.
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# Add libraries to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "libraries"))

from time_tracking import TimeTracker, TimeTrackingError, InvalidProjectError, TimeTrackingActiveError, TimeTrackingNotActiveError


class TestTimeTracker:
    """Test cases for TimeTracker class."""
    
    def test_init_with_valid_client(self):
        """Test TimeTracker initialization with valid GraphQL client."""
        mock_client = Mock()
        tracker = TimeTracker(mock_client)
        assert tracker.client == mock_client
        assert tracker.active_tracking is None
    
    @pytest.mark.asyncio
    async def test_start_time_tracking_success(self):
        """Test successful time tracking start."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "createStaffTime": {
                "id": "time-123",
                "projectId": "proj-123",
                "personId": "person-456",
                "startTime": "2024-01-01T09:00:00Z",
                "isActive": True
            }
        })
        
        tracker = TimeTracker(mock_client)
        result = await tracker.start_time_tracking("proj-123", "person-456")
        
        assert result["id"] == "time-123"
        assert result["projectId"] == "proj-123"
        assert result["personId"] == "person-456"
        assert result["isActive"] is True
        assert tracker.active_tracking == "time-123"
    
    @pytest.mark.asyncio
    async def test_start_time_tracking_when_already_active(self):
        """Test starting time tracking when already active raises error."""
        mock_client = Mock()
        tracker = TimeTracker(mock_client)
        tracker.active_tracking = "existing-time-123"
        
        with pytest.raises(TimeTrackingActiveError):
            await tracker.start_time_tracking("proj-123", "person-456")
    
    @pytest.mark.asyncio
    async def test_stop_time_tracking_success(self):
        """Test successful time tracking stop."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(return_value={
            "updateStaffTime": {
                "id": "time-123",
                "endTime": "2024-01-01T17:00:00Z",
                "durationHours": 8.0,
                "isActive": False
            }
        })
        
        tracker = TimeTracker(mock_client)
        tracker.active_tracking = "time-123"
        
        result = await tracker.stop_time_tracking()
        
        assert result["id"] == "time-123"
        assert result["endTime"] == "2024-01-01T17:00:00Z"
        assert result["durationHours"] == 8.0
        assert result["isActive"] is False
        assert tracker.active_tracking is None
    
    @pytest.mark.asyncio
    async def test_stop_time_tracking_when_not_active(self):
        """Test stopping time tracking when not active raises error."""
        mock_client = Mock()
        tracker = TimeTracker(mock_client)
        tracker.active_tracking = None
        
        with pytest.raises(TimeTrackingNotActiveError):
            await tracker.stop_time_tracking()
    
    @pytest.mark.asyncio
    async def test_get_current_times_success(self):
        """Test getting current time tracking data."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "staffTimes": [
                {
                    "id": "time-123",
                    "projectId": "proj-123",
                    "personId": "person-456",
                    "startTime": "2024-01-01T09:00:00Z",
                    "endTime": None,
                    "durationHours": None,
                    "isActive": True
                }
            ]
        })
        
        tracker = TimeTracker(mock_client)
        result = await tracker.get_current_times()
        
        assert len(result) == 1
        assert result[0]["id"] == "time-123"
        assert result[0]["isActive"] is True
    
    @pytest.mark.asyncio
    async def test_get_current_times_empty(self):
        """Test getting current times when none are active."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={"staffTimes": []})
        
        tracker = TimeTracker(mock_client)
        result = await tracker.get_current_times()
        
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_current_times_for_project(self):
        """Test getting current times for specific project."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "staffTimes": [
                {
                    "id": "time-123",
                    "projectId": "proj-123",
                    "personId": "person-456",
                    "startTime": "2024-01-01T09:00:00Z",
                    "isActive": True
                }
            ]
        })
        
        tracker = TimeTracker(mock_client)
        result = await tracker.get_current_times(project_id="proj-123")
        
        assert len(result) == 1
        assert result[0]["projectId"] == "proj-123"
    
    @pytest.mark.asyncio
    async def test_get_current_times_for_person(self):
        """Test getting current times for specific person."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "staffTimes": [
                {
                    "id": "time-123",
                    "projectId": "proj-123",
                    "personId": "person-456",
                    "startTime": "2024-01-01T09:00:00Z",
                    "isActive": True
                }
            ]
        })
        
        tracker = TimeTracker(mock_client)
        result = await tracker.get_current_times(person_id="person-456")
        
        assert len(result) == 1
        assert result[0]["personId"] == "person-456"
    
    @pytest.mark.asyncio
    async def test_start_time_tracking_invalid_project(self):
        """Test starting time tracking with invalid project raises error."""
        mock_client = Mock()
        mock_client.mutation = AsyncMock(side_effect=Exception("Project not found"))
        
        tracker = TimeTracker(mock_client)
        
        with pytest.raises(InvalidProjectError):
            await tracker.start_time_tracking("invalid-proj", "person-456")
    
    @pytest.mark.asyncio
    async def test_get_time_tracking_history(self):
        """Test getting time tracking history."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "staffTimes": [
                {
                    "id": "time-123",
                    "projectId": "proj-123",
                    "personId": "person-456",
                    "startTime": "2024-01-01T09:00:00Z",
                    "endTime": "2024-01-01T17:00:00Z",
                    "durationHours": 8.0,
                    "isActive": False
                }
            ]
        })
        
        tracker = TimeTracker(mock_client)
        result = await tracker.get_time_tracking_history()
        
        assert len(result) == 1
        assert result[0]["durationHours"] == 8.0
        assert result[0]["isActive"] is False
    
    @pytest.mark.asyncio
    async def test_get_time_tracking_history_with_filters(self):
        """Test getting time tracking history with filters."""
        mock_client = Mock()
        mock_client.query = AsyncMock(return_value={
            "staffTimes": [
                {
                    "id": "time-123",
                    "projectId": "proj-123",
                    "personId": "person-456",
                    "startTime": "2024-01-01T09:00:00Z",
                    "endTime": "2024-01-01T17:00:00Z",
                    "durationHours": 8.0,
                    "isActive": False
                }
            ]
        })
        
        tracker = TimeTracker(mock_client)
        result = await tracker.get_time_tracking_history(
            project_id="proj-123",
            person_id="person-456",
            start_date="2024-01-01",
            end_date="2024-01-31"
        )
        
        assert len(result) == 1
        assert result[0]["projectId"] == "proj-123"
        assert result[0]["personId"] == "person-456"
    
    def test_is_tracking_active(self):
        """Test checking if time tracking is active."""
        mock_client = Mock()
        tracker = TimeTracker(mock_client)
        
        # Initially not active
        assert not tracker.is_tracking_active()
        
        # Set active tracking
        tracker.active_tracking = "time-123"
        assert tracker.is_tracking_active()
    
    def test_get_active_tracking_id(self):
        """Test getting active tracking ID."""
        mock_client = Mock()
        tracker = TimeTracker(mock_client)
        
        # Initially no active tracking
        assert tracker.get_active_tracking_id() is None
        
        # Set active tracking
        tracker.active_tracking = "time-123"
        assert tracker.get_active_tracking_id() == "time-123"
