from repositories.result_repository import ResultRepository
from typing import List, Dict, Optional


class ResultService:
    """Service layer for Result business logic"""
    
    @staticmethod
    def calculate_grade(percentage: float) -> str:
        """Calculate grade based on percentage"""
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    @staticmethod
    def get_all_results() -> List[Dict]:
        """Get all results with formatted data"""
        raw_data = ResultRepository.get_all_results()
        return [
            {
                "id": row[0],
                "subject_name": row[1],
                "marks_obtained": float(row[2]),
                "total_marks": float(row[3]),
                "grade": row[4] or "",
                "exam_date": row[5],
                "student_id": row[6],
                "student_name": row[7],
                "course_id": row[8],
                "course_name": row[9],
                "percentage": float(row[10])
            }
            for row in raw_data
        ]
    
    @staticmethod
    def get_results_by_student(student_id: int) -> List[Dict]:
        """Get all results for a specific student"""
        raw_data = ResultRepository.get_results_by_student(student_id)
        return [
            {
                "id": row[0],
                "subject_name": row[1],
                "marks_obtained": float(row[2]),
                "total_marks": float(row[3]),
                "grade": row[4] or "",
                "exam_date": row[5],
                "remarks": row[6] or "",
                "course_name": row[7],
                "percentage": float(row[8])
            }
            for row in raw_data
        ]
    
    @staticmethod
    def get_result_by_id(result_id: int) -> Optional[Dict]:
        """Get single result with formatted data"""
        row = ResultRepository.get_result_by_id(result_id)
        if not row:
            return None
        
        return {
            "id": row[0],
            "student_id": row[1],
            "course_id": row[2],
            "subject_name": row[3],
            "marks_obtained": float(row[4]),
            "total_marks": float(row[5]),
            "grade": row[6] or "",
            "exam_date": row[7],
            "remarks": row[8] or "",
            "student_name": row[9],
            "course_name": row[10]
        }
    
    @staticmethod
    def create_result(data: Dict) -> int:
        """
        Create new result with validation
        
        Args:
            data: Dictionary containing result information
            
        Returns:
            ID of newly created result
            
        Raises:
            ValueError: If validation fails
        """
        # Validation
        try:
            student_id = int(data.get('student_id', 0))
            if student_id <= 0:
                raise ValueError("Valid student is required")
        except (ValueError, TypeError):
            raise ValueError("Valid student is required")
        
        try:
            course_id = int(data.get('course_id', 0))
            if course_id <= 0:
                raise ValueError("Valid course is required")
        except (ValueError, TypeError):
            raise ValueError("Valid course is required")
        
        if not data.get('subject_name') or len(data['subject_name'].strip()) < 2:
            raise ValueError("Subject name is required")
        
        try:
            marks_obtained = float(data.get('marks_obtained', 0))
            total_marks = float(data.get('total_marks', 0))
            
            if marks_obtained < 0:
                raise ValueError("Marks obtained cannot be negative")
            if total_marks <= 0:
                raise ValueError("Total marks must be greater than 0")
            if marks_obtained > total_marks:
                raise ValueError("Marks obtained cannot exceed total marks")
        except (ValueError, TypeError) as e:
            if "cannot" in str(e) or "must" in str(e):
                raise
            raise ValueError("Marks must be valid numbers")
        
        # Calculate grade
        percentage = (marks_obtained / total_marks) * 100
        grade = ResultService.calculate_grade(percentage)
        
        return ResultRepository.create_result(
            student_id=student_id,
            course_id=course_id,
            subject_name=data['subject_name'].strip(),
            marks_obtained=marks_obtained,
            total_marks=total_marks,
            grade=grade,
            exam_date=data.get('exam_date') or None,
            remarks=data.get('remarks', '').strip()
        )
    
    @staticmethod
    def update_result(result_id: int, data: Dict) -> bool:
        """Update result information"""
        # Validation
        if not data.get('subject_name') or len(data['subject_name'].strip()) < 2:
            raise ValueError("Subject name is required")
        
        try:
            marks_obtained = float(data.get('marks_obtained', 0))
            total_marks = float(data.get('total_marks', 0))
            
            if marks_obtained < 0:
                raise ValueError("Marks obtained cannot be negative")
            if total_marks <= 0:
                raise ValueError("Total marks must be greater than 0")
            if marks_obtained > total_marks:
                raise ValueError("Marks obtained cannot exceed total marks")
        except (ValueError, TypeError) as e:
            if "cannot" in str(e) or "must" in str(e):
                raise
            raise ValueError("Marks must be valid numbers")
        
        # Calculate grade
        percentage = (marks_obtained / total_marks) * 100
        grade = ResultService.calculate_grade(percentage)
        
        rows_affected = ResultRepository.update_result(
            result_id=result_id,
            subject_name=data['subject_name'].strip(),
            marks_obtained=marks_obtained,
            total_marks=total_marks,
            grade=grade,
            exam_date=data.get('exam_date') or None,
            remarks=data.get('remarks', '').strip()
        )
        
        return rows_affected > 0
    
    @staticmethod
    def delete_result(result_id: int) -> bool:
        """Delete result"""
        rows_affected = ResultRepository.delete_result(result_id)
        return rows_affected > 0
    
    @staticmethod
    def get_student_summary(student_id: int) -> Optional[Dict]:
        """Get summary statistics for a student"""
        row = ResultRepository.get_student_aggregate_results(student_id)
        if not row or row[0] == 0:
            return None
        
        return {
            "total_subjects": row[0],
            "total_marks_obtained": float(row[1]) if row[1] else 0,
            "total_marks_possible": float(row[2]) if row[2] else 0,
            "average_percentage": float(row[3]) if row[3] else 0,
            "overall_grade": ResultService.calculate_grade(float(row[3])) if row[3] else 'N/A'
        }
