from models import employees, equipment, issues, laboratories


def menu_equipment(data):
    print("1.Добавить 2.Изменить 3.Удалить 4.Поиск 5.Сортировка")
    c = input("Действие: ").strip()
    if c == "1":
        equipment.add(data)
    elif c == "2":
        equipment.edit(data)
    elif c == "3":
        equipment.delete(data)
    elif c == "4":
        equipment.search(data)
    elif c == "5":
        equipment.sort(data)


def menu_laboratories(data):
    print("1.Добавить 2.Изменить 3.Удалить 4.Поиск")
    c = input("Действие: ").strip()
    if c == "1":
        laboratories.add(data)
    elif c == "2":
        laboratories.edit(data)
    elif c == "3":
        laboratories.delete(data)
    elif c == "4":
        laboratories.search(data)


def menu_employees(data):
    print("1.Добавить 2.Изменить 3.Удалить 4.Поиск")
    c = input("Действие: ").strip()
    if c == "1":
        employees.add(data)
    elif c == "2":
        employees.edit(data)
    elif c == "3":
        employees.delete(data)
    elif c == "4":
        employees.search(data)


def menu_issues(data, equipment_list, employees_list):
    print("1.Выдать 2.Вернуть 3.Проверить 4.Статистика")
    c = input("Действие: ").strip()
    if c == "1":
        issues.add(data, equipment_list, employees_list)
    elif c == "2":
        issues.cancel(data)
    elif c == "3":
        issues.check(data)
    elif c == "4":
        issues.statistics(data)


def main() -> None:
    eq = equipment.load()
    lab = laboratories.load()
    emp = employees.load()
    iss = issues.load(eq, emp)

    while True:
        print("\n--- Меню ---")
        print("1. Оборудование")
        print("2. Лаборатории")
        print("3. Сотрудники")
        print("4. Выдачи")
        print("0. Выход")

        choice = input("Выбор: ").strip()

        if choice == "1":
            menu_equipment(eq)
        elif choice == "2":
            menu_laboratories(lab)
        elif choice == "3":
            menu_employees(emp)
        elif choice == "4":
            menu_issues(iss, eq, emp)
        elif choice == "0":
            equipment.save(eq)
            laboratories.save(lab)
            employees.save(emp)
            issues.save(iss)
            print("Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()