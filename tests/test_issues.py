import os
import pytest
from datetime import date, timedelta
from models import Employee, Equipment, Issue
from models import issues


@pytest.fixture(autouse=True)
def clean_file():
    if os.path.exists(issues.DATA_FILE):
        os.remove(issues.DATA_FILE)
    yield
    if os.path.exists(issues.DATA_FILE):
        os.remove(issues.DATA_FILE)


def make_eq_emp():
    eq = Equipment("001", "Микроскоп", "исправно")
    emp = Employee("1001", "Иванов И.И.", "Инженер", "101")
    return eq, emp


def test_issue_creation():
    eq, emp = make_eq_emp()
    issue = Issue(eq, emp, "2026-12-12")
    assert issue.equipment is eq
    assert issue.employee is emp
    assert issue.is_active()


def test_issue_cancel():
    eq, emp = make_eq_emp()
    issue = Issue(eq, emp, "2026-12-12")
    issue.cancel()
    assert issue.status == "завершена"
    assert not issue.is_active()


def test_add(monkeypatch):
    eq, emp = make_eq_emp()
    future = str(date.today() + timedelta(days=5))
    inputs = iter(["001", "Иванов И.И.", future])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    data = []
    issues.add(data, [eq], [emp])
    assert len(data) == 1
    assert data[0].equipment is eq
    assert data[0].employee is emp
    assert data[0].is_active()


def test_add_past_date(monkeypatch, capsys):
    eq, emp = make_eq_emp()
    past = str(date.today() - timedelta(days=1))
    inputs = iter(["001", "Иванов И.И.", past])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    data = []
    issues.add(data, [eq], [emp])
    captured = capsys.readouterr()
    assert "в прошлом" in captured.out
    assert len(data) == 0


def test_cancel(monkeypatch):
    eq, emp = make_eq_emp()
    data = [Issue(eq, emp, str(date.today() + timedelta(days=5)))]
    monkeypatch.setattr("builtins.input", lambda _: "001")
    issues.cancel(data)
    assert data[0].status == "завершена"


def test_check(monkeypatch, capsys):
    eq, emp = make_eq_emp()
    data = [Issue(eq, emp, "2026-12-12")]
    monkeypatch.setattr("builtins.input", lambda _: "001")
    issues.check(data)
    captured = capsys.readouterr()
    assert "Выдано" in captured.out


def test_statistics(capsys):
    eq1, emp1 = Equipment("001", "A", "исправно"), Employee("1001", "A", "A", "101")
    eq2, emp2 = Equipment("002", "B", "исправно"), Employee("1002", "B", "B", "102")
    data = [
        Issue(eq1, emp1, "2026-12-12", status="активна"),
        Issue(eq2, emp2, "2026-01-01", status="завершена"),
    ]
    issues.statistics(data)
    captured = capsys.readouterr()
    assert "Активных выдач: 1" in captured.out
    assert "Завершённых выдач: 1" in captured.out
