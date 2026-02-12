#!/bin/bash
# Comprehensive API Endpoint Testing Script

echo "=========================================="
echo "BRENT OIL API ENDPOINT TESTING"
echo "=========================================="
echo ""

BASE_URL="http://localhost:5000"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local description=$2
    echo -e "${YELLOW}Testing:${NC} $description"
    echo "Endpoint: $endpoint"
    
    response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✓ Status: $http_code${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        echo -e "${RED}✗ Status: $http_code${NC}"
        echo "$body"
    fi
    echo ""
    echo "------------------------------------------"
    echo ""
}

# Health Check Endpoints
echo "=== HEALTH CHECK ENDPOINTS ==="
test_endpoint "/health" "Health Check"
test_endpoint "/" "API Root Info"

# Price Data Endpoints
echo "=== PRICE DATA ENDPOINTS ==="
test_endpoint "/api/prices/date-range" "Get Available Date Range"
test_endpoint "/api/prices/info" "Get Dataset Info"
test_endpoint "/api/prices?start_date=2020-01-01&end_date=2020-01-31" "Get Prices (Jan 2020)"
test_endpoint "/api/prices/statistics?start_date=2020-01-01&end_date=2020-12-31" "Get Price Statistics (2020)"

# Change Point Endpoints
echo "=== CHANGE POINT ENDPOINTS ==="
test_endpoint "/api/changepoints" "Get All Change Points"
test_endpoint "/api/changepoints/1" "Get Change Point #1"
test_endpoint "/api/changepoints/stats" "Get Change Point Statistics"
test_endpoint "/api/changepoints?min_confidence=0.9" "Get High-Confidence Change Points"

# Event Endpoints
echo "=== EVENT ENDPOINTS ==="
test_endpoint "/api/events" "Get All Events"
test_endpoint "/api/events/0" "Get Event #0 (Gulf War)"
test_endpoint "/api/events/8" "Get Event #8 (Financial Crisis)"
test_endpoint "/api/events/types" "Get Event Types"
test_endpoint "/api/events/stats" "Get Event Statistics"
test_endpoint "/api/events?event_type=geopolitical" "Get Geopolitical Events"
test_endpoint "/api/events/0/impact?window_days=30" "Get Event #0 Impact"

# Swagger Documentation
echo "=== DOCUMENTATION ENDPOINTS ==="
test_endpoint "/swagger.json" "OpenAPI Specification"
echo -e "${YELLOW}Testing:${NC} Swagger UI"
echo "Endpoint: /api/docs/"
curl_output=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/docs/")
http_code=$(echo "$curl_output" | tail -n1)
if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✓ Status: $http_code (Swagger UI loads successfully)${NC}"
else
    echo -e "${RED}✗ Status: $http_code${NC}"
fi
echo ""
echo "------------------------------------------"

echo ""
echo "=========================================="
echo "TESTING COMPLETE"
echo "=========================================="
