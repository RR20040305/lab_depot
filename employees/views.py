from django.http import HttpResponse

from homepage.views import page
from models import employees as employees_models


def employees(request):
    emp_list = employees_models.load()
    items = ''
    for emp in emp_list:
        items += f"""
        <li class="list-group-item">
            <a href="/employees/{emp.emp_id}/">
                {emp.emp_id}: {emp.fio} — {emp.position}
            </a>
        </li>
        """
    content = f"""
    <h1>Сотрудники</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('lab_depot — сотрудники', content))


def employee_detail(request, emp_id):
    emp_list = employees_models.load()
    emp = employees_models.find_by_id(emp_list, emp_id)

    if emp is None:
        content = """
        <h1 class="text-danger">Сотрудник не найден</h1>
        <a href="/employees/"
           class="btn btn-outline-secondary">← к списку сотрудников</a>
        """
        return HttpResponse(
            page('Сотрудник не найден', content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{emp.fio}</h5>
            <p class="card-text"><strong>Табельный номер:</strong> {emp.emp_id}</p>
            <p class="card-text"><strong>Должность:</strong> {emp.position}</p>
            <p class="card-text"><strong>Лаборатория:</strong> {emp.lab}</p>
            <a href="/employees/"
               class="btn btn-outline-secondary">← к списку сотрудников</a>
        </div>
    </div>
    """
    return HttpResponse(page(emp.fio, content))