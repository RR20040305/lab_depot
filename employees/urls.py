from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name='employees'),
    path('<str:emp_id>/', views.employee_detail, name='employee_detail'),
]