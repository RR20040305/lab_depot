from django.shortcuts import render, get_object_or_404
from .models import Employee

def employees(request):
    # ORM: select_related для оптимизации (JOIN)
    emps = Employee.objects.select_related('lab').all()
    return render(request, 'employees/employee_list.html', {'employees_list': emps})

def employee_detail(request, emp_id):
    emp = get_object_or_404(Employee.objects.select_related('lab'), pk=emp_id)
    return render(request, 'employees/employee_detail.html', {'employee': emp})
