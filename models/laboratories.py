from typing import List, Optional
import storage

DATA_FILE = 'data/laboratories.json'


class Laboratory:
    def __init__(self, lab_id: str, responsible: str, location: str) -> None:
        self.lab_id = lab_id
        self.responsible = responsible
        self.location = location

    def __str__(self) -> str:
        return f'{self.lab_id}: {self.responsible} — {self.location}'

    def matches(self, query: str) -> bool:
        q = query.lower()
        return q in self.lab_id.lower() or q in self.location.lower()

    @classmethod
    def from_data(cls, lab_id: str, data: dict) -> 'Laboratory':
        return cls(
            lab_id=lab_id,
            responsible=data['responsible'],
            location=data['location'],
        )

    def to_dict(self) -> dict:
        return {'responsible': self.responsible, 'location': self.location}


def load() -> List[Laboratory]:
    raw = storage.load(DATA_FILE)
    return [Laboratory.from_data(lab_id, data) for lab_id, data in raw.items()]


def save(data: List[Laboratory]) -> None:
    raw = {lab.lab_id: lab.to_dict() for lab in data}
    storage.save(DATA_FILE, raw)


def find_by_id(data: List[Laboratory], lab_id: str) -> Optional[Laboratory]:
    for lab in data:
        if lab.lab_id == lab_id:
            return lab
    return None


def add(data: List[Laboratory]) -> None:
    lab_id = input("Введите номер лаборатории: ").strip()
    if find_by_id(data, lab_id) is not None:
        print("Ошибка: номер уже существует.")
        return
    responsible = input("Ответственное лицо: ").strip()
    location = input("Местоположение: ").strip()
    data.append(Laboratory(lab_id, responsible, location))
    save(data)
    print(f"Лаборатория {lab_id} добавлена.")


def edit(data: List[Laboratory]) -> None:
    lab_id = input("Введите номер лаборатории: ").strip()
    lab = find_by_id(data, lab_id)
    if lab is None:
        print("Ошибка: не найдено.")
        return
    responsible = input(f"Ответственное лицо ({lab.responsible}): ").strip()
    location = input(f"Местоположение ({lab.location}): ").strip()
    if responsible:
        lab.responsible = responsible
    if location:
        lab.location = location
    save(data)
    print("Запись обновлена.")


def delete(data: List[Laboratory]) -> None:
    lab_id = input("Введите номер лаборатории: ").strip()
    lab = find_by_id(data, lab_id)
    if lab is None:
        print("Ошибка: не найдено.")
        return
    confirm = input(f"Удалить {lab_id}? (да/нет): ").strip().lower()
    if confirm == "да":
        data.remove(lab)
        save(data)
        print("Удалено.")
    else:
        print("Отменено.")


def search(data: List[Laboratory]) -> None:
    query = input("Часть названия/местоположения: ").strip()
    results = [lab for lab in data if lab.matches(query)]
    if not results:
        print("Ничего не найдено.")
        return
    for lab in results:
        print(lab)
