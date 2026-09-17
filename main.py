import equipment
import laboratory
import employee
import issue


def main():
    eq = equipment.load()
    lab = laboratory.load()
    emp = employee.load()
    iss = issue.load()

    while True:
        print("\n--- Меню ---")
        print("1. Оборудование")
        print("2. Лаборатории")
        print("3. Сотрудники")
        print("4. Выдачи")
        print("0. Выход")

        choice = input("Выбор: ").strip()

        if choice == "1":
            print("1.Добавить 2.Изменить 3.Удалить 4.Поиск 5.Сортировка")
            c = input("Действие: ").strip()
            if c == "1":
                equipment.add(eq)
            elif c == "2":
                equipment.edit(eq)
            elif c == "3":
                equipment.delete(eq)
            elif c == "4":
                equipment.search(eq)
            elif c == "5":
                equipment.sort(eq)
        elif choice == "2":
            print("1.Добавить 2.Изменить 3.Удалить 4.Поиск")
            c = input("Действие: ").strip()
            if c == "1":
                laboratory.add(lab)
            elif c == "2":
                laboratory.edit(lab)
            elif c == "3":
                laboratory.delete(lab)
            elif c == "4":
                laboratory.search(lab)
        elif choice == "3":
            print("1.Добавить 2.Изменить 3.Удалить 4.Поиск")
            c = input("Действие: ").strip()
            if c == "1":
                employee.add(emp)
            elif c == "2":
                employee.edit(emp)
            elif c == "3":
                employee.delete(emp)
            elif c == "4":
                employee.search(emp)
        elif choice == "4":
            print("1.Выдать 2.Вернуть 3.Проверить 4.Статистика")
            c = input("Действие: ").strip()
            if c == "1":
                issue.add(iss)
            elif c == "2":
                issue.cancel(iss)
            elif c == "3":
                issue.check(iss)
            elif c == "4":
                issue.statistics(iss)
        elif choice == "0":
            equipment.save(eq)
            laboratory.save(lab)
            employee.save(emp)
            issue.save(iss)
            print("Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()