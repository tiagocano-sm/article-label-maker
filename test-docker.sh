#!/bin/bash

# Test script for Docker setup
set -e

echo "🐳 Testing Article Label Maker Docker Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

# Check if Docker is running
echo "Checking Docker..."
if docker info > /dev/null 2>&1; then
    print_status 0 "Docker is running"
else
    print_status 1 "Docker is not running"
fi

# Check if docker-compose is available
echo "Checking docker-compose..."
if command -v docker-compose > /dev/null 2>&1; then
    print_status 0 "docker-compose is available"
else
    print_status 1 "docker-compose is not available"
fi

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d
print_status $? "Services started"

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Test API health
echo "Testing API health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status 0 "API is healthy"
else
    print_status 1 "API health check failed"
fi

# Test frontend
echo "Testing frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_status 0 "Frontend is accessible"
else
    print_status 1 "Frontend is not accessible"
fi

# Test API documentation
echo "Testing API documentation..."
if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
    print_status 0 "API documentation is accessible"
else
    print_status 1 "API documentation is not accessible"
fi

# Show container status
echo "Container status:"
docker-compose ps

echo ""
echo -e "${GREEN}🎉 All tests passed! Your Docker setup is working correctly.${NC}"
echo ""
echo "Access your application at:"
echo "  Frontend: http://localhost:3000"
echo "  API Docs: http://localhost:8000/docs"
echo "  API Health: http://localhost:8000/health"
echo ""
echo "To stop the services, run: docker-compose down"
