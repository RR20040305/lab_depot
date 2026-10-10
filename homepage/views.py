from django.http import HttpResponse

BOOTSTRAP_CSS = (
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3'
    '/dist/css/bootstrap.min.css'
)


def page(title: str, content: str) -> str:
    """Единый HTML-каркас для всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="nav bg-light mb-4 px-3 py-2">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/equipment/">Оборудование</a>
        <a class="nav-link" href="/laboratories/">Лаборатории</a>
        <a class="nav-link" href="/employees/">Сотрудники</a>
        <a class="nav-link" href="/issues/">Выдачи</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">lab_depot</h1>
    <p class="lead">Система учёта лабораторного оборудования.</p>
    <p>Основные разделы:</p>
    <a href="/equipment/" class="btn btn-primary me-2">Оборудование</a>
    <a href="/laboratories/" class="btn btn-primary me-2">Лаборатории</a>
    <a href="/employees/" class="btn btn-primary me-2">Сотрудники</a>
    <a href="/issues/" class="btn btn-secondary">Выдачи</a>
    """
    return HttpResponse(page('lab_depot', content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page('404 — страница не найдена', content),
        status=404,
    )

