import json
import os

DATA_FILE = "employee.json"


def load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add(data):
    emp_id = input("Введите табельный номер: ").strip()
    if emp_id in data:
        print("Ошибка: номер уже существует.")
        return
    fio = input("ФИО: ").strip()
    position = input("Должность: ").strip()
    lab = input("Номер лаборатории: ").strip()
    data[emp_id] = {"fio": fio, "position": position, "lab": lab}
    save(data)
    print(f"Сотрудник {emp_id} добавлен.")


def edit(data):
    emp_id = input("Введите табельный номер: ").strip()
    if emp_id not in data:
        print("Ошибка: не найдено.")
        return
    rec = data[emp_id]
    fio = input(f"ФИО ({rec['fio']}): ").strip()
    position = input(f"Должность ({rec['position']}): ").strip()
    lab = input(f"Лаборатория ({rec['lab']}): ").strip()
    if fio:
        rec["fio"] = fio
    if position:
        rec["position"] = position
    if lab:
        rec["lab"] = lab
    save(data)
    print("Запись обновлена.")


def delete(data):
    emp_id = input("Введите табельный номер: ").strip()
    if emp_id not in data:
        print("Ошибка: не найдено.")
        return
    confirm = input(f"Удалить {emp_id}? (да/нет): ").strip().lower()
    if confirm == "да":
        del data[emp_id]
        save(data)
        print("Удалено.")
    else:
        print("Отменено.")


def search(data):
    query = input("Часть ФИО: ").strip().lower()
    results = [(k, v) for k, v in data.items() if query in v["fio"].lower()]
    if not results:
        print("Ничего не найдено.")
        return
    for k, v in results:
        print(f"{k}: {v['fio']} — {v['position']} (лаб. {v['lab']})")