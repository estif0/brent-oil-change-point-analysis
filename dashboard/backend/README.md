# Brent Oil Change Point Analysis - Backend API

## Overview

RESTful Flask API serving historical Brent oil price data, detected change points, and geopolitical event information for analysis and visualization.

## Features

- **16 RESTful Endpoints** - Complete API for prices, change points, and events
- **Service Layer Architecture** - Clean separation of concerns
- **CORS Enabled** - Cross-origin requests supported
- **Swagger Documentation** - Interactive API docs at `/api/docs`
- **Error Handling** - Comprehensive error responses
- **CSV Data Backend** - Efficient file-based storage

## Technology Stack

- **Flask 3.0.0** - Web framework
- **Flask-RESTful** - REST API extension
- **Flask-CORS** - Cross-origin resource sharing
- **flask-swagger-ui** - API documentation
- **pandas** - Data manipulation

## Quick Start

```bash
cd dashboard/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

API available at **http://localhost:5000**
Swagger docs at **http://localhost:5000/api/docs**

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (latest version)

### Steps

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Data Files**
   Required files:
   - `../../data/raw/BrentOilPrices.csv`
   - `../../data/events.csv`
   - `../../reports/changepoints_processed.csv`

4. **Run Server**
   ```bash
   python app.py
   ```

## API Endpoints

### Health Check
- `GET /health` - API health status

### Price Endpoints
- `GET /api/prices` - Historical prices (with date filters)
- `GET /api/prices/date-range` - Min/max dates
- `GET /api/prices/statistics` - Price statistics
- `GET /api/prices/info` - Metadata

### Change Point Endpoints
- `GET /api/changepoints` - All change points
- `GET /api/changepoints/<date>` - Specific change point
- `GET /api/changepoints/<date>/impact` - Impact analysis
- `GET /api/changepoints/stats` - Statistics

### Event Endpoints
- `GET /api/events` - All events (with filters)
- `GET /api/events/<id>` - Specific event
- `GET /api/events/<id>/impact` - Impact analysis
- `GET /api/events/types` - Event types
- `GET /api/events/types/<type>` - Events by type
- `GET /api/events/stats` - Statistics

### Correlation Endpoint
- `GET /api/correlations` - Change point-event correlations

## Example Usage

### Get Prices with Date Range
```bash
curl "http://localhost:5000/api/prices?start_date=2008-01-01&end_date=2008-12-31"
```

Response:
```json
{
  "success": true,
  "data": [
    {"date": "2008-01-02", "price": 96.84}
  ],
  "count": 252
}
```

### Get Change Points
```bash
curl http://localhost:5000/api/changepoints
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "date": "2008-07-14",
      "confidence": 94,
      "before_mean": 68.45,
      "after_mean": 51.23
    }
  ],
  "count": 1
}
```

### Get Events by Type
```bash
curl "http://localhost:5000/api/events?event_type=opec_decision"
```

## Project Structure

```
dashboard/backend/
├── app.py              # Flask app entry point
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── swagger.json        # OpenAPI spec
├── routes/             # API route blueprints
│   ├── data_routes.py
│   ├── changepoint_routes.py
│   └── event_routes.py
├── services/           # Business logic layer
│   ├── data_service.py
│   ├── changepoint_service.py
│   └── event_service.py
└── tests/              # Unit tests
```

## Service Layer

### DataService
- Load price data from CSV
- Filter by date range
- Calculate statistics

### ChangePointService
- Load change point data
- Get details and impact metrics

### EventService
- Load event data
- Filter by date and type
- Get event details and impact

## Error Responses

All errors return:
```json
{
  "success": false,
  "error": "Error message"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_data_service.py -v

# With coverage
pytest --cov=services tests/
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Security Considerations
- Configure CORS for production domains
- Add authentication for sensitive endpoints
- Enable rate limiting
- Use HTTPS

## Troubleshooting

**Port already in use:**
```bash
lsof -ti:5000 | xargs kill -9
```

**File not found:**
```bash
# Verify data files exist
ls -la ../../data/raw/BrentOilPrices.csv
```

**Import errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

---

**API Documentation:** http://localhost:5000/api/docs
**Backend Health:** http://localhost:5000/health
