import json
from db.database import get_connection


def load_json(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ОШИБКА: Файл {filename} не найден в папке data/!")
        return None


def main():
    conn = get_connection()
    try:
        conn.executescript("""
            DELETE FROM issues;
            DELETE FROM equipment;
            DELETE FROM employees;
            DELETE FROM laboratories;
        """)

        labs = load_json("data/laboratories.json")
        if labs:
            conn.executemany(
                "INSERT INTO laboratories (lab_id, responsible, location) VALUES (?, ?, ?)",
                [(k, v['responsible'], v['location']) for k, v in labs.items()]
            )
            print(f"Импортировано лабораторий: {len(labs)}")

        emps = load_json("data/employees.json")
        if emps:
            conn.executemany(
                "INSERT INTO employees (emp_id, fio, position, lab_id) VALUES (?, ?, ?, ?)",
                [(k, v['fio'], v['position'], v['lab']) for k, v in emps.items()]
            )
            print(f"Импортировано сотрудников: {len(emps)}")

        eqs = load_json("data/equipment.json")
        if eqs:
            conn.executemany(
                "INSERT INTO equipment (inv_num, name, status) VALUES (?, ?, ?)",
                [(k, v['name'], v['status']) for k, v in eqs.items()]
            )
            print(f"Импортировано оборудования: {len(eqs)}")

        issues = load_json("data/issues.json")
        if issues and emps:
            fio_to_emp_id = {v['fio']: k for k, v in emps.items()}
            issues_data = []
            for item in issues:
                emp_id = fio_to_emp_id.get(item['employee'])
                if emp_id:
                    issues_data.append((
                        item['id'], item['inv_num'], emp_id,
                        item['return_date'], item.get('status', 'активна')
                    ))
            if issues_data:
                conn.executemany(
                    "INSERT INTO issues (id, inv_num, emp_id, return_date, status) VALUES (?, ?, ?, ?, ?)",
                    issues_data
                )
                print(f"Импортировано выдач: {len(issues_data)}")

        conn.commit()
        print("--- Импорт успешно завершен! ---")
    except Exception as e:
        conn.rollback()
        print(f"ОШИБКА ПРИ ИМПОРТЕ: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
