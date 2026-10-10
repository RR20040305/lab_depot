from django.shortcuts import render

from models import employees as employees_models


def employees(request):
    employee_list = employees_models.load()
    return render(
        request,
        'employees/employee_list.html',
        {'employee_list': employee_list},
    )


def employee_detail(request, emp_id):
    employee_list = employees_models.load()
    employee = employees_models.find_by_id(employee_list, emp_id)
    return render(
        request,
        'employees/employee_detail.html',
        {'employee': employee},
        status=404 if employee is None else 200,
    )
