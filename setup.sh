#!/bin/bash

# Setup script for Student Result Management System

echo "========================================"
echo "Student Result Management System Setup"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if PostgreSQL is running
echo -e "${YELLOW}Checking PostgreSQL...${NC}"
if sudo systemctl is-active --quiet postgresql; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not running${NC}"
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql
fi

echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✓ Virtual environment is activated${NC}"
else
    echo -e "${YELLOW}! Virtual environment not activated${NC}"
    echo "Run: source venv/bin/activate"
    exit 1
fi

echo ""

# Database setup
echo -e "${YELLOW}Setting up database...${NC}"
echo "Enter PostgreSQL password when prompted"

# Create database
echo "Creating database 'srms_db'..."
psql -U postgres -c "CREATE DATABASE srms_db;" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${YELLOW}! Database already exists or error occurred${NC}"
fi

echo ""

# Run schema
echo "Running database schema..."
psql -U postgres -d srms_db -f sql/schema.sql > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Schema created successfully${NC}"
else
    echo -e "${RED}✗ Failed to create schema${NC}"
    exit 1
fi

echo ""

# Load sample data
read -p "Load sample data? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Loading sample data..."
    psql -U postgres -d srms_db -f sql/sample_data.sql > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Sample data loaded${NC}"
    else
        echo -e "${RED}✗ Failed to load sample data${NC}"
    fi
fi

echo ""

# Create superuser
echo -e "${YELLOW}Creating Django superuser...${NC}"
echo "Follow the prompts to create an admin user"
python manage.py createsuperuser

echo ""
echo -e "${GREEN}========================================"
echo "Setup Complete!"
echo "========================================${NC}"
echo ""
echo "To start the server:"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://localhost:8000"
echo ""
echo "Sample credentials (if sample data loaded):"
echo "  Username: admin"
echo "  Password: (the one you just created)"
echo ""
