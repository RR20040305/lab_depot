import sqlite3
from django.shortcuts import render

DB_PATH = "data/lab_depot.sqlite"


def laboratories(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    laboratories_list = conn.execute("""
        SELECT lab_id, responsible, location FROM laboratories ORDER BY lab_id;
    """).fetchall()
    conn.close()
    return render(request, 'laboratories/laboratory_list.html', {'laboratories_list': laboratories_list})

def laboratory_detail(request, lab_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Получаем саму лабораторию по ID
    lab = conn.execute("""
        SELECT lab_id, responsible, location 
        FROM laboratories 
        WHERE lab_id = ?;
    """, (lab_id,)).fetchone()
    
    if lab is None:
        conn.close()
        return render(
            request, 
            'laboratories/laboratory_detail.html', 
            {'laboratory': None}, 
            status=404
        )
        
    # Дополнительно: получаем список сотрудников этой лаборатории (JOIN/WHERE)
    employees_in_lab = conn.execute("""
        SELECT emp_id, fio, position 
        FROM employees 
        WHERE lab_id = ?;
    """, (lab_id,)).fetchall()
    
    conn.close()
    
    return render(request, 'laboratories/laboratory_detail.html', {
        'laboratory': lab,
        'employees_in_lab': employees_in_lab
    })
