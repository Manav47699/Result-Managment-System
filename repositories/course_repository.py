from repositories.base_repository import BaseRepository
from typing import List, Tuple, Optional


class CourseRepository(BaseRepository):
    """Repository for Course entity using raw SQL"""
    
    @staticmethod
    def get_all_courses() -> List[Tuple]:
        """Fetch all active courses"""
        query = """
            SELECT id, name, code, duration, fee, description, created_at
            FROM courses
            WHERE is_active = TRUE
            ORDER BY name ASC
        """
        return BaseRepository.execute_query(query)
    
    @staticmethod
    def get_course_by_id(course_id: int) -> Optional[Tuple]:
        """Fetch single course by ID"""
        query = """
            SELECT id, name, code, duration, fee, description
            FROM courses
            WHERE id = %s AND is_active = TRUE
        """
        results = BaseRepository.execute_query(query, (course_id,))
        return results[0] if results else None
    
    @staticmethod
    def create_course(name: str, code: str, duration: int, fee: float, description: str) -> int:
        """Insert a new course"""
        query = """
            INSERT INTO courses (name, code, duration, fee, description)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        return BaseRepository.execute_insert(query, (name, code, duration, fee, description))
    
    @staticmethod
    def update_course(course_id: int, name: str, code: str, 
                     duration: int, fee: float, description: str) -> int:
        """Update course information"""
        query = """
            UPDATE courses
            SET name = %s, code = %s, duration = %s, fee = %s, 
                description = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        return BaseRepository.execute_update(query, (name, code, duration, fee, description, course_id))
    
    @staticmethod
    def delete_course(course_id: int) -> int:
        """Soft delete a course"""
        query = "UPDATE courses SET is_active = FALSE WHERE id = %s"
        return BaseRepository.execute_update(query, (course_id,))
    
    @staticmethod
    def get_course_with_student_count() -> List[Tuple]:
        """Get courses with student enrollment count using aggregation"""
        query = """
            SELECT 
                c.id, c.name, c.code, c.duration, c.fee,
                COUNT(s.id) as student_count
            FROM courses c
            LEFT JOIN students s ON c.id = s.course_id AND s.is_active = TRUE
            WHERE c.is_active = TRUE
            GROUP BY c.id, c.name, c.code, c.duration, c.fee
            ORDER BY c.name ASC
        """
        return BaseRepository.execute_query(query)
    
    @staticmethod
    def search_courses(keyword: str) -> List[Tuple]:
        """Search courses by name or code"""
        query = """
            SELECT id, name, code, duration, fee, description
            FROM courses
            WHERE is_active = TRUE 
            AND (name ILIKE %s OR code ILIKE %s)
            ORDER BY name ASC
        """
        search_term = f"%{keyword}%"
        return BaseRepository.execute_query(query, (search_term, search_term))
