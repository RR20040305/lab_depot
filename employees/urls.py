from django.urls import path

from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employees, name='list'),
    path('<str:emp_id>/', views.employee_detail, name='detail'),
]
