from repositories.base_repository import BaseRepository
from typing import List, Tuple, Optional


class ResultRepository(BaseRepository):
    """Repository for Result entity using raw SQL"""
    
    @staticmethod
    def get_all_results() -> List[Tuple]:
        """Fetch all results with student and course info using JOIN"""
        query = """
            SELECT 
                r.id, r.subject_name, r.marks_obtained, r.total_marks, 
                r.grade, r.exam_date,
                s.id as student_id, s.name as student_name,
                c.id as course_id, c.name as course_name,
                ROUND((r.marks_obtained / r.total_marks * 100), 2) as percentage
            FROM results r
            INNER JOIN students s ON r.student_id = s.id
            INNER JOIN courses c ON r.course_id = c.id
            ORDER BY r.exam_date DESC, s.name ASC
        """
        return BaseRepository.execute_query(query)
    
    @staticmethod
    def get_results_by_student(student_id: int) -> List[Tuple]:
        """Fetch all results for a specific student"""
        query = """
            SELECT 
                r.id, r.subject_name, r.marks_obtained, r.total_marks,
                r.grade, r.exam_date, r.remarks,
                c.name as course_name,
                ROUND((r.marks_obtained / r.total_marks * 100), 2) as percentage
            FROM results r
            INNER JOIN courses c ON r.course_id = c.id
            WHERE r.student_id = %s
            ORDER BY r.exam_date DESC
        """
        return BaseRepository.execute_query(query, (student_id,))
    
    @staticmethod
    def get_result_by_id(result_id: int) -> Optional[Tuple]:
        """Fetch single result by ID"""
        query = """
            SELECT 
                r.id, r.student_id, r.course_id, r.subject_name,
                r.marks_obtained, r.total_marks, r.grade, r.exam_date, r.remarks,
                s.name as student_name, c.name as course_name
            FROM results r
            INNER JOIN students s ON r.student_id = s.id
            INNER JOIN courses c ON r.course_id = c.id
            WHERE r.id = %s
        """
        results = BaseRepository.execute_query(query, (result_id,))
        return results[0] if results else None
    
    @staticmethod
    def create_result(student_id: int, course_id: int, subject_name: str,
                     marks_obtained: float, total_marks: float, 
                     grade: str, exam_date: str, remarks: str) -> int:
        """Insert a new result"""
        query = """
            INSERT INTO results 
            (student_id, course_id, subject_name, marks_obtained, 
             total_marks, grade, exam_date, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        return BaseRepository.execute_insert(query, (student_id, course_id, subject_name,
                                                     marks_obtained, total_marks, grade, 
                                                     exam_date, remarks))
    
    @staticmethod
    def update_result(result_id: int, subject_name: str, marks_obtained: float,
                     total_marks: float, grade: str, exam_date: str, remarks: str) -> int:
        """Update result information"""
        query = """
            UPDATE results
            SET subject_name = %s, marks_obtained = %s, total_marks = %s,
                grade = %s, exam_date = %s, remarks = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        return BaseRepository.execute_update(query, (subject_name, marks_obtained, 
                                                     total_marks, grade, exam_date, 
                                                     remarks, result_id))
    
    @staticmethod
    def delete_result(result_id: int) -> int:
        """Hard delete a result"""
        query = "DELETE FROM results WHERE id = %s"
        return BaseRepository.execute_delete(query, (result_id,))
    
    @staticmethod
    def get_student_aggregate_results(student_id: int) -> Optional[Tuple]:
        """Get aggregate results for a student using SQL aggregation"""
        query = """
            SELECT 
                COUNT(*) as total_subjects,
                SUM(marks_obtained) as total_marks_obtained,
                SUM(total_marks) as total_marks_possible,
                ROUND(AVG(marks_obtained / total_marks * 100), 2) as average_percentage
            FROM results
            WHERE student_id = %s
        """
        results = BaseRepository.execute_query(query, (student_id,))
        return results[0] if results else None
    
    @staticmethod
    def get_results_by_course(course_id: int) -> List[Tuple]:
        """Get all results for a specific course"""
        query = """
            SELECT 
                r.id, r.subject_name, r.marks_obtained, r.total_marks,
                r.grade, s.name as student_name,
                ROUND((r.marks_obtained / r.total_marks * 100), 2) as percentage
            FROM results r
            INNER JOIN students s ON r.student_id = s.id
            WHERE r.course_id = %s
            ORDER BY s.name ASC
        """
        return BaseRepository.execute_query(query, (course_id,))
    
    @staticmethod
    def search_results(keyword: str) -> List[Tuple]:
        """Search results by student name or subject"""
        query = """
            SELECT 
                r.id, r.subject_name, r.marks_obtained, r.total_marks,
                s.name as student_name, c.name as course_name
            FROM results r
            INNER JOIN students s ON r.student_id = s.id
            INNER JOIN courses c ON r.course_id = c.id
            WHERE s.name ILIKE %s OR r.subject_name ILIKE %s
            ORDER BY s.name ASC
        """
        search_term = f"%{keyword}%"
        return BaseRepository.execute_query(query, (search_term, search_term))
