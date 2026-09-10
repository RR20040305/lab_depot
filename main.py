from datetime import datetime, date

# Хранилище записей: {инвентарный номер: {поля}}
equipment_db = {}


def add_equipment():
    """Добавление новой записи об оборудовании."""
    inv_num = input("Введите инвентарный номер: ").strip()

    if inv_num in equipment_db:
        print(f"Ошибка: оборудование с номером {inv_num} уже существует.")
        return

    name = input("Введите название оборудования: ").strip()
    status = input("Введите состояние (исправно/в ремонте/выдано): ").strip()

    equipment_db[inv_num] = {
        "name": name,
        "status": status
    }
    print(f"Оборудование {inv_num} успешно добавлено.")


def edit_equipment():
    """Редактирование существующей записи."""
    inv_num = input("Введите инвентарный номер для редактирования: ").strip()

    if inv_num not in equipment_db:
        print(f"Ошибка: оборудование с номером {inv_num} не найдено.")
        return

    record = equipment_db[inv_num]
    print(f"Текущие данные: {record}")

    name = input(f"Новое название (Enter — оставить '{record['name']}'): ").strip()
    status = input(f"Новое состояние (Enter — оставить '{record['status']}'): ").strip()

    if name:
        record["name"] = name
    if status:
        record["status"] = status

    print(f"Запись {inv_num} обновлена: {record}")


def delete_equipment():
    """Удаление записи об оборудовании."""
    inv_num = input("Введите инвентарный номер для удаления: ").strip()

    if inv_num not in equipment_db:
        print(f"Ошибка: оборудование с номером {inv_num} не найдено.")
        return

    confirm = input(f"Удалить оборудование {inv_num}? (да/нет): ").strip().lower()
    if confirm == "да":
        del equipment_db[inv_num]
        print(f"Оборудование {inv_num} удалено.")
    else:
        print("Удаление отменено.")


def check_availability():
    """Проверка возможности выдачи оборудования."""
    today = date.today()

    inv_num = input("Введите инвентарный номер оборудования: ").strip()

    if inv_num not in equipment_db:
        print(f"Ошибка: оборудование с номером {inv_num} не найдено в базе.")
        return

    status = equipment_db[inv_num]["status"]
    return_date_str = input("Введите планируемую дату возврата (ГГГГ-ММ-ДД): ")

    try:
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Ошибка: неверный формат даты. Используйте ГГГГ-ММ-ДД.")
        return

    if status == "в ремонте":
        print(f"Оборудование {inv_num} находится в ремонте – выдача невозможна.")
    elif status == "выдано":
        print(f"Оборудование {inv_num} уже выдано другому сотруднику.")
    elif status == "исправно":
        if return_date >= today:
            print(f"Оборудование {inv_num} доступно для выдачи до {return_date}.")
        else:
            print("Ошибка: дата возврата не может быть раньше сегодняшнего дня.")
    else:
        print("Неизвестное состояние оборудования. "
              "Допустимые значения: исправно, в ремонте, выдано.")


# Главное меню
if __name__ == "__main__":
    while True:
        print("\n--- Меню ---")
        print("1. Добавить оборудование")
        print("2. Редактировать оборудование")
        print("3. Удалить оборудование")
        print("4. Проверить возможность выдачи")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_equipment()
        elif choice == "2":
            edit_equipment()
        elif choice == "3":
            delete_equipment()
        elif choice == "4":
            check_availability()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")