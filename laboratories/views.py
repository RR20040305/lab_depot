from django.http import HttpResponse

from homepage.views import page
from models import laboratories as laboratories_models


def laboratories(request):
    labs_list = laboratories_models.load()
    items = ''
    for lab in labs_list:
        items += f"""
        <li class="list-group-item">
            <a href="/laboratories/{lab.lab_id}/">
                {lab.lab_id}: {lab.responsible} — {lab.location}
            </a>
        </li>
        """
    content = f"""
    <h1>Лаборатории</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page('lab_depot — лаборатории', content))


def laboratory_detail(request, lab_id):
    labs_list = laboratories_models.load()
    lab = laboratories_models.find_by_id(labs_list, lab_id)

    if lab is None:
        content = """
        <h1 class="text-danger">Лаборатория не найдена</h1>
        <a href="/laboratories/"
           class="btn btn-outline-secondary">← к списку лабораторий</a>
        """
        return HttpResponse(
            page('Лаборатория не найдена', content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Лаборатория {lab.lab_id}</h5>
            <p class="card-text"><strong>Ответственный:</strong> {lab.responsible}</p>
            <p class="card-text"><strong>Расположение:</strong> {lab.location}</p>
            <a href="/laboratories/"
               class="btn btn-outline-secondary">← к списку лабораторий</a>
        </div>
    </div>
    """
    return HttpResponse(page(f'Лаборатория {lab.lab_id}', content))