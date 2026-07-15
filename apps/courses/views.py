from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.course_service import CourseService


@login_required
def course_list(request):
    """Display list of all courses"""
    try:
        courses = CourseService.get_courses_with_student_count()
        return render(request, 'courses/list.html', {'courses': courses})
    except Exception as e:
        messages.error(request, f"Error loading courses: {str(e)}")
        return render(request, 'courses/list.html', {'courses': []})


@login_required
def course_create(request):
    """Create new course"""
    if request.method == 'POST':
        try:
            data = {
                'name': request.POST.get('name'),
                'code': request.POST.get('code'),
                'duration': request.POST.get('duration'),
                'fee': request.POST.get('fee'),
                'description': request.POST.get('description')
            }
            
            course_id = CourseService.create_course(data)
            messages.success(request, "Course created successfully!")
            return redirect('course_list')
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Error creating course: {str(e)}")
    
    return render(request, 'courses/create.html')


@login_required
def course_update(request, course_id):
    """Update existing course"""
    try:
        course = CourseService.get_course_by_id(course_id)
        if not course:
            messages.error(request, "Course not found")
            return redirect('course_list')
        
        if request.method == 'POST':
            data = {
                'name': request.POST.get('name'),
                'code': request.POST.get('code'),
                'duration': request.POST.get('duration'),
                'fee': request.POST.get('fee'),
                'description': request.POST.get('description')
            }
            
            if CourseService.update_course(course_id, data):
                messages.success(request, "Course updated successfully")
                return redirect('course_list')
            else:
                messages.error(request, "Failed to update course")
        
        return render(request, 'courses/update.html', {'course': course})
    
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('course_list')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('course_list')


@login_required
def course_delete(request, course_id):
    """Delete course"""
    try:
        if CourseService.delete_course(course_id):
            messages.success(request, "Course deleted successfully")
        else:
            messages.error(request, "Failed to delete course")
    except Exception as e:
        messages.error(request, f"Error deleting course: {str(e)}")
    
    return redirect('course_list')
