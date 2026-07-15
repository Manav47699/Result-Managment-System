from repositories.student_repository import StudentRepository
from typing import List, Dict, Optional


class StudentService:
    """Service layer for Student business logic"""
    
    @staticmethod
    def get_all_students() -> List[Dict]:
        """
        Get all students with formatted data
        
        Returns:
            List of student dictionaries
        """
        raw_data = StudentRepository.get_all_students()
        return [
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3] or "",
                "gender": row[4] or "",
                "date_of_birth": row[5],
                "address": row[6] or "",
                "enrollment_date": row[7],
                "course_id": row[8],
                "course_name": row[9] if row[9] else "Not Enrolled",
                "course_code": row[10] if len(row) > 10 and row[10] else ""
            }
            for row in raw_data
        ]
    
    @staticmethod
    def get_student_by_id(student_id: int) -> Optional[Dict]:
        """Get single student with formatted data"""
        row = StudentRepository.get_student_by_id(student_id)
        if not row:
            return None
        
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3] or "",
            "gender": row[4] or "",
            "date_of_birth": row[5],
            "address": row[6] or "",
            "enrollment_date": row[7],
            "course_id": row[8],
            "course_name": row[9] if row[9] else "Not Enrolled"
        }
    
    @staticmethod
    def create_student(data: Dict) -> int:
        """
        Create new student with validation
        
        Args:
            data: Dictionary containing student information
            
        Returns:
            ID of newly created student
            
        Raises:
            ValueError: If validation fails
        """
        # Validation
        if not data.get('name') or len(data['name'].strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        
        if not data.get('email') or '@' not in data['email']:
            raise ValueError("Valid email is required")
        
        return StudentRepository.create_student(
            name=data['name'].strip(),
            email=data['email'].strip(),
            phone=data.get('phone', '').strip(),
            gender=data.get('gender', 'Other'),
            date_of_birth=data.get('date_of_birth') or None,
            address=data.get('address', '').strip(),
            course_id=data.get('course_id') or None
        )
    
    @staticmethod
    def update_student(student_id: int, data: Dict) -> bool:
        """Update student information"""
        # Validation
        if not data.get('name') or len(data['name'].strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        
        if not data.get('email') or '@' not in data['email']:
            raise ValueError("Valid email is required")
        
        rows_affected = StudentRepository.update_student(
            student_id=student_id,
            name=data['name'].strip(),
            email=data['email'].strip(),
            phone=data.get('phone', '').strip(),
            gender=data.get('gender', 'Other'),
            date_of_birth=data.get('date_of_birth') or None,
            address=data.get('address', '').strip(),
            course_id=data.get('course_id') or None
        )
        
        return rows_affected > 0
    
    @staticmethod
    def delete_student(student_id: int) -> bool:
        """Delete student (soft delete)"""
        rows_affected = StudentRepository.delete_student(student_id)
        return rows_affected > 0
    
    @staticmethod
    def search_students(keyword: str) -> List[Dict]:
        """Search students by keyword"""
        if not keyword or len(keyword.strip()) < 2:
            return StudentService.get_all_students()
        
        raw_data = StudentRepository.search_students(keyword.strip())
        return [
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3] or "",
                "gender": row[4] or "",
                "course_name": row[5] if row[5] else "Not Enrolled"
            }
            for row in raw_data
        ]
