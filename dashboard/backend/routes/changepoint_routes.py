"""
API routes for change point data.

This module defines Flask-RESTful resources for accessing
detected change points from Bayesian analysis.
"""

from flask import request
from flask_restful import Resource
from services.changepoint_service import ChangePointService
from config import get_config

# Initialize service
config = get_config()
changepoint_service = ChangePointService(config.CHANGEPOINT_SUMMARY_FILE)


class ChangePointList(Resource):
    """
    Resource for retrieving list of change points.

    Endpoints:
        GET /api/changepoints - Get list of detected change points
    """

    def get(self):
        """
        Get list of detected change points with optional filtering.

        Query Parameters:
            start_date (str, optional): Filter from this date (YYYY-MM-DD)
            end_date (str, optional): Filter to this date (YYYY-MM-DD)
            min_confidence (float, optional): Minimum confidence threshold (0-1)

        Returns:
            JSON response with change point array

        Example:
            GET /api/changepoints?min_confidence=0.8

            Response:
            {
                "success": true,
                "data": [
                    {
                        "id": 1,
                        "date": "2008-07-03",
                        "mean_before": 95.84,
                        "mean_after": 68.23,
                        "price_change": -27.61,
                        "percent_change": -28.8,
                        "confidence": 0.95,
                        "associated_event": "Global Financial Crisis"
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
            min_confidence = request.args.get("min_confidence", type=float)

            # Get change points
            changepoints = changepoint_service.get_changepoints(
                start_date=start_date, end_date=end_date, min_confidence=min_confidence
            )

            return {
                "success": True,
                "data": changepoints,
                "count": len(changepoints),
            }, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class ChangePointDetail(Resource):
    """
    Resource for retrieving specific change point details.

    Endpoints:
        GET /api/changepoints/<id> - Get details of a specific change point
    """

    def get(self, changepoint_id):
        """
        Get detailed information about a specific change point.

        Path Parameters:
            changepoint_id (int): ID of the change point

        Returns:
            JSON response with change point details

        Example:
            GET /api/changepoints/1

            Response:
            {
                "success": true,
                "data": {
                    "changepoint_id": 1,
                    "date": "2008-07-03",
                    "mean_before": 95.84,
                    "mean_after": 68.23,
                    "std_before": 15.32,
                    "std_after": 12.45,
                    "price_change": -27.61,
                    "percent_change": -28.8,
                    "confidence": 0.95,
                    "associated_event": "Global Financial Crisis"
                }
            }
        """
        try:
            changepoint = changepoint_service.get_changepoint_details(changepoint_id)

            if changepoint is None:
                return {
                    "success": False,
                    "error": f"Change point with ID {changepoint_id} not found",
                }, 404

            return {"success": True, "data": changepoint}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class ChangePointStats(Resource):
    """
    Resource for retrieving change point statistics.

    Endpoints:
        GET /api/changepoints/stats - Get statistics about change points
    """

    def get(self):
        """
        Get statistics about detected change points.

        Returns:
            JSON response with change point statistics

        Example:
            GET /api/changepoints/stats

            Response:
            {
                "success": true,
                "statistics": {
                    "total_count": 8,
                    "by_year": {
                        "2008": 2,
                        "2014": 1,
                        "2020": 2
                    }
                }
            }
        """
        try:
            total_count = changepoint_service.get_changepoint_count()
            by_year = changepoint_service.get_changepoints_by_year()

            return {
                "success": True,
                "statistics": {"total_count": total_count, "by_year": by_year},
            }, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500
