from django.shortcuts import render

from models import equipment as equipment_models
from models import employees as employees_models
from models import issues as issues_models


def equipment(request):
    equipment_list = equipment_models.load()
    context = {
        'equipment_list': equipment_list,
    }
    return render(request, 'equipment/equipment_list.html', context)


def equipment_detail(request, inv_num):
    equipment_list = equipment_models.load()
    eq = equipment_models.find_by_id(equipment_list, inv_num)

    if eq is not None:
        employees_list = employees_models.load()
        issues_list = issues_models.load(equipment_list, employees_list)
        busy = issues_models.is_equipment_busy(issues_list, eq)
    else:
        busy = False

    context = {
        'equipment': eq,
        'busy': busy,
    }
    return render(
        request,
        'equipment/equipment_detail.html',
        context,
        status=404 if eq is None else 200,
    )
