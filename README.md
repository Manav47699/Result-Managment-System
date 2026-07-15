# Student Result Management System (SRMS)

A production-grade Student Result Management System built with Django and PostgreSQL, demonstrating clean architecture, raw SQL implementation, and professional development practices.

## 🚀 Features

- **Clean Architecture**: Repository → Service → View → Template layers
- **Raw SQL**: All database operations use `django.db.connection.cursor()` 
- **Complete CRUD**: Full Create, Read, Update, Delete for Students, Courses, and Results
- **Authentication**: Secure login/logout system
- **Dashboard Analytics**: Real-time statistics with SQL aggregation
- **Search & Filter**: Find students, courses, and results quickly
- **Grade Calculation**: Automatic grade assignment based on percentage
- **Responsive UI**: Modern interface with Tailwind CSS

## 🏗️ Architecture

```
User Request → View Layer → Service Layer → Repository Layer → PostgreSQL
```

- **Repository Layer**: Raw SQL queries with parameterized execution
- **Service Layer**: Business logic, validation, data transformation
- **View Layer**: Request handling, authentication checks
- **Template Layer**: Clean, responsive UI

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 14+
- pip & virtualenv

## ⚙️ Installation

### 1. Clone and Setup Virtual Environment

```bash
cd Result_management
source venv/bin/activate  # Already exists
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` file with your PostgreSQL credentials:

```env
DB_NAME=srms_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Create Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE srms_db;

# Exit psql
\q
```

### 5. Run Database Schema

```bash
psql -U postgres -d srms_db -f sql/schema.sql
```

### 6. Load Sample Data (Optional)

```bash
psql -U postgres -d srms_db -f sql/sample_data.sql
```

### 7. Create Django Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 📁 Project Structure

```
Result_management/
├── apps/
│   ├── accounts/       # Authentication
│   ├── students/       # Student management
│   ├── courses/        # Course management
│   ├── results/        # Result management
│   └── dashboard/      # Dashboard analytics
├── repositories/       # Raw SQL queries
├── services/          # Business logic
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── sql/              # Database scripts
└── core/             # Django settings
```

## 🗄️ Database Schema

### Tables

- **courses**: Course information
- **students**: Student details with course enrollment
- **results**: Exam results with marks and grades
- **users**: Django authentication (managed by Django)

### Key Relationships

- One Course → Many Students (1:N)
- One Student → Many Results (1:N)
- One Course → Many Results (1:N)

## 🔐 Security Features

- ✅ Parameterized SQL queries (SQL injection prevention)
- ✅ Django CSRF protection
- ✅ Authentication required for all pages
- ✅ Session management
- ✅ Password hashing

## 📊 Key SQL Operations

### Students with Course Names (JOIN)
```sql
SELECT s.*, c.name as course_name
FROM students s
LEFT JOIN courses c ON s.course_id = c.id
WHERE s.is_active = TRUE;
```

### Dashboard Statistics (Aggregation)
```sql
SELECT COUNT(*) FROM students WHERE is_active = TRUE;
SELECT COUNT(*) FROM courses WHERE is_active = TRUE;
SELECT COUNT(*) FROM results;
```

### Top Performers (JOIN + GROUP BY + Aggregation)
```sql
SELECT s.name, ROUND(AVG(r.marks_obtained / r.total_marks * 100), 2) as avg
FROM results r
INNER JOIN students s ON r.student_id = s.id
GROUP BY s.id, s.name
ORDER BY avg DESC LIMIT 5;
```

## 🎨 UI Pages

- **Login**: Secure authentication
- **Dashboard**: Overview with statistics
- **Students**: List, Create, Update, Delete
- **Courses**: List, Create, Update, Delete
- **Results**: List, Create, Update, Delete, View by Student

## 🧪 Testing

### Test CRUD Operations

1. **Create Student**: Add new student with course enrollment
2. **Create Course**: Add new course with details
3. **Create Result**: Add exam result for student
4. **Search**: Search students by name/email
5. **Update**: Modify existing records
6. **Delete**: Remove records (soft delete for students)

### Test Edge Cases

- Empty data scenarios
- Invalid input validation
- Foreign key constraints
- SQL injection attempts (should be prevented)

## 📈 Performance Optimization

- ✅ Indexes on foreign keys
- ✅ Efficient JOIN queries
- ✅ Query result caching where applicable
- ✅ Minimal database round trips

## 🎓 Educational Value

This project demonstrates:

- Clean software architecture
- Raw SQL proficiency
- Database design principles
- Security best practices
- RESTful URL patterns
- Django framework expertise

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify credentials in .env file
```

### Module Import Error
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 License

Educational Project - Free to use for learning purposes

## 👨‍💻 Author

Built following industry best practices for academic demonstration.

---

**Note**: This is a demonstration project showcasing clean architecture, raw SQL implementation, and professional development practices suitable for academic submission and viva presentation.
