# Brent Oil Change Point Analysis - Backend API

Flask-based REST API for the Brent Oil Change Point Analysis Dashboard.

## Overview

This backend provides RESTful API endpoints for accessing:
- Historical Brent oil price data
- Detected change points from Bayesian analysis
- Geopolitical and economic events
- Statistical analyses and impact assessments

## Tech Stack

- **Framework:** Flask 3.0
- **API:** Flask-RESTful
- **CORS:** Flask-CORS
- **Documentation:** Swagger UI (OpenAPI 3.0)
- **Data Processing:** pandas, numpy
- **Configuration:** python-dotenv

## Setup

### 1. Install Dependencies

```bash
cd dashboard/backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

The default configuration should work for local development.

### 3. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

### Interactive Documentation (Swagger UI)

Full interactive API documentation is available at:

**http://localhost:5000/api/docs**

The Swagger UI provides:
- Complete endpoint documentation with request/response schemas
- Try-it-out functionality to test endpoints directly
- Example requests and responses
- Data model schemas

### OpenAPI Specification

The OpenAPI 3.0 specification is available at:

**http://localhost:5000/swagger.json**

## API Endpoints

### Health Check

**GET** `/health`
- Check if API is running

**GET** `/`
- API information and available endpoints

### Price Data

**GET** `/api/prices`
- Get historical price data
- Query params:
  - `start_date` (optional): YYYY-MM-DD
  - `end_date` (optional): YYYY-MM-DD

**GET** `/api/prices/statistics`
- Get price statistics for date range
- Query params: same as `/api/prices`

**GET** `/api/prices/date-range`
- Get available date range in dataset

**GET** `/api/prices/info`
- Get dataset information

### Change Points

**GET** `/api/changepoints`
- Get list of detected change points
- Query params:
  - `start_date` (optional): YYYY-MM-DD
  - `end_date` (optional): YYYY-MM-DD
  - `min_confidence` (optional): float (0-1)

**GET** `/api/changepoints/<id>`
- Get details of a specific change point
- Path param: `id` (integer)

**GET** `/api/changepoints/stats`
- Get change point statistics

### Events

**GET** `/api/events`
- Get list of events
- Query params:
  - `start_date` (optional): YYYY-MM-DD
  - `end_date` (optional): YYYY-MM-DD
  - `event_type` (optional): geopolitical, opec_decision, economic_shock, sanction

**GET** `/api/events/<id>`
- Get details of a specific event
- Path param: `id` (integer)

**GET** `/api/events/<id>/impact`
- Get price impact analysis for an event
- Path param: `id` (integer)
- Query param: `window_days` (optional, default 30)

**GET** `/api/events/types`
- Get list of unique event types

**GET** `/api/events/stats`
- Get event statistics

## Example Requests

### Using curl

```bash
# Get price data for 2020
curl "http://localhost:5000/api/prices?start_date=2020-01-01&end_date=2020-12-31"

# Get price statistics
curl "http://localhost:5000/api/prices/statistics?start_date=2020-01-01&end_date=2020-12-31"

# Get change points
curl "http://localhost:5000/api/changepoints"

# Get events
curl "http://localhost:5000/api/events?event_type=geopolitical"

# Get event impact
curl "http://localhost:5000/api/events/0/impact?window_days=30"
```

### Response Format

All successful responses follow this format:

```json
{
  "success": true,
  "data": [...],  // or "statistics", "info", etc.
  "count": 10     // for list endpoints
}
```

Error responses:

```json
{
  "success": false,
  "error": "Error message"
}
```

## Project Structure

```
backend/
├── app.py                 # Flask application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (gitignored)
├── .env.example           # Example environment variables
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── data_service.py
│   ├── changepoint_service.py
│   └── event_service.py
├── routes/                # API endpoints
│   ├── __init__.py
│   ├── data_routes.py
│   ├── changepoint_routes.py
│   └── event_routes.py
└── tests/                 # Unit tests
    └── test_services.py
```

## Running Tests

```bash
cd dashboard/backend
python -m pytest tests/
```

Or run specific test file:

```bash
python tests/test_services.py
```

## Development

### Adding New Endpoints

1. Create service method in appropriate service class (`services/`)
2. Create Flask-RESTful Resource in appropriate route file (`routes/`)
3. Register resource in `app.py` `register_routes()` function
4. Add tests in `tests/`

### Configuration

The application uses environment-based configuration:
- `DevelopmentConfig` - For local development (default)
- `ProductionConfig` - For production deployment
- `TestingConfig` - For running tests

Set `FLASK_ENV` in `.env` to switch between configurations.

## CORS

CORS is enabled for the origins specified in `CORS_ORIGINS` environment variable. Default includes common local development ports for frontend frameworks.

## Data Sources

The API loads data from:
- `data/raw/BrentOilPrices.csv` - Historical price data
- `data/events.csv` - Event data
- `reports/changepoint_summary.csv` - Detected change points

Paths are configurable via environment variables.

## Error Handling

The API provides appropriate HTTP status codes:
- `200` - Success
- `404` - Resource not found
- `500` - Internal server error

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in environment
2. Use a production WSGI server (gunicorn, uWSGI)
3. Configure proper CORS origins
4. Use environment variables for sensitive configuration
5. Enable HTTPS
6. Consider rate limiting and authentication if needed

Example with gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

Part of the Brent Oil Change Point Analysis project for Birhan Energies.
