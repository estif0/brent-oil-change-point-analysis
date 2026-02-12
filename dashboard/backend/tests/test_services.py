"""
Unit tests for the backend services.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestDataService(unittest.TestCase):
    """Tests for DataService."""

    def setUp(self):
        """Set up test fixtures."""
        from dashboard.backend.services.data_service import DataService

        data_file = project_root / "data" / "raw" / "BrentOilPrices.csv"
        self.service = DataService(data_file)

    def test_service_initialization(self):
        """Test service initializes properly."""
        self.assertIsNotNone(self.service.data)
        self.assertTrue(len(self.service.data) > 0)

    def test_get_historical_prices(self):
        """Test getting historical prices."""
        prices = self.service.get_historical_prices("2020-01-01", "2020-01-31")
        self.assertIsInstance(prices, list)
        self.assertTrue(len(prices) > 0)
        self.assertIn("date", prices[0])
        self.assertIn("price", prices[0])

    def test_get_price_statistics(self):
        """Test getting price statistics."""
        stats = self.service.get_price_statistics("2020-01-01", "2020-12-31")
        self.assertIn("mean", stats)
        self.assertIn("median", stats)
        self.assertIn("std", stats)
        self.assertIn("min", stats)
        self.assertIn("max", stats)
        self.assertIn("count", stats)

    def test_get_date_range(self):
        """Test getting date range."""
        date_range = self.service.get_date_range()
        self.assertIn("min_date", date_range)
        self.assertIn("max_date", date_range)


class TestChangePointService(unittest.TestCase):
    """Tests for ChangePointService."""

    def setUp(self):
        """Set up test fixtures."""
        from dashboard.backend.services.changepoint_service import ChangePointService

        changepoint_file = project_root / "reports" / "changepoint_summary.csv"
        self.service = ChangePointService(changepoint_file)

    def test_service_initialization(self):
        """Test service initializes properly."""
        self.assertIsNotNone(self.service.data)

    def test_get_changepoints(self):
        """Test getting change points."""
        changepoints = self.service.get_changepoints()
        self.assertIsInstance(changepoints, list)


class TestEventService(unittest.TestCase):
    """Tests for EventService."""

    def setUp(self):
        """Set up test fixtures."""
        from dashboard.backend.services.event_service import EventService

        event_file = project_root / "data" / "events.csv"
        self.service = EventService(event_file)

    def test_service_initialization(self):
        """Test service initializes properly."""
        self.assertIsNotNone(self.service.data)
        self.assertTrue(len(self.service.data) > 0)

    def test_get_events(self):
        """Test getting events."""
        events = self.service.get_events()
        self.assertIsInstance(events, list)
        self.assertTrue(len(events) > 0)
        self.assertIn("id", events[0])
        self.assertIn("date", events[0])
        self.assertIn("event_name", events[0])

    def test_filter_by_type(self):
        """Test filtering events by type."""
        events = self.service.get_events(event_type="geopolitical")
        self.assertIsInstance(events, list)

    def test_get_event_types(self):
        """Test getting event types."""
        types = self.service.get_event_types()
        self.assertIsInstance(types, list)
        self.assertTrue(len(types) > 0)


if __name__ == "__main__":
    unittest.main()
