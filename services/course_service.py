from repositories.course_repository import CourseRepository
from typing import List, Dict, Optional


class CourseService:
    """Service layer for Course business logic"""
    
    @staticmethod
    def get_all_courses() -> List[Dict]:
        """Get all courses with formatted data"""
        raw_data = CourseRepository.get_all_courses()
        return [
            {
                "id": row[0],
                "name": row[1],
                "code": row[2],
                "duration": row[3],
                "fee": float(row[4]),
                "description": row[5] or "",
                "created_at": row[6]
            }
            for row in raw_data
        ]
    
    @staticmethod
    def get_course_by_id(course_id: int) -> Optional[Dict]:
        """Get single course with formatted data"""
        row = CourseRepository.get_course_by_id(course_id)
        if not row:
            return None
        
        return {
            "id": row[0],
            "name": row[1],
            "code": row[2],
            "duration": row[3],
            "fee": float(row[4]),
            "description": row[5] or ""
        }
    
    @staticmethod
    def create_course(data: Dict) -> int:
        """
        Create new course with validation
        
        Args:
            data: Dictionary containing course information
            
        Returns:
            ID of newly created course
            
        Raises:
            ValueError: If validation fails
        """
        # Validation
        if not data.get('name') or len(data['name'].strip()) < 2:
            raise ValueError("Course name must be at least 2 characters")
        
        if not data.get('code') or len(data['code'].strip()) < 2:
            raise ValueError("Course code is required")
        
        try:
            duration = int(data.get('duration', 0))
            if duration <= 0:
                raise ValueError("Duration must be greater than 0")
        except (ValueError, TypeError):
            raise ValueError("Duration must be a valid number")
        
        try:
            fee = float(data.get('fee', 0))
            if fee < 0:
                raise ValueError("Fee cannot be negative")
        except (ValueError, TypeError):
            raise ValueError("Fee must be a valid number")
        
        return CourseRepository.create_course(
            name=data['name'].strip(),
            code=data['code'].strip().upper(),
            duration=duration,
            fee=fee,
            description=data.get('description', '').strip()
        )
    
    @staticmethod
    def update_course(course_id: int, data: Dict) -> bool:
        """Update course information"""
        # Validation (similar to create)
        if not data.get('name') or len(data['name'].strip()) < 2:
            raise ValueError("Course name must be at least 2 characters")
        
        if not data.get('code') or len(data['code'].strip()) < 2:
            raise ValueError("Course code is required")
        
        try:
            duration = int(data.get('duration', 0))
            if duration <= 0:
                raise ValueError("Duration must be greater than 0")
        except (ValueError, TypeError):
            raise ValueError("Duration must be a valid number")
        
        try:
            fee = float(data.get('fee', 0))
            if fee < 0:
                raise ValueError("Fee cannot be negative")
        except (ValueError, TypeError):
            raise ValueError("Fee must be a valid number")
        
        rows_affected = CourseRepository.update_course(
            course_id=course_id,
            name=data['name'].strip(),
            code=data['code'].strip().upper(),
            duration=duration,
            fee=fee,
            description=data.get('description', '').strip()
        )
        
        return rows_affected > 0
    
    @staticmethod
    def delete_course(course_id: int) -> bool:
        """Delete course (soft delete)"""
        rows_affected = CourseRepository.delete_course(course_id)
        return rows_affected > 0
    
    @staticmethod
    def get_courses_with_student_count() -> List[Dict]:
        """Get courses with student enrollment count"""
        raw_data = CourseRepository.get_course_with_student_count()
        return [
            {
                "id": row[0],
                "name": row[1],
                "code": row[2],
                "duration": row[3],
                "fee": float(row[4]),
                "student_count": row[5]
            }
            for row in raw_data
        ]
