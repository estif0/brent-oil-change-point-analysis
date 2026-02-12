"""
Configuration management for the Flask backend.

This module provides configuration settings for different environments
(development, production, testing).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the backend
BASE_DIR = Path(__file__).resolve().parent

# Project root directory (two levels up from backend)
PROJECT_ROOT = BASE_DIR.parent.parent


class Config:
    """Base configuration class with common settings."""

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    # Server settings
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))

    # CORS settings
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")

    # Data paths
    DATA_DIR = PROJECT_ROOT / os.environ.get("DATA_DIR", "data")
    REPORTS_DIR = PROJECT_ROOT / os.environ.get("REPORTS_DIR", "reports")

    # Specific data files
    BRENT_PRICES_FILE = DATA_DIR / "raw" / "BrentOilPrices.csv"
    EVENTS_FILE = DATA_DIR / "events.csv"
    CHANGEPOINT_SUMMARY_FILE = REPORTS_DIR / "changepoints_processed.csv"
    IMPACT_STATEMENT_FILE = REPORTS_DIR / "impact_statement.txt"

    # API settings
    API_PREFIX = "/api"
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(env=None):
    """
    Get configuration object based on environment.

    Args:
        env (str, optional): Environment name. If None, uses FLASK_ENV
                           from environment variables.

    Returns:
        Config: Configuration object for the specified environment.
    """
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")
    return config.get(env, config["default"])
