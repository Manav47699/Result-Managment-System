from repositories.base_repository import BaseRepository
from typing import Dict


class DashboardService:
    """Service layer for Dashboard analytics"""
    
    @staticmethod
    def get_dashboard_stats() -> Dict:
        """
        Get dashboard statistics using SQL aggregation
        
        Returns:
            Dictionary containing counts and analytics
        """
        # Count students
        student_count_query = "SELECT COUNT(*) FROM students WHERE is_active = TRUE"
        student_count = BaseRepository.execute_query(student_count_query)[0][0]
        
        # Count courses
        course_count_query = "SELECT COUNT(*) FROM courses WHERE is_active = TRUE"
        course_count = BaseRepository.execute_query(course_count_query)[0][0]
        
        # Count results
        result_count_query = "SELECT COUNT(*) FROM results"
        result_count = BaseRepository.execute_query(result_count_query)[0][0]
        
        # Get recent students (last 5 enrollments)
        recent_students_query = """
            SELECT s.name, c.name as course_name, s.enrollment_date
            FROM students s
            LEFT JOIN courses c ON s.course_id = c.id
            WHERE s.is_active = TRUE
            ORDER BY s.enrollment_date DESC
            LIMIT 5
        """
        recent_students_raw = BaseRepository.execute_query(recent_students_query)
        recent_students = [
            {
                "name": row[0],
                "course": row[1] if row[1] else "Not Enrolled",
                "enrollment_date": row[2]
            }
            for row in recent_students_raw
        ]
        
        # Get top performing students (top 5 by average percentage)
        top_performers_query = """
            SELECT 
                s.name,
                c.name as course_name,
                ROUND(AVG(r.marks_obtained / r.total_marks * 100), 2) as avg_percentage
            FROM results r
            INNER JOIN students s ON r.student_id = s.id
            INNER JOIN courses c ON r.course_id = c.id
            WHERE s.is_active = TRUE
            GROUP BY s.id, s.name, c.name
            HAVING COUNT(r.id) > 0
            ORDER BY avg_percentage DESC
            LIMIT 5
        """
        top_performers_raw = BaseRepository.execute_query(top_performers_query)
        top_performers = [
            {
                "name": row[0],
                "course": row[1],
                "percentage": float(row[2])
            }
            for row in top_performers_raw
        ]
        
        # Get course enrollment statistics
        course_stats_query = """
            SELECT 
                c.name,
                COUNT(s.id) as student_count
            FROM courses c
            LEFT JOIN students s ON c.id = s.course_id AND s.is_active = TRUE
            WHERE c.is_active = TRUE
            GROUP BY c.id, c.name
            ORDER BY student_count DESC
            LIMIT 5
        """
        course_stats_raw = BaseRepository.execute_query(course_stats_query)
        course_stats = [
            {
                "course_name": row[0],
                "student_count": row[1]
            }
            for row in course_stats_raw
        ]
        
        return {
            "total_students": student_count,
            "total_courses": course_count,
            "total_results": result_count,
            "recent_students": recent_students,
            "top_performers": top_performers,
            "course_stats": course_stats
        }
