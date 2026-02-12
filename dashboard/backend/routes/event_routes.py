"""
API routes for event data.

This module defines Flask-RESTful resources for accessing
geopolitical and economic events that may impact oil prices.
"""

from flask import request
from flask_restful import Resource
from services.event_service import EventService
from services.data_service import DataService
from config import get_config

# Initialize services
config = get_config()
event_service = EventService(config.EVENTS_FILE)
data_service = DataService(config.BRENT_PRICES_FILE)


class EventList(Resource):
    """
    Resource for retrieving list of events.

    Endpoints:
        GET /api/events - Get list of events with optional filtering
    """

    def get(self):
        """
        Get list of events with optional filtering.

        Query Parameters:
            start_date (str, optional): Filter from this date (YYYY-MM-DD)
            end_date (str, optional): Filter to this date (YYYY-MM-DD)
            event_type (str, optional): Filter by event type
                (geopolitical, opec_decision, economic_shock, sanction)

        Returns:
            JSON response with event array

        Example:
            GET /api/events?event_type=opec_decision

            Response:
            {
                "success": true,
                "data": [
                    {
                        "id": 0,
                        "date": "1990-08-02",
                        "event_name": "Gulf War",
                        "event_type": "geopolitical",
                        "description": "Iraq invades Kuwait",
                        "expected_impact": "increase"
                    },
                    ...
                ],
                "count": 5
            }
        """
        try:
            # Get query parameters
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            event_type = request.args.get("event_type")

            # Get events
            events = event_service.get_events(
                start_date=start_date, end_date=end_date, event_type=event_type
            )

            return {"success": True, "data": events, "count": len(events)}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class EventDetail(Resource):
    """
    Resource for retrieving specific event details.

    Endpoints:
        GET /api/events/<id> - Get details of a specific event
    """

    def get(self, event_id):
        """
        Get detailed information about a specific event.

        Path Parameters:
            event_id (int): ID of the event

        Returns:
            JSON response with event details

        Example:
            GET /api/events/0

            Response:
            {
                "success": true,
                "data": {
                    "id": 0,
                    "date": "1990-08-02",
                    "event_name": "Gulf War",
                    "event_type": "geopolitical",
                    "description": "Iraq invades Kuwait",
                    "expected_impact": "increase"
                }
            }
        """
        try:
            event = event_service.get_event_details(event_id)

            if event is None:
                return {
                    "success": False,
                    "error": f"Event with ID {event_id} not found",
                }, 404

            return {"success": True, "data": event}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class EventImpact(Resource):
    """
    Resource for analyzing event impact on prices.

    Endpoints:
        GET /api/events/<id>/impact - Get price impact analysis for an event
    """

    def get(self, event_id):
        """
        Calculate price impact around a specific event.

        Path Parameters:
            event_id (int): ID of the event

        Query Parameters:
            window_days (int, optional): Days before/after event (default 30)

        Returns:
            JSON response with impact analysis

        Example:
            GET /api/events/0/impact?window_days=30

            Response:
            {
                "success": true,
                "impact": {
                    "event_id": 0,
                    "event_name": "Gulf War",
                    "event_date": "1990-08-02",
                    "window_days": 30,
                    "mean_price_before": 17.25,
                    "mean_price_after": 32.84,
                    "price_change": 15.59,
                    "price_change_pct": 90.38,
                    "volatility_before": 0.87,
                    "volatility_after": 3.45
                }
            }
        """
        try:
            window_days = request.args.get("window_days", default=30, type=int)

            # Get price data
            price_data = data_service.data

            # Calculate impact
            impact = event_service.get_event_impact(
                event_id=event_id, price_data=price_data, window_days=window_days
            )

            # Check for error
            if "error" in impact:
                return {"success": False, "error": impact["error"]}, 404

            return {"success": True, "impact": impact}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class EventTypes(Resource):
    """
    Resource for retrieving available event types.

    Endpoints:
        GET /api/events/types - Get list of unique event types
    """

    def get(self):
        """
        Get list of unique event types.

        Returns:
            JSON response with event types

        Example:
            GET /api/events/types

            Response:
            {
                "success": true,
                "event_types": [
                    "geopolitical",
                    "opec_decision",
                    "economic_shock",
                    "sanction"
                ]
            }
        """
        try:
            event_types = event_service.get_event_types()

            return {"success": True, "event_types": event_types}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class EventStats(Resource):
    """
    Resource for retrieving event statistics.

    Endpoints:
        GET /api/events/stats - Get statistics about events
    """

    def get(self):
        """
        Get statistics about events.

        Returns:
            JSON response with event statistics

        Example:
            GET /api/events/stats

            Response:
            {
                "success": true,
                "statistics": {
                    "total_count": 15,
                    "by_type": {
                        "geopolitical": 7,
                        "opec_decision": 4,
                        "economic_shock": 3,
                        "sanction": 1
                    }
                }
            }
        """
        try:
            by_type = event_service.get_events_by_type()
            total_count = sum(by_type.values())

            return {
                "success": True,
                "statistics": {"total_count": total_count, "by_type": by_type},
            }, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500
