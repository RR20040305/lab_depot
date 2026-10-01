from typing import List, Optional
import storage

DATA_FILE = 'data/employees.json'


class Employee:
    def __init__(self, emp_id: str, fio: str, position: str, lab: str) -> None:
        self.emp_id = emp_id
        self.fio = fio
        self.position = position
        self.lab = lab

    def __str__(self) -> str:
        return f'{self.emp_id}: {self.fio} — {self.position} (лаб. {self.lab})'

    def matches(self, query: str) -> bool:
        return query.lower() in self.fio.lower()

    @classmethod
    def from_data(cls, emp_id: str, data: dict) -> 'Employee':
        return cls(
            emp_id=emp_id,
            fio=data['fio'],
            position=data['position'],
            lab=data['lab'],
        )

    def to_dict(self) -> dict:
        return {
            'fio': self.fio,
            'position': self.position,
            'lab': self.lab,
        }


def load() -> List[Employee]:
    raw = storage.load(DATA_FILE)
    return [Employee.from_data(emp_id, data) for emp_id, data in raw.items()]


def save(data: List[Employee]) -> None:
    raw = {emp.emp_id: emp.to_dict() for emp in data}
    storage.save(DATA_FILE, raw)


def find_by_id(data: List[Employee], emp_id: str) -> Optional[Employee]:
    for emp in data:
        if emp.emp_id == emp_id:
            return emp
    return None


def add(data: List[Employee]) -> None:
    emp_id = input("Введите табельный номер: ").strip()
    if find_by_id(data, emp_id) is not None:
        print("Ошибка: номер уже существует.")
        return
    fio = input("ФИО: ").strip()
    position = input("Должность: ").strip()
    lab = input("Номер лаборатории: ").strip()
    data.append(Employee(emp_id, fio, position, lab))
    save(data)
    print(f"Сотрудник {emp_id} добавлен.")


def edit(data: List[Employee]) -> None:
    emp_id = input("Введите табельный номер: ").strip()
    emp = find_by_id(data, emp_id)
    if emp is None:
        print("Ошибка: не найдено.")
        return
    fio = input(f"ФИО ({emp.fio}): ").strip()
    position = input(f"Должность ({emp.position}): ").strip()
    lab = input(f"Лаборатория ({emp.lab}): ").strip()
    if fio:
        emp.fio = fio
    if position:
        emp.position = position
    if lab:
        emp.lab = lab
    save(data)
    print("Запись обновлена.")


def delete(data: List[Employee]) -> None:
    emp_id = input("Введите табельный номер: ").strip()
    emp = find_by_id(data, emp_id)
    if emp is None:
        print("Ошибка: не найдено.")
        return
    confirm = input(f"Удалить {emp_id}? (да/нет): ").strip().lower()
    if confirm == "да":
        data.remove(emp)
        save(data)
        print("Удалено.")
    else:
        print("Отменено.")


def search(data: List[Employee]) -> None:
    query = input("Часть ФИО: ").strip()
    results = [emp for emp in data if emp.matches(query)]
    if not results:
        print("Ничего не найдено.")
        return
    for emp in results:
        print(emp)
