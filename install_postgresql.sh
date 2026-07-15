#!/bin/bash

# PostgreSQL Installation and Setup for Student Result Management System
# Using custom user: student / student123

echo "========================================"
echo "PostgreSQL Installation & Setup"
echo "Student Result Management System"
echo "========================================"
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Step 1: Installing PostgreSQL..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    echo "✓ PostgreSQL installed"
else
    echo "✓ PostgreSQL is already installed"
fi

echo ""
echo "Step 2: Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql
echo "✓ PostgreSQL is running"

echo ""
echo "========================================"
echo "Creating Database User & Database"
echo "========================================"
echo ""

# Create PostgreSQL user 'student' with password 'student123'
echo "Creating user 'student'..."
sudo -u postgres psql -c "CREATE USER student WITH PASSWORD 'student123';" 2>/dev/null || echo "User 'student' already exists"

# Create database 'srms_db' owned by 'student'
echo "Creating database 'srms_db'..."
sudo -u postgres psql -c "CREATE DATABASE srms_db OWNER student;" 2>/dev/null || echo "Database 'srms_db' already exists"

# Grant all privileges
echo "Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE srms_db TO student;"
sudo -u postgres psql -c "ALTER USER student CREATEDB;"

echo "✓ User and database created"

echo ""
echo "========================================"
echo "Loading Database Schema"
echo "========================================"
echo ""

# Load schema as student user
echo "Creating tables..."
PGPASSWORD=student123 psql -U student -d srms_db -h localhost -f sql/schema.sql

if [ $? -eq 0 ]; then
    echo "✓ Schema loaded successfully"
else
    echo "✗ Failed to load schema. Trying with postgres user..."
    sudo -u postgres psql -d srms_db -f sql/schema.sql
    # Grant permissions on tables to student
    sudo -u postgres psql -d srms_db -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO student;"
    sudo -u postgres psql -d srms_db -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO student;"
fi

echo ""
echo "========================================"
echo "Loading Sample Data (Optional)"
echo "========================================"
echo ""

read -p "Load sample data? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Loading sample data..."
    PGPASSWORD=student123 psql -U student -d srms_db -h localhost -f sql/sample_data.sql
    
    if [ $? -eq 0 ]; then
        echo "✓ Sample data loaded"
    else
        echo "Trying with postgres user..."
        sudo -u postgres psql -d srms_db -f sql/sample_data.sql
    fi
fi

echo ""
echo "========================================"
echo "PostgreSQL Setup Complete!"
echo "========================================"
echo ""
echo "Database Configuration:"
echo "  Database: srms_db"
echo "  User: student"
echo "  Password: student123"
echo "  Host: localhost"
echo "  Port: 5432"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Create Django superuser:"
echo "   python manage.py createsuperuser"
echo ""
echo "3. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "4. Open browser and visit:"
echo "   http://localhost:8000"
echo ""
echo "========================================"
