from typing import List, Optional
import storage
from utils import parse_date, is_future_or_today
from .equipment import Equipment
from .employees import Employee

DATA_FILE = 'data/issues.json'


class Issue:
    """Выдача оборудования сотруднику."""

    def __init__(
        self,
        equipment: Equipment,
        employee: Employee,
        return_date: str,
        status: str = 'активна',
        issue_id: int = 0,
    ) -> None:
        self.id = issue_id
        self.equipment = equipment
        self.employee = employee
        self.return_date = return_date
        self.status = status

    def __str__(self) -> str:
        return (
            f'№{self.id}: {self.equipment.inv_num} ({self.equipment.name}) → '
            f'{self.employee.fio} (до {self.return_date}, {self.status})'
        )

    def cancel(self) -> None:
        self.status = 'завершена'

    def is_active(self) -> bool:
        return self.status == 'активна'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'inv_num': self.equipment.inv_num,
            'employee': self.employee.fio,
            'return_date': self.return_date,
            'status': self.status,
        }


def load(
    equipment_list: List[Equipment],
    employees_list: List[Employee],
) -> List[Issue]:
    raw = storage.load_list(DATA_FILE)
    result: List[Issue] = []
    for item in raw:
        eq = next(
            (e for e in equipment_list if e.inv_num == item['inv_num']),
            None,
        )
        emp = next(
            (e for e in employees_list if e.fio == item['employee']),
            None,
        )
        if eq is not None and emp is not None:
            result.append(Issue(
                equipment=eq,
                employee=emp,
                return_date=item['return_date'],
                status=item.get('status', 'активна'),
                issue_id=item.get('id', 0),
            ))
    return result


def save(data: List[Issue]) -> None:
    raw = [issue.to_dict() for issue in data]
    storage.save(DATA_FILE, raw)


def find_by_id(data: List[Issue], issue_id: int) -> Optional[Issue]:
    for issue in data:
        if issue.id == issue_id:
            return issue
    return None


def is_equipment_busy(
    issues_list: List[Issue],
    equipment: Equipment,
) -> bool:
    """Есть ли активная выдача на эту единицу оборудования."""
    return any(
        issue.equipment.inv_num == equipment.inv_num and issue.is_active()
        for issue in issues_list
    )


def _next_id(data: List[Issue]) -> int:
    return max((issue.id for issue in data), default=0) + 1


def add(
    data: List[Issue],
    equipment_list: List[Equipment],
    employees_list: List[Employee],
) -> None:
    inv_num = input("Инвентарный номер: ").strip()
    eq = next((e for e in equipment_list if e.inv_num == inv_num), None)
    if eq is None:
        print("Ошибка: оборудование не найдено.")
        return

    fio = input("ФИО сотрудника: ").strip()
    emp = next((e for e in employees_list if e.fio == fio), None)
    if emp is None:
        print("Ошибка: сотрудник не найден.")
        return

    date_str = input("Дата возврата (ГГГГ-ММ-ДД): ").strip()
    return_date = parse_date(date_str)
    if return_date is None:
        print("Ошибка: неверный формат даты.")
        return
    if not is_future_or_today(return_date):
        print("Ошибка: дата в прошлом.")
        return

    data.append(Issue(
        equipment=eq,
        employee=emp,
        return_date=str(return_date),
        issue_id=_next_id(data),
    ))
    save(data)
    print(f"Выдача оформлена: {eq.inv_num} → {emp.fio}")


def cancel(data: List[Issue]) -> None:
    inv_num = input("Инвентарный номер: ").strip()
    for issue in data:
        if issue.equipment.inv_num == inv_num and issue.is_active():
            issue.cancel()
            save(data)
            print(f"Бронь на {inv_num} завершена.")
            return
    print("Активная бронь не найдена.")


def check(data: List[Issue]) -> None:
    inv_num = input("Инвентарный номер: ").strip()
    active = [
        i for i in data
        if i.equipment.inv_num == inv_num and i.is_active()
    ]
    if active:
        print(f"Выдано. Дата возврата: {active[0].return_date}")
    else:
        print("Доступно для выдачи.")


def statistics(data: List[Issue]) -> None:
    active = sum(1 for issue in data if issue.is_active())
    done = sum(1 for issue in data if issue.status == 'завершена')
    print(f"Активных выдач: {active}")
    print(f"Завершённых выдач: {done}")