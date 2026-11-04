from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Issue
from equipment.models import Equipment

def issues(request):
    # Базовый QuerySet с JOIN-оптимизацией
    qs = Issue.objects.select_related('equipment', 'employee').all()

    # Фильтрация
    status_filter = request.GET.get('status')
    if status_filter:
        qs = qs.filter(status=status_filter)

    # Сортировка
    sort = request.GET.get('sort', 'date_desc')
    if sort == 'date_asc':
        qs = qs.order_by('return_date')
    elif sort == 'eq_name':
        qs = qs.order_by('equipment__name')
    else:
        qs = qs.order_by('-return_date')

    # Пагинация (по 5 записей)
    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'issues/issue_list.html', {
        'issues_list': page_obj,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'sort': sort,
    })

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue.objects.select_related('equipment', 'employee'), pk=issue_id)
    return render(request, 'issues/issue_detail.html', {'issue': issue})

def statistics(request):
    # ORM: Агрегация и аннотирование
    total_eq = Equipment.objects.aggregate(total=Count('inv_num'))['total']
    active_issues = Issue.objects.filter(status='активна').count()
    
    # Аннотирование: считаем количество выдач для каждого оборудования
    eq_stats = Equipment.objects.annotate(issue_count=Count('issues')).order_by('-issue_count')

    return render(request, 'issues/statistics.html', {
        'total_eq': total_eq,
        'active_issues': active_issues,
        'eq_stats': eq_stats,
    })
