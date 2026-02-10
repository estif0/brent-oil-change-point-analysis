"""
Flask application entry point for the Brent Oil Change Point Analysis Dashboard.

This module initializes and configures the Flask application, sets up CORS,
and registers API routes.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from config import get_config
import sys
from pathlib import Path

# Add project src to path for imports
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app.

    Args:
        config_name (str, optional): Configuration environment name.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Enable CORS
    CORS(app, origins=config.CORS_ORIGINS)

    # Initialize Flask-RESTful API
    api = Api(app, prefix=config.API_PREFIX)

    # Register routes (will be added in subsequent tasks)
    register_routes(api)

    # Health check endpoint
    @app.route("/health")
    def health_check():
        """Health check endpoint to verify API is running."""
        return jsonify(
            {
                "status": "healthy",
                "service": "Brent Oil Change Point Analysis API",
                "version": "1.0.0",
            }
        )

    # Root endpoint
    @app.route("/")
    def index():
        """Root endpoint with API information."""
        return jsonify(
            {
                "message": "Brent Oil Change Point Analysis API",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/health",
                    "api": {
                        "prices": f"{config.API_PREFIX}/prices",
                        "changepoints": f"{config.API_PREFIX}/changepoints",
                        "events": f"{config.API_PREFIX}/events",
                    },
                },
            }
        )

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({"error": "Internal server error"}), 500

    return app


def register_routes(api):
    """
    Register API routes with the Flask-RESTful API instance.

    Args:
        api (Api): Flask-RESTful API instance.
    """
    # Import route resources
    from routes.data_routes import PriceList, PriceStatistics, DateRange, DataInfo
    from routes.changepoint_routes import (
        ChangePointList,
        ChangePointDetail,
        ChangePointStats,
    )
    from routes.event_routes import (
        EventList,
        EventDetail,
        EventImpact,
        EventTypes,
        EventStats,
    )

    # Register data/price routes
    api.add_resource(PriceList, "/prices")
    api.add_resource(PriceStatistics, "/prices/statistics")
    api.add_resource(DateRange, "/prices/date-range")
    api.add_resource(DataInfo, "/prices/info")

    # Register change point routes
    api.add_resource(ChangePointList, "/changepoints")
    api.add_resource(ChangePointDetail, "/changepoints/<int:changepoint_id>")
    api.add_resource(ChangePointStats, "/changepoints/stats")

    # Register event routes
    api.add_resource(EventList, "/events")
    api.add_resource(EventDetail, "/events/<int:event_id>")
    api.add_resource(EventImpact, "/events/<int:event_id>/impact")
    api.add_resource(EventTypes, "/events/types")
    api.add_resource(EventStats, "/events/stats")


if __name__ == "__main__":
    app = create_app()
    config = get_config()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
