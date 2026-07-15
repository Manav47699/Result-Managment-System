-- Sample data for Student Result Management System

-- Insert sample courses
INSERT INTO courses (name, code, duration, fee, description) VALUES
('Computer Science', 'CS101', 48, 15000.00, 'Comprehensive computer science program covering programming, databases, and algorithms'),
('Business Administration', 'BA201', 36, 12000.00, 'Business management and administration fundamentals'),
('Electrical Engineering', 'EE301', 48, 18000.00, 'Core electrical engineering principles and applications'),
('Data Science', 'DS401', 24, 20000.00, 'Data analysis, machine learning, and statistical modeling'),
('Web Development', 'WD501', 12, 8000.00, 'Full-stack web development with modern frameworks');

-- Insert sample students
INSERT INTO students (name, email, phone, gender, date_of_birth, address, course_id) VALUES
('John Doe', 'john.doe@example.com', '1234567890', 'Male', '2000-05-15', '123 Main St, City A', 1),
('Jane Smith', 'jane.smith@example.com', '9876543210', 'Female', '1999-08-22', '456 Oak Ave, City B', 1),
('Mike Johnson', 'mike.j@example.com', '5551234567', 'Male', '2001-03-10', '789 Pine Rd, City C', 2),
('Sarah Williams', 'sarah.w@example.com', '5559876543', 'Female', '2000-11-30', '321 Elm St, City A', 3),
('David Brown', 'david.brown@example.com', '5556667777', 'Male', '1998-07-18', '654 Maple Dr, City D', 4),
('Emily Davis', 'emily.davis@example.com', '5558889999', 'Female', '2002-01-25', '987 Cedar Ln, City B', 5),
('Robert Miller', 'robert.m@example.com', '5551112222', 'Male', '1999-09-05', '147 Birch Ct, City C', 1),
('Lisa Anderson', 'lisa.anderson@example.com', '5553334444', 'Female', '2001-12-12', '258 Walnut Pl, City A', 2);

-- Insert sample results
INSERT INTO results (student_id, course_id, subject_name, marks_obtained, total_marks, grade, exam_date, remarks) VALUES
-- John Doe (CS101)
(1, 1, 'Programming Fundamentals', 85.00, 100.00, 'A', '2024-12-15', 'Excellent performance'),
(1, 1, 'Data Structures', 78.00, 100.00, 'B+', '2024-12-18', 'Good understanding'),
(1, 1, 'Database Systems', 92.00, 100.00, 'A+', '2024-12-20', 'Outstanding work'),
(1, 1, 'Web Technologies', 88.00, 100.00, 'A', '2024-12-22', 'Very good'),

-- Jane Smith (CS101)
(2, 1, 'Programming Fundamentals', 95.00, 100.00, 'A+', '2024-12-15', 'Exceptional'),
(2, 1, 'Data Structures', 90.00, 100.00, 'A+', '2024-12-18', 'Excellent grasp'),
(2, 1, 'Database Systems', 87.00, 100.00, 'A', '2024-12-20', 'Very strong'),
(2, 1, 'Web Technologies', 93.00, 100.00, 'A+', '2024-12-22', 'Outstanding'),

-- Mike Johnson (BA201)
(3, 2, 'Business Management', 72.00, 100.00, 'B+', '2024-12-16', 'Good progress'),
(3, 2, 'Marketing Fundamentals', 68.00, 100.00, 'B', '2024-12-19', 'Satisfactory'),
(3, 2, 'Financial Accounting', 75.00, 100.00, 'B+', '2024-12-21', 'Solid understanding'),

-- Sarah Williams (EE301)
(4, 3, 'Circuit Analysis', 82.00, 100.00, 'A', '2024-12-17', 'Strong analytical skills'),
(4, 3, 'Digital Electronics', 79.00, 100.00, 'B+', '2024-12-19', 'Good performance'),
(4, 3, 'Control Systems', 85.00, 100.00, 'A', '2024-12-23', 'Excellent work'),

-- David Brown (DS401)
(5, 4, 'Statistics', 91.00, 100.00, 'A+', '2024-12-14', 'Outstanding'),
(5, 4, 'Machine Learning', 88.00, 100.00, 'A', '2024-12-17', 'Very good'),
(5, 4, 'Data Visualization', 94.00, 100.00, 'A+', '2024-12-21', 'Exceptional'),

-- Emily Davis (WD501)
(6, 5, 'HTML & CSS', 86.00, 100.00, 'A', '2024-12-15', 'Creative designs'),
(6, 5, 'JavaScript', 82.00, 100.00, 'A', '2024-12-18', 'Strong coding'),
(6, 5, 'React Framework', 90.00, 100.00, 'A+', '2024-12-20', 'Excellent projects'),

-- Robert Miller (CS101)
(7, 1, 'Programming Fundamentals', 70.00, 100.00, 'B', '2024-12-15', 'Needs practice'),
(7, 1, 'Data Structures', 65.00, 100.00, 'B', '2024-12-18', 'Improving'),

-- Lisa Anderson (BA201)
(8, 2, 'Business Management', 80.00, 100.00, 'A', '2024-12-16', 'Very good'),
(8, 2, 'Marketing Fundamentals', 84.00, 100.00, 'A', '2024-12-19', 'Strong concepts');
