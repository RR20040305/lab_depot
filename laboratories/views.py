from django.shortcuts import render, get_object_or_404
from .models import Laboratory
from employees.models import Employee

def laboratories(request):
    # ORM: all() + сортировка из Meta
    labs = Laboratory.objects.all()
    return render(request, 'laboratories/laboratory_list.html', {'laboratories_list': labs})

def laboratory_detail(request, lab_id):
    # ORM: get_object_or_404
    lab = get_object_or_404(Laboratory, pk=lab_id)
    # ORM: обратная связь related_name="employees"
    employees_in_lab = lab.employees.all()
    return render(request, 'laboratories/laboratory_detail.html', {
        'laboratory': lab,
        'employees_in_lab': employees_in_lab
    })
