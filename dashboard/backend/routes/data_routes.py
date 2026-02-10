"""
API routes for historical price data.

This module defines Flask-RESTful resources for accessing
Brent oil historical price data and statistics.
"""

from flask import request
from flask_restful import Resource
from services.data_service import DataService
from config import get_config

# Initialize service
config = get_config()
data_service = DataService(config.BRENT_PRICES_FILE)


class PriceList(Resource):
    """
    Resource for retrieving historical price data.

    Endpoints:
        GET /api/prices - Get historical price data with optional date filtering
    """

    def get(self):
        """
        Get historical price data.

        Query Parameters:
            start_date (str, optional): Start date in YYYY-MM-DD format
            end_date (str, optional): End date in YYYY-MM-DD format

        Returns:
            JSON response with price data array

        Example:
            GET /api/prices?start_date=2020-01-01&end_date=2020-12-31

            Response:
            {
                "success": true,
                "data": [
                    {"date": "2020-01-02", "price": 68.91},
                    {"date": "2020-01-03", "price": 69.52},
                    ...
                ],
                "count": 253
            }
        """
        try:
            # Get query parameters
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")

            # Get price data
            prices = data_service.get_historical_prices(start_date, end_date)

            return {"success": True, "data": prices, "count": len(prices)}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class PriceStatistics(Resource):
    """
    Resource for retrieving price statistics.

    Endpoints:
        GET /api/prices/statistics - Get statistical summary of prices
    """

    def get(self):
        """
        Get price statistics for specified date range.

        Query Parameters:
            start_date (str, optional): Start date in YYYY-MM-DD format
            end_date (str, optional): End date in YYYY-MM-DD format

        Returns:
            JSON response with statistical measures

        Example:
            GET /api/prices/statistics?start_date=2020-01-01&end_date=2020-12-31

            Response:
            {
                "success": true,
                "statistics": {
                    "mean": 43.21,
                    "median": 41.84,
                    "std": 11.45,
                    "min": 19.33,
                    "max": 68.91,
                    "count": 253,
                    "start_date": "2020-01-02",
                    "end_date": "2020-12-30"
                }
            }
        """
        try:
            # Get query parameters
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")

            # Get statistics
            stats = data_service.get_price_statistics(start_date, end_date)

            # Check for error in stats
            if "error" in stats:
                return {"success": False, "error": stats["error"]}, 404

            return {"success": True, "statistics": stats}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class DateRange(Resource):
    """
    Resource for retrieving available date range.

    Endpoints:
        GET /api/prices/date-range - Get min and max dates available
    """

    def get(self):
        """
        Get the full date range available in the dataset.

        Returns:
            JSON response with min_date and max_date

        Example:
            GET /api/prices/date-range

            Response:
            {
                "success": true,
                "date_range": {
                    "min_date": "1987-05-20",
                    "max_date": "2022-09-30"
                }
            }
        """
        try:
            date_range = data_service.get_date_range()

            return {"success": True, "date_range": date_range}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class DataInfo(Resource):
    """
    Resource for retrieving dataset information.

    Endpoints:
        GET /api/prices/info - Get information about the dataset
    """

    def get(self):
        """
        Get information about the loaded dataset.

        Returns:
            JSON response with dataset information

        Example:
            GET /api/prices/info

            Response:
            {
                "success": true,
                "info": {
                    "total_records": 9154,
                    "date_range": {
                        "min_date": "1987-05-20",
                        "max_date": "2022-09-30"
                    },
                    "columns": ["Date", "Price"],
                    "missing_values": 0
                }
            }
        """
        try:
            info = data_service.get_data_info()

            return {"success": True, "info": info}, 200

        except Exception as e:
            return {"success": False, "error": str(e)}, 500
