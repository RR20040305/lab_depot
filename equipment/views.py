from django.http import HttpResponse

from homepage.views import page
from models import equipment as equipment_models
from models import employees as employees_models
from models import issues as issues_models


def equipment(request):
    equipment_list = equipment_models.load()
    items = ''
    for eq in equipment_list:
        items += f"""
        <li class="list-group-item">
            <a href="/equipment/{eq.inv_num}/">
                {eq.inv_num}: {eq.name} — {eq.status}
            </a>
        </li>
        """
    content = f"""
    <h1>Оборудование</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('lab_depot — оборудование', content))


def equipment_detail(request, inv_num):
    equipment_list = equipment_models.load()
    eq = equipment_models.find_by_id(equipment_list, inv_num)

    if eq is None:
        content = """
        <h1 class="text-danger">Оборудование не найдено</h1>
        <a href="/equipment/"
           class="btn btn-outline-secondary">← к списку оборудования</a>
        """
        return HttpResponse(
            page('Оборудование не найдено', content),
            status=404,
        )

    # Проверяем, выдано ли оборудование прямо сейчас
    employees_list = employees_models.load()
    issues_list = issues_models.load(equipment_list, employees_list)
    busy = issues_models.is_equipment_busy(issues_list, eq)

    status = 'выдано' if busy else 'доступно'
    badge = 'bg-warning' if busy else 'bg-success'

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{eq.name}</h5>
            <p class="card-text"><strong>Инвентарный номер:</strong> {eq.inv_num}</p>
            <p class="card-text"><strong>Состояние:</strong> {eq.status}</p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/equipment/"
               class="btn btn-outline-secondary">← к списку оборудования</a>
        </div>
    </div>
    """
    return HttpResponse(page(eq.name, content))