from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Equipment
from issues.models import Issue

def equipment(request):
    query = request.GET.get("q", "").strip()
    equipment_list = Equipment.objects.all()

    # Поиск по названию или инвентарному номеру с помощью Q-объектов
    if query:
        equipment_list = equipment_list.filter(
            Q(name__icontains=query) | Q(inv_num__icontains=query)
        )

    # Аннотирование: подсчет количества выдач для каждого оборудования
    equipment_list = equipment_list.annotate(issue_count=Count('issues'))

    return render(request, 'equipment/equipment_list.html', {
        'equipment_list': equipment_list,
        'search_query': query
    })

def equipment_detail(request, inv_num):
    # Получаем оборудование по первичному ключу или 404
    eq = get_object_or_404(Equipment, pk=inv_num)
    
    # Ищем активную выдачу для этого оборудования
    busy_info = Issue.objects.filter(
        equipment=eq, 
        status=Issue.Status.ACTIVE
    ).select_related('employee').first()
    
    return render(request, 'equipment/equipment_detail.html', {
        'equipment': eq,
        'busy_info': busy_info,
    })

def available_equipment(request):
    status_filter = request.GET.get('status', 'исправно')
    
    # Ищем оборудование нужного статуса, у которого нет активных выдач
    available_list = Equipment.objects.filter(
        status=status_filter
    ).exclude(
        issues__status=Issue.Status.ACTIVE
    ).order_by('name')
    
    return render(request, 'equipment/available.html', {
        'available_list': available_list,
        'status_filter': status_filter,
    })
