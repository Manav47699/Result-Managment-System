from django.urls import path
from apps.results import views

urlpatterns = [
    path('', views.result_list, name='result_list'),
    path('create/', views.result_create, name='result_create'),
    path('<int:result_id>/update/', views.result_update, name='result_update'),
    path('<int:result_id>/delete/', views.result_delete, name='result_delete'),
    path('student/<int:student_id>/', views.result_by_student, name='result_by_student'),
]
