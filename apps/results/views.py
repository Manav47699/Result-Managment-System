from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.result_service import ResultService
from services.student_service import StudentService
from services.course_service import CourseService


@login_required
def result_list(request):
    """Display list of all results"""
    try:
        results = ResultService.get_all_results()
        return render(request, 'results/list.html', {'results': results})
    except Exception as e:
        messages.error(request, f"Error loading results: {str(e)}")
        return render(request, 'results/list.html', {'results': []})


@login_required
def result_create(request):
    """Create new result"""
    if request.method == 'POST':
        try:
            data = {
                'student_id': request.POST.get('student_id'),
                'course_id': request.POST.get('course_id'),
                'subject_name': request.POST.get('subject_name'),
                'marks_obtained': request.POST.get('marks_obtained'),
                'total_marks': request.POST.get('total_marks'),
                'exam_date': request.POST.get('exam_date'),
                'remarks': request.POST.get('remarks')
            }
            
            result_id = ResultService.create_result(data)
            messages.success(request, "Result created successfully!")
            return redirect('result_list')
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Error creating result: {str(e)}")
    
    # Get students and courses for dropdowns
    students = StudentService.get_all_students()
    courses = CourseService.get_all_courses()
    return render(request, 'results/create.html', {
        'students': students,
        'courses': courses
    })


@login_required
def result_update(request, result_id):
    """Update existing result"""
    try:
        result = ResultService.get_result_by_id(result_id)
        if not result:
            messages.error(request, "Result not found")
            return redirect('result_list')
        
        if request.method == 'POST':
            data = {
                'subject_name': request.POST.get('subject_name'),
                'marks_obtained': request.POST.get('marks_obtained'),
                'total_marks': request.POST.get('total_marks'),
                'exam_date': request.POST.get('exam_date'),
                'remarks': request.POST.get('remarks')
            }
            
            if ResultService.update_result(result_id, data):
                messages.success(request, "Result updated successfully")
                return redirect('result_list')
            else:
                messages.error(request, "Failed to update result")
        
        return render(request, 'results/update.html', {'result': result})
    
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('result_list')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('result_list')


@login_required
def result_delete(request, result_id):
    """Delete result"""
    try:
        if ResultService.delete_result(result_id):
            messages.success(request, "Result deleted successfully")
        else:
            messages.error(request, "Failed to delete result")
    except Exception as e:
        messages.error(request, f"Error deleting result: {str(e)}")
    
    return redirect('result_list')


@login_required
def result_by_student(request, student_id):
    """View results for a specific student"""
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            messages.error(request, "Student not found")
            return redirect('student_list')
        
        results = ResultService.get_results_by_student(student_id)
        summary = ResultService.get_student_summary(student_id)
        
        context = {
            'student': student,
            'results': results,
            'summary': summary
        }
        return render(request, 'results/by_student.html', context)
    
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('student_list')
