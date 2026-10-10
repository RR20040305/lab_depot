from django.shortcuts import render

from models import equipment as equipment_models
from models import employees as employees_models
from models import issues as issues_models


def issues(request):
    equipment_list = equipment_models.load()
    employees_list = employees_models.load()
    issue_list = issues_models.load(equipment_list, employees_list)
    return render(
        request,
        'issues/issue_list.html',
        {'issue_list': issue_list},
    )


def issue_detail(request, issue_id):
    equipment_list = equipment_models.load()
    employees_list = employees_models.load()
    issue_list = issues_models.load(equipment_list, employees_list)
    issue = issues_models.find_by_id(issue_list, issue_id)
    return render(
        request,
        'issues/issue_detail.html',
        {'issue': issue},
        status=404 if issue is None else 200,
    )