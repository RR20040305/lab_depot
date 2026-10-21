import sqlite3
from django.shortcuts import render

DB_PATH = "data/lab_depot.sqlite"


def issues(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    issues_list = conn.execute("""
        SELECT i.id, i.return_date, i.status, 
               e.name AS eq_name, e.inv_num,
               emp.fio AS emp_name
        FROM issues i
        LEFT JOIN equipment e ON i.inv_num = e.inv_num
        LEFT JOIN employees emp ON i.emp_id = emp.emp_id
        ORDER BY i.return_date DESC;
    """).fetchall()
    conn.close()
    return render(request, 'issues/issue_list.html', {'issues_list': issues_list})

def issue_detail(request, issue_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Запрос с JOIN, чтобы получить и данные выдачи, и ФИО сотрудника, и название оборудования
    issue = conn.execute("""
        SELECT i.id, i.return_date, i.status, 
               e.name AS eq_name, e.inv_num,
               emp.fio AS emp_name, emp.emp_id
        FROM issues i
        JOIN equipment e ON i.inv_num = e.inv_num
        JOIN employees emp ON i.emp_id = emp.emp_id
        WHERE i.id = ?;
    """, (issue_id,)).fetchone()
    
    if issue is None:
        conn.close()
        return render(
            request, 
            'issues/issue_detail.html', 
            {'issue': None}, 
            status=404
        )
        
    conn.close()
    return render(request, 'issues/issue_detail.html', {'issue': issue})
