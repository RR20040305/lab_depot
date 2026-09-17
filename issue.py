import json
import os
from datetime import datetime, date

DATA_FILE = "issue.json"


def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add(data):
    inv_num = input("Инвентарный номер: ").strip()
    employee = input("ФИО сотрудника: ").strip()
    date_str = input("Дата возврата (ГГГГ-ММ-ДД): ").strip()
    try:
        return_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Ошибка: неверный формат даты.")
        return
    if return_date < date.today():
        print("Ошибка: дата в прошлом.")
        return
    record = {
        "inv_num": inv_num,
        "employee": employee,
        "return_date": str(return_date),
        "status": "активна"
    }
    data.append(record)
    save(data)
    print(f"Выдача оформлена: {inv_num} → {employee}")


def cancel(data):
    inv_num = input("Инвентарный номер: ").strip()
    for rec in data:
        if rec["inv_num"] == inv_num and rec["status"] == "активна":
            rec["status"] = "завершена"
            save(data)
            print(f"Бронь на {inv_num} завершена.")
            return
    print("Активная бронь не найдена.")


def check(data):
    inv_num = input("Инвентарный номер: ").strip()
    active = [r for r in data if r["inv_num"] == inv_num and r["status"] == "активна"]
    if active:
        print(f"Выдано. Дата возврата: {active[0]['return_date']}")
    else:
        print("Доступно для выдачи.")


def statistics(data):
    active = sum(1 for r in data if r["status"] == "активна")
    done = sum(1 for r in data if r["status"] == "завершена")
    print(f"Активных выдач: {active}")
    print(f"Завершённых выдач: {done}")