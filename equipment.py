import json
import os

DATA_FILE = "equipment.json"


def load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add(data):
    inv_num = input("Введите инвентарный номер: ").strip()
    if inv_num in data:
        print("Ошибка: номер уже существует.")
        return
    name = input("Введите название: ").strip()
    status = input("Состояние (исправно/в ремонте): ").strip()
    if status not in ("исправно", "в ремонте"):
        print("Ошибка: недопустимое состояние.")
        return
    data[inv_num] = {"name": name, "status": status}
    save(data)
    print(f"Оборудование {inv_num} добавлено.")


def edit(data):
    inv_num = input("Введите инвентарный номер: ").strip()
    if inv_num not in data:
        print("Ошибка: не найдено.")
        return
    rec = data[inv_num]
    name = input(f"Новое название ({rec['name']}): ").strip()
    status = input(f"Новое состояние ({rec['status']}): ").strip()
    if name:
        rec["name"] = name
    if status:
        if status not in ("исправно", "в ремонте"):
            print("Ошибка: недопустимое состояние.")
            return
        rec["status"] = status
    save(data)
    print("Запись обновлена.")


def delete(data):
    inv_num = input("Введите инвентарный номер: ").strip()
    if inv_num not in data:
        print("Ошибка: не найдено.")
        return
    confirm = input(f"Удалить {inv_num}? (да/нет): ").strip().lower()
    if confirm == "да":
        del data[inv_num]
        save(data)
        print("Удалено.")
    else:
        print("Отменено.")


def search(data):
    query = input("Часть названия: ").strip().lower()
    results = [(n, r) for n, r in data.items() if query in r["name"].lower()]
    if not results:
        print("Ничего не найдено.")
        return
    for n, r in results:
        print(f"{n}: {r['name']} — {r['status']}")


def sort(data):
    print("1 — по номеру, 2 — по названию")
    choice = input("Выбор: ").strip()
    if choice == "1":
        items = sorted(data.items(), key=lambda x: x[0])
    elif choice == "2":
        items = sorted(data.items(), key=lambda x: x[1]["name"])
    else:
        print("Неверный выбор.")
        return
    for n, r in items:
        print(f"{n}: {r['name']} — {r['status']}")