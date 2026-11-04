from django.shortcuts import render, get_object_or_404
from .models import Equipment

def equipment(request):
    # ORM: all()
    eqs = Equipment.objects.all()
    return render(request, 'equipment/equipment_list.html', {'equipment_list': eqs})

def equipment_detail(request, inv_num):
    eq = get_object_or_404(Equipment, pk=inv_num)
    # ORM: filter() по обратной связи (ищем активные выдачи)
    busy_info = eq.issues.filter(status='активна').first()
    
    return render(request, 'equipment/equipment_detail.html', {
        'equipment': eq,
        'busy_info': busy_info,
    })
