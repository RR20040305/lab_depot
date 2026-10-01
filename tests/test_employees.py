import os
import pytest
from models import Employee
from models import employees


@pytest.fixture(autouse=True)
def clean_file():
    if os.path.exists(employees.DATA_FILE):
        os.remove(employees.DATA_FILE)
    yield
    if os.path.exists(employees.DATA_FILE):
        os.remove(employees.DATA_FILE)


def test_employee_creation():
    emp = Employee("1001", "Иванов И.И.", "Инженер", "101")
    assert emp.emp_id == "1001"
    assert emp.fio == "Иванов И.И."
    assert emp.position == "Инженер"
    assert emp.lab == "101"


def test_employee_str():
    emp = Employee("1001", "Иванов И.И.", "Инженер", "101")
    assert "Иванов И.И." in str(emp)


def test_employee_matches():
    emp = Employee("1001", "Иванов И.И.", "Инженер", "101")
    assert emp.matches("иванов")
    assert not emp.matches("петров")


def test_add(monkeypatch):
    inputs = iter(["1001", "Иванов И.И.", "Инженер", "101"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    data = []
    employees.add(data)
    assert len(data) == 1
    assert data[0].emp_id == "1001"
    assert data[0].fio == "Иванов И.И."


def test_edit(monkeypatch):
    data = [Employee("1001", "Иванов И.И.", "Инженер", "101")]
    inputs = iter(["1001", "Иванов И.И.", "Ст. инженер", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    employees.edit(data)
    assert data[0].position == "Ст. инженер"
    assert data[0].lab == "101"


def test_delete(monkeypatch):
    data = [Employee("1001", "Иванов И.И.", "Инженер", "101")]
    inputs = iter(["1001", "да"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    employees.delete(data)
    assert len(data) == 0


def test_search(monkeypatch, capsys):
    data = [
        Employee("1001", "Иванов И.И.", "Инженер", "101"),
        Employee("1002", "Петрова А.С.", "Научный сотрудник", "102"),
    ]
    monkeypatch.setattr("builtins.input", lambda _: "иванов")
    employees.search(data)
    captured = capsys.readouterr()
    assert "Иванов И.И." in captured.out
