from repositories.base_repository import BaseRepository
from typing import List, Tuple, Optional


class StudentRepository(BaseRepository):
    """Repository for Student entity using raw SQL"""
    
    @staticmethod
    def get_all_students() -> List[Tuple]:
        """Fetch all students with course information using JOIN"""
        query = """
            SELECT 
                s.id, s.name, s.email, s.phone, s.gender,
                s.date_of_birth, s.address, s.enrollment_date,
                c.id as course_id, c.name as course_name, c.code as course_code
            FROM students s
            LEFT JOIN courses c ON s.course_id = c.id
            WHERE s.is_active = TRUE
            ORDER BY s.name ASC
        """
        return BaseRepository.execute_query(query)
    
    @staticmethod
    def get_student_by_id(student_id: int) -> Optional[Tuple]:
        """Fetch a single student by ID"""
        query = """
            SELECT 
                s.id, s.name, s.email, s.phone, s.gender,
                s.date_of_birth, s.address, s.enrollment_date,
                c.id as course_id, c.name as course_name
            FROM students s
            LEFT JOIN courses c ON s.course_id = c.id
            WHERE s.id = %s AND s.is_active = TRUE
        """
        results = BaseRepository.execute_query(query, (student_id,))
        return results[0] if results else None
    
    @staticmethod
    def create_student(name: str, email: str, phone: str, gender: str,
                      date_of_birth: str, address: str, course_id: Optional[int]) -> int:
        """Insert a new student"""
        query = """
            INSERT INTO students (name, email, phone, gender, date_of_birth, address, course_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        return BaseRepository.execute_insert(query, (name, email, phone, gender, 
                                                     date_of_birth, address, course_id))
    
    @staticmethod
    def update_student(student_id: int, name: str, email: str, phone: str,
                      gender: str, date_of_birth: str, address: str, course_id: Optional[int]) -> int:
        """Update student information"""
        query = """
            UPDATE students 
            SET name = %s, email = %s, phone = %s, gender = %s,
                date_of_birth = %s, address = %s, course_id = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        return BaseRepository.execute_update(query, (name, email, phone, gender,
                                                     date_of_birth, address, course_id, student_id))
    
    @staticmethod
    def delete_student(student_id: int) -> int:
        """Soft delete a student (set is_active to FALSE)"""
        query = "UPDATE students SET is_active = FALSE WHERE id = %s"
        return BaseRepository.execute_update(query, (student_id,))
    
    @staticmethod
    def search_students(keyword: str) -> List[Tuple]:
        """Search students by name or email"""
        query = """
            SELECT 
                s.id, s.name, s.email, s.phone, s.gender,
                c.name as course_name
            FROM students s
            LEFT JOIN courses c ON s.course_id = c.id
            WHERE s.is_active = TRUE 
            AND (s.name ILIKE %s OR s.email ILIKE %s)
            ORDER BY s.name ASC
        """
        search_term = f"%{keyword}%"
        return BaseRepository.execute_query(query, (search_term, search_term))
    
    @staticmethod
    def get_students_by_course(course_id: int) -> List[Tuple]:
        """Get all students enrolled in a specific course"""
        query = """
            SELECT id, name, email, phone, gender, enrollment_date
            FROM students
            WHERE course_id = %s AND is_active = TRUE
            ORDER BY name ASC
        """
        return BaseRepository.execute_query(query, (course_id,))
