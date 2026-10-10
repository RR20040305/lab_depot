from django.shortcuts import render

from models import laboratories as laboratories_models


def laboratories(request):
    laboratory_list = laboratories_models.load()
    return render(
        request,
        'laboratories/laboratory_list.html',
        {'laboratory_list': laboratory_list},
    )


def laboratory_detail(request, lab_id):
    laboratory_list = laboratories_models.load()
    laboratory = laboratories_models.find_by_id(laboratory_list, lab_id)
    return render(
        request,
        'laboratories/laboratory_detail.html',
        {'laboratory': laboratory},
        status=404 if laboratory is None else 200,
    )
