import sqlite3
from django.shortcuts import render

DB_PATH = "data/lab_depot.sqlite"


def employees(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    employees_list = conn.execute("""
        SELECT e.emp_id, e.fio, e.position, e.lab_id, l.location AS lab_location
        FROM employees e
        LEFT JOIN laboratories l ON e.lab_id = l.lab_id
        ORDER BY e.fio;
    """).fetchall()
    conn.close()
    return render(request, 'employees/employee_list.html', {'employees_list': employees_list})

def employee_detail(request, emp_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    emp = conn.execute("""
        SELECT emp_id, fio, position, lab_id 
        FROM employees 
        WHERE emp_id = ?;
    """, (emp_id,)).fetchone()
    
    if emp is None:
        conn.close()
        return render(
            request, 
            'employees/employee_detail.html', 
            {'employee': None}, 
            status=404
        )
        
    conn.close()
    return render(request, 'employees/employee_detail.html', {'employee': emp})
