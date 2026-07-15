from django.urls import path
from apps.courses import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:course_id>/update/', views.course_update, name='course_update'),
    path('<int:course_id>/delete/', views.course_delete, name='course_delete'),
]
