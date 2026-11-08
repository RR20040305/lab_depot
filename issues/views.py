from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Issue


def issues(request):
    # 1. select_related("equipment", "employee") решает проблему N+1 запроса.
    # При открытии списка выдачи, данные оборудования и сотрудников 
    # подтягиваются одним SQL-запросом с JOIN.
    qs = Issue.objects.select_related('equipment', 'employee').all()

    # Фильтрация по статусу (используем новые TextChoices)
    status_filter = request.GET.get('status')
    if status_filter:
        qs = qs.filter(status=status_filter)

    # Пагинация: по 5 записей на страницу
    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Передаем список доступных статусов для выпадающего списка в шаблоне
    statuses = Issue.Status.choices

    return render(request, 'issues/issue_list.html', {
        'issues_list': page_obj,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'statuses': statuses,
    })


def issue_detail(request, issue_id):
    # 2. get_object_or_404 - безопасное получение одного объекта.
    # 3. select_related - оптимизация для карточки выдачи.
    issue = get_object_or_404(
        Issue.objects.select_related('equipment', 'employee'), 
        pk=issue_id
    )
    
    return render(request, 'issues/issue_detail.html', {
        'issue': issue
    })


def statistics(request):
    # 4. Агрегация (aggregate) и условные выражения (Q) для статистики.
    # Считаем общее количество выдач и количество по каждому статусу.
    stats = Issue.objects.aggregate(
        total_issues=Count('id'),
        active_issues=Count('id', filter=Q(status=Issue.Status.ACTIVE)),
        cancelled_issues=Count('id', filter=Q(status=Issue.Status.CANCELLED)),
        completed_issues=Count('id', filter=Q(status=Issue.Status.COMPLETED)),
    )

    return render(request, 'issues/statistics.html', {
        'stats': stats
    })
