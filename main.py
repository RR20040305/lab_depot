import json
import os
from datetime import datetime, date

# ---------- Файл для хранения данных ----------
DATA_FILE = "data.json"

# ---------- Загрузка и сохранение ----------
def load_data():
    """Загружает данные из JSON-файла. Если файла нет — возвращает пустую структуру."""
    if not os.path.exists(DATA_FILE):
        return {"equipment": {}, "bookings": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """Сохраняет данные в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ---------- 1. Добавление оборудования ----------
def add_equipment(data):
    inv_num = input("Введите инвентарный номер: ").strip()

    if inv_num in data["equipment"]:
        print(f"Ошибка: оборудование с номером {inv_num} уже существует.")
        return

    name = input("Введите название оборудования: ").strip()
    status = input("Введите состояние (исправно/в ремонте): ").strip()

    if status not in ("исправно", "в ремонте"):
        print("Ошибка: допустимые состояния — 'исправно' или 'в ремонте'.")
        return

    data["equipment"][inv_num] = {"name": name, "status": status}
    save_data(data)
    print(f"Оборудование {inv_num} успешно добавлено.")


# ---------- 2. Редактирование ----------
def edit_equipment(data):
    inv_num = input("Введите инвентарный номер для редактирования: ").strip()

    if inv_num not in data["equipment"]:
        print(f"Ошибка: оборудование с номером {inv_num} не найдено.")
        return

    record = data["equipment"][inv_num]
    print(f"Текущие данные: {record}")

    name = input(f"Новое название (Enter — оставить '{record['name']}'): ").strip()
    status = input(f"Новое состояние (Enter — оставить '{record['status']}'): ").strip()

    if name:
        record["name"] = name
    if status:
        if status not in ("исправно", "в ремонте"):
            print("Ошибка: недопустимое состояние.")
            return
        record["status"] = status

    save_data(data)
    print(f"Запись {inv_num} обновлена: {record}")


# ---------- 3. Удаление ----------
def delete_equipment(data):
    inv_num = input("Введите инвентарный номер для удаления: ").strip()

    if inv_num not in data["equipment"]:
        print(f"Ошибка: оборудование с номером {inv_num} не найдено.")
        return

    # Проверим, нет ли активной брони на это оборудование
    active = [b for b in data["bookings"]
              if b["inv_num"] == inv_num and b["status"] == "активна"]
    if active:
        print("Ошибка: оборудование выдано, сначала отмените бронь.")
        return

    confirm = input(f"Удалить оборудование {inv_num}? (да/нет): ").strip().lower()
    if confirm == "да":
        del data["equipment"][inv_num]
        save_data(data)
        print(f"Оборудование {inv_num} удалено.")
    else:
        print("Удаление отменено.")


# ---------- 4. Проверка доступности ----------
def check_availability(data):
    inv_num = input("Введите инвентарный номер оборудования: ").strip()

    if inv_num not in data["equipment"]:
        print(f"Ошибка: оборудование с номером {inv_num} не найдено.")
        return

    status = data["equipment"][inv_num]["status"]

    if status == "в ремонте":
        print(f"Оборудование {inv_num} в ремонте – выдача невозможна.")
        return

    active = [b for b in data["bookings"]
              if b["inv_num"] == inv_num and b["status"] == "активна"]
    if active:
        print(f"Оборудование {inv_num} уже выдано. "
              f"Дата возврата: {active[0]['return_date']}")
    else:
        print(f"Оборудование {inv_num} доступно для выдачи.")


# ---------- 5. Добавление брони (выдача) ----------
def add_booking(data):
    inv_num = input("Введите инвентарный номер оборудования: ").strip()

    if inv_num not in data["equipment"]:
        print("Ошибка: оборудование не найдено.")
        return

    if data["equipment"][inv_num]["status"] == "в ремонте":
        print("Ошибка: оборудование в ремонте.")
        return

    active = [b for b in data["bookings"]
              if b["inv_num"] == inv_num and b["status"] == "активна"]
    if active:
        print("Ошибка: оборудование уже выдано.")
        return

    employee = input("Введите ФИО сотрудника: ").strip()
    date_str = input("Введите дату возврата (ГГГГ-ММ-ДД): ").strip()

    try:
        return_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Ошибка: неверный формат даты.")
        return

    if return_date < date.today():
        print("Ошибка: дата возврата не может быть в прошлом.")
        return

    booking = {
        "inv_num": inv_num,
        "employee": employee,
        "return_date": str(return_date),
        "status": "активна"
    }
    data["bookings"].append(booking)
    save_data(data)
    print(f"Оборудование {inv_num} выдано сотруднику {employee}.")


# ---------- 6. Отмена брони (возврат) ----------
def cancel_booking(data):
    inv_num = input("Введите инвентарный номер: ").strip()

    for booking in data["bookings"]:
        if booking["inv_num"] == inv_num and booking["status"] == "активна":
            booking["status"] = "завершена"
            save_data(data)
            print(f"Бронь на оборудование {inv_num} завершена.")
            return

    print("Активная бронь не найдена.")


# ---------- 7. Поиск ----------
def search_equipment(data):
    query = input("Введите часть названия для поиска: ").strip().lower()

    results = [(num, rec) for num, rec in data["equipment"].items()
               if query in rec["name"].lower()]

    if not results:
        print("Ничего не найдено.")
        return

    print(f"\nНайдено записей: {len(results)}")
    for num, rec in results:
        print(f"{num}: {rec['name']} — {rec['status']}")


# ---------- 8. Сортировка ----------
def sort_equipment(data):
    print("Сортировать по: 1 — номеру, 2 — названию")
    choice = input("Выбор: ").strip()

    if choice == "1":
        items = sorted(data["equipment"].items(), key=lambda x: x[0])
    elif choice == "2":
        items = sorted(data["equipment"].items(), key=lambda x: x[1]["name"])
    else:
        print("Неверный выбор.")
        return

    for num, rec in items:
        print(f"{num}: {rec['name']} — {rec['status']}")


# ---------- 9. Статистика ----------
def show_statistics(data):
    total = len(data["equipment"])
    in_repair = sum(1 for r in data["equipment"].values() if r["status"] == "в ремонте")
    active_bookings = sum(1 for b in data["bookings"] if b["status"] == "активна")

    print("\n--- Статистика ---")
    print(f"Всего оборудования: {total}")
    print(f"В ремонте: {in_repair}")
    print(f"Активных выдач: {active_bookings}")
    print(f"Завершённых выдач: {sum(1 for b in data['bookings'] if b['status'] == 'завершена')}")


# ---------- Главное меню ----------
def main():
    data = load_data()

    while True:
        print("\n--- Меню ---")
        print("1. Добавить оборудование")
        print("2. Редактировать оборудование")
        print("3. Удалить оборудование")
        print("4. Проверить доступность")
        print("5. Выдать оборудование")
        print("6. Вернуть оборудование")
        print("7. Поиск")
        print("8. Сортировка")
        print("9. Статистика")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_equipment(data)
        elif choice == "2":
            edit_equipment(data)
        elif choice == "3":
            delete_equipment(data)
        elif choice == "4":
            check_availability(data)
        elif choice == "5":
            add_booking(data)
        elif choice == "6":
            cancel_booking(data)
        elif choice == "7":
            search_equipment(data)
        elif choice == "8":
            sort_equipment(data)
        elif choice == "9":
            show_statistics(data)
        elif choice == "0":
            save_data(data)
            print("Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()