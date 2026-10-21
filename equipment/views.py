import sqlite3
from django.shortcuts import render

DB_PATH = "data/lab_depot.sqlite"


def equipment(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    equipment_list = conn.execute("""
        SELECT inv_num, name, status FROM equipment ORDER BY name;
    """).fetchall()
    conn.close()

    return render(request, 'equipment/equipment_list.html', {'equipment_list': equipment_list})


def equipment_detail(request, inv_num):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Получаем оборудование
    eq = conn.execute("""
        SELECT inv_num, name, status FROM equipment WHERE inv_num = ?;
    """, (inv_num,)).fetchone()

    if eq is None:
        conn.close()
        return render(request, 'equipment/equipment_detail.html', {'equipment': None}, status=404)

    # Проверяем, выдано ли оно сейчас (JOIN)
    busy_info = conn.execute("""
        SELECT i.return_date, emp.fio 
        FROM issues i
        JOIN employees emp ON i.emp_id = emp.emp_id
        WHERE i.inv_num = ? AND i.status = 'активна';
    """, (inv_num,)).fetchone()
    conn.close()

    return render(request, 'equipment/equipment_detail.html', {
        'equipment': eq,
        'busy_info': busy_info,
    })

def available_equipment(request):
    status_filter = request.GET.get('status', 'исправно')
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Ищем оборудование нужного статуса, которое НЕ ВЫДАНО (нет активных выдач)
    available = conn.execute("""
        SELECT inv_num, name, status
        FROM equipment
        WHERE status = ?
          AND inv_num NOT IN (
              SELECT inv_num FROM issues WHERE status = 'активна'
          )
        ORDER BY name;
    """, (status_filter,)).fetchall()
    conn.close()

    return render(request, 'equipment/available.html', {
        'available_list': available,
        'status_filter': status_filter,
    })