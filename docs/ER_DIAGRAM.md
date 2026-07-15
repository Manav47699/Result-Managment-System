# Entity Relationship Diagram

## Student Result Management System

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    ENTITY RELATIONSHIP DIAGRAM                          │
│                Student Result Management System                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│      COURSES         │
├──────────────────────┤
│ PK: id               │
│     name             │
│     code (UNIQUE)    │
│     duration         │
│     fee              │
│     description      │
│     is_active        │
│     created_at       │
│     updated_at       │
└──────────┬───────────┘
           │
           │ 1
           │
           │
           │ N (One Course → Many Students)
           │
           ▼
┌──────────────────────┐
│      STUDENTS        │
├──────────────────────┤
│ PK: id               │
│     name             │
│     email (UNIQUE)   │
│     phone            │
│     gender           │
│     date_of_birth    │
│     address          │
│ FK: course_id        │◄────┐
│     enrollment_date  │     │
│     is_active        │     │
│     created_at       │     │
│     updated_at       │     │
└──────────┬───────────┘     │
           │                 │
           │ 1               │
           │                 │
           │                 │
           │ N (One Student → Many Results)
           │                 │
           ▼                 │
┌──────────────────────┐     │
│      RESULTS         │     │
├──────────────────────┤     │
│ PK: id               │     │
│ FK: student_id       │─────┘
│ FK: course_id        │─────┐
│     subject_name     │     │
│     marks_obtained   │     │
│     total_marks      │     │
│     grade            │     │
│     remarks          │     │
│     exam_date        │     │
│     created_at       │     │
│     updated_at       │     │
└──────────────────────┘     │
                             │
                             │ N
                             │
                             │ (One Course → Many Results)
                             │
                             │ 1
                             │
                             └─────────────────┐
                                               │
                                               ▼
                             ┌──────────────────────┐
                             │      COURSES         │
                             │   (back reference)   │
                             └──────────────────────┘


## RELATIONSHIPS

### 1. Courses ← → Students (One-to-Many)
- **Type**: 1:N
- **Foreign Key**: students.course_id → courses.id
- **On Delete**: SET NULL (student can exist without course)
- **Description**: One course can have many students enrolled

### 2. Students ← → Results (One-to-Many)
- **Type**: 1:N
- **Foreign Key**: results.student_id → students.id
- **On Delete**: CASCADE (delete results if student deleted)
- **Description**: One student can have many exam results

### 3. Courses ← → Results (One-to-Many)
- **Type**: 1:N
- **Foreign Key**: results.course_id → courses.id
- **On Delete**: CASCADE (delete results if course deleted)
- **Description**: One course can have many results across different students


## CONSTRAINTS

### Primary Keys
- courses.id (SERIAL)
- students.id (SERIAL)
- results.id (SERIAL)

### Foreign Keys
- students.course_id → courses.id
- results.student_id → students.id
- results.course_id → courses.id

### Unique Constraints
- courses.code
- students.email
- results(student_id, course_id, subject_name) - composite unique

### Check Constraints
- students.gender IN ('Male', 'Female', 'Other')
- results.marks_obtained >= 0
- results.total_marks > 0


## INDEXES (For Performance)

1. idx_students_course_id ON students(course_id)
2. idx_results_student_id ON results(student_id)
3. idx_results_course_id ON results(course_id)
4. idx_students_name ON students(name)
5. idx_students_email ON students(email)
6. idx_courses_name ON courses(name)
7. idx_courses_code ON courses(code)
8. idx_results_student_course ON results(student_id, course_id)


## SAMPLE QUERIES

### Get Students with Course Names (JOIN)
```sql
SELECT s.name, s.email, c.name as course_name
FROM students s
LEFT JOIN courses c ON s.course_id = c.id
WHERE s.is_active = TRUE;
```

### Get All Results for a Student (JOIN)
```sql
SELECT r.subject_name, r.marks_obtained, r.total_marks,
       ROUND((r.marks_obtained / r.total_marks * 100), 2) as percentage
FROM results r
WHERE r.student_id = 1;
```

### Course Enrollment Statistics (Aggregation)
```sql
SELECT c.name, COUNT(s.id) as student_count
FROM courses c
LEFT JOIN students s ON c.id = s.course_id AND s.is_active = TRUE
GROUP BY c.id, c.name
ORDER BY student_count DESC;
```

### Top Performing Students (JOIN + Aggregation)
```sql
SELECT s.name, c.name as course,
       ROUND(AVG(r.marks_obtained / r.total_marks * 100), 2) as avg_percentage
FROM results r
INNER JOIN students s ON r.student_id = s.id
INNER JOIN courses c ON r.course_id = c.id
GROUP BY s.id, s.name, c.name
HAVING COUNT(r.id) > 0
ORDER BY avg_percentage DESC
LIMIT 5;
```
