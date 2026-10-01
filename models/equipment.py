from typing import List, Optional
import storage
from utils import validate_status

DATA_FILE = 'data/equipment.json'


class Equipment:
    def __init__(self, inv_num: str, name: str, status: str) -> None:
        self.inv_num = inv_num
        self.name = name
        self.status = status

    def __str__(self) -> str:
        return f'{self.inv_num}: {self.name} — {self.status}'

    def matches(self, query: str) -> bool:
        return query.lower() in self.name.lower()

    def is_available(self) -> bool:
        return self.status == 'исправно'

    @classmethod
    def from_data(cls, inv_num: str, data: dict) -> 'Equipment':
        return cls(
            inv_num=inv_num,
            name=data['name'],
            status=data['status'],
        )

    def to_dict(self) -> dict:
        return {'name': self.name, 'status': self.status}


def load() -> List[Equipment]:
    raw = storage.load(DATA_FILE)
    return [Equipment.from_data(inv, data) for inv, data in raw.items()]


def save(data: List[Equipment]) -> None:
    raw = {eq.inv_num: eq.to_dict() for eq in data}
    storage.save(DATA_FILE, raw)


def find_by_id(data: List[Equipment], inv_num: str) -> Optional[Equipment]:
    for eq in data:
        if eq.inv_num == inv_num:
            return eq
    return None


def add(data: List[Equipment]) -> None:
    inv_num = input("Введите инвентарный номер: ").strip()
    if find_by_id(data, inv_num) is not None:
        print("Ошибка: номер уже существует.")
        return
    name = input("Введите название: ").strip()
    status = input("Состояние (исправно/в ремонте): ").strip()
    if not validate_status(status):
        print("Ошибка: недопустимое состояние.")
        return
    data.append(Equipment(inv_num, name, status))
    save(data)
    print(f"Оборудование {inv_num} добавлено.")


def edit(data: List[Equipment]) -> None:
    inv_num = input("Введите инвентарный номер: ").strip()
    eq = find_by_id(data, inv_num)
    if eq is None:
        print("Ошибка: не найдено.")
        return
    name = input(f"Новое название ({eq.name}): ").strip()
    status = input(f"Новое состояние ({eq.status}): ").strip()
    if name:
        eq.name = name
    if status:
        if not validate_status(status):
            print("Ошибка: недопустимое состояние.")
            return
        eq.status = status
    save(data)
    print("Запись обновлена.")


def delete(data: List[Equipment]) -> None:
    inv_num = input("Введите инвентарный номер: ").strip()
    eq = find_by_id(data, inv_num)
    if eq is None:
        print("Ошибка: не найдено.")
        return
    confirm = input(f"Удалить {inv_num}? (да/нет): ").strip().lower()
    if confirm == "да":
        data.remove(eq)
        save(data)
        print("Удалено.")
    else:
        print("Отменено.")


def search(data: List[Equipment]) -> None:
    query = input("Часть названия: ").strip()
    results = [eq for eq in data if eq.matches(query)]
    if not results:
        print("Ничего не найдено.")
        return
    for eq in results:
        print(eq)


def sort(data: List[Equipment]) -> None:
    print("1 — по номеру, 2 — по названию")
    choice = input("Выбор: ").strip()
    if choice == "1":
        items = sorted(data, key=lambda x: x.inv_num)
    elif choice == "2":
        items = sorted(data, key=lambda x: x.name)
    else:
        print("Неверный выбор.")
        return
    for eq in items:
        print(eq)
