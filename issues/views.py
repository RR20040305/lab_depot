from django.http import HttpResponse

from homepage.views import page
from models import equipment as equipment_models
from models import employees as employees_models
from models import issues as issues_models


def issues(request):
    equipment_list = equipment_models.load()
    employees_list = employees_models.load()
    issues_list = issues_models.load(equipment_list, employees_list)

    items = ''
    for issue in issues_list:
        status = 'отменено' if not issue.is_active() else 'активно'
        badge = 'bg-secondary' if not issue.is_active() else 'bg-success'
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/issues/{issue.id}/">
                {issue.equipment.name} — {issue.employee.fio} (до {issue.return_date})
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Выдачи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('lab_depot — выдачи', content))


def issue_detail(request, issue_id):
    equipment_list = equipment_models.load()
    employees_list = employees_models.load()
    issues_list = issues_models.load(equipment_list, employees_list)

    issue = issues_models.find_by_id(issues_list, issue_id)

    if issue is None:
        content = """
        <h1 class="text-danger">Выдача не найдена</h1>
        <a href="/issues/"
           class="btn btn-outline-secondary">← к списку выдач</a>
        """
        return HttpResponse(
            page('Выдача не найдена', content),
            status=404,
        )

    status = 'отменено' if not issue.is_active() else 'активно'
    badge = 'bg-secondary' if not issue.is_active() else 'bg-success'

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Выдача №{issue.id}</h5>
            <p class="card-text"><strong>Оборудование:</strong>
                <a href="/equipment/{issue.equipment.inv_num}/">
                    {issue.equipment.name} ({issue.equipment.inv_num})
                </a>
            </p>
            <p class="card-text"><strong>Сотрудник:</strong>
                <a href="/employees/{issue.employee.emp_id}/">
                    {issue.employee.fio}
                </a>
            </p>
            <p class="card-text"><strong>Дата возврата:</strong> {issue.return_date}</p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/issues/"
               class="btn btn-outline-secondary">← к списку выдач</a>
        </div>
    </div>
    """
    return HttpResponse(page(f'Выдача №{issue.id}', content))