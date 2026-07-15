from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.dashboard_service import DashboardService


@login_required
def dashboard(request):
    """Display dashboard with statistics"""
    try:
        stats = DashboardService.get_dashboard_stats()
        return render(request, 'dashboard/index.html', {'stats': stats})
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, 'dashboard/index.html', {
            'stats': {
                'total_students': 0,
                'total_courses': 0,
                'total_results': 0,
                'recent_students': [],
                'top_performers': [],
                'course_stats': []
            }
        })
