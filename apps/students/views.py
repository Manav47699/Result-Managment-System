from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.student_service import StudentService
from services.course_service import CourseService


@login_required
def student_list(request):
    """Display list of all students"""
    try:
        keyword = request.GET.get('search', '')
        
        if keyword:
            students = StudentService.search_students(keyword)
        else:
            students = StudentService.get_all_students()
        
        context = {
            'students': students,
            'search_keyword': keyword
        }
        return render(request, 'students/list.html', context)
    
    except Exception as e:
        messages.error(request, f"Error loading students: {str(e)}")
        return render(request, 'students/list.html', {'students': []})


@login_required
def student_detail(request, student_id):
    """Display student details"""
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            messages.error(request, "Student not found")
            return redirect('student_list')
        
        return render(request, 'students/detail.html', {'student': student})
    
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('student_list')


@login_required
def student_create(request):
    """Create new student"""
    if request.method == 'POST':
        try:
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'gender': request.POST.get('gender'),
                'date_of_birth': request.POST.get('date_of_birth'),
                'address': request.POST.get('address'),
                'course_id': request.POST.get('course_id') or None
            }
            
            student_id = StudentService.create_student(data)
            messages.success(request, f"Student created successfully!")
            return redirect('student_list')
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Error creating student: {str(e)}")
    
    # Get courses for dropdown
    courses = CourseService.get_all_courses()
    return render(request, 'students/create.html', {'courses': courses})


@login_required
def student_update(request, student_id):
    """Update existing student"""
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            messages.error(request, "Student not found")
            return redirect('student_list')
        
        if request.method == 'POST':
            data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'gender': request.POST.get('gender'),
                'date_of_birth': request.POST.get('date_of_birth'),
                'address': request.POST.get('address'),
                'course_id': request.POST.get('course_id') or None
            }
            
            if StudentService.update_student(student_id, data):
                messages.success(request, "Student updated successfully")
                return redirect('student_list')
            else:
                messages.error(request, "Failed to update student")
        
        courses = CourseService.get_all_courses()
        context = {
            'student': student,
            'courses': courses
        }
        return render(request, 'students/update.html', context)
    
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('student_list')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('student_list')


@login_required
def student_delete(request, student_id):
    """Delete student"""
    try:
        if StudentService.delete_student(student_id):
            messages.success(request, "Student deleted successfully")
        else:
            messages.error(request, "Failed to delete student")
    except Exception as e:
        messages.error(request, f"Error deleting student: {str(e)}")
    
    return redirect('student_list')
