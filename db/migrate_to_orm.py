import os
import sys
import sqlite3
from datetime import date
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from laboratories.models import Laboratory
from employees.models import Employee
from equipment.models import Equipment
from issues.models import Issue

SOURCE_DB = BASE_DIR / "data" / "lab_depot.sqlite"


def main():
    if not SOURCE_DB.exists():
        print(f"Исходная база {SOURCE_DB} не найдена!")
        return

    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row
        
        # 1. Лаборатории
        labs = conn.execute("SELECT * FROM laboratories").fetchall()
        for row in labs:
            Laboratory.objects.update_or_create(
                lab_id=row["lab_id"],
                defaults={"responsible": row["responsible"], "location": row["location"]}
            )
        
        # 2. Сотрудники
        emps = conn.execute("SELECT * FROM employees").fetchall()
        for row in emps:
            Employee.objects.update_or_create(
                emp_id=row["emp_id"],
                defaults={"fio": row["fio"], "position": row["position"], "lab_id": row["lab_id"]}
            )

        # 3. Оборудование
        eqs = conn.execute("SELECT * FROM equipment").fetchall()
        for row in eqs:
            Equipment.objects.update_or_create(
                inv_num=row["inv_num"],
                defaults={"name": row["name"], "status": row["status"]}
            )

        # 4. Выдачи
        issues = conn.execute("SELECT * FROM issues").fetchall()
        for row in issues:
            Issue.objects.update_or_create(
                id=row["id"],
                defaults={
                    "equipment_id": row["inv_num"],
                    "employee_id": row["emp_id"],
                    "return_date": date.fromisoformat(row["return_date"]),
                    "status": row["status"]
                }
            )

    print("--- Данные успешно перенесены в ORM! ---")


if __name__ == "__main__":
    main()
