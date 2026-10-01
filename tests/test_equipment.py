import os
import pytest
from models import Equipment
from models import equipment


@pytest.fixture(autouse=True)
def clean_file():
    if os.path.exists(equipment.DATA_FILE):
        os.remove(equipment.DATA_FILE)
    yield
    if os.path.exists(equipment.DATA_FILE):
        os.remove(equipment.DATA_FILE)


def test_equipment_creation():
    eq = Equipment("001", "Микроскоп", "исправно")
    assert eq.inv_num == "001"
    assert eq.name == "Микроскоп"
    assert eq.status == "исправно"
    assert eq.is_available()


def test_equipment_str():
    eq = Equipment("001", "Микроскоп", "исправно")
    assert "Микроскоп" in str(eq)


def test_add(monkeypatch):
    inputs = iter(["001", "Микроскоп", "исправно"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    data = []
    equipment.add(data)
    assert len(data) == 1
    assert data[0].inv_num == "001"
    assert data[0].name == "Микроскоп"


def test_add_duplicate(monkeypatch, capsys):
    inputs = iter(["001", "Микроскоп", "исправно"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    data = []
    equipment.add(data)
    inputs2 = iter(["001", "Дубль", "исправно"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs2))
    equipment.add(data)
    captured = capsys.readouterr()
    assert "уже существует" in captured.out


def test_edit(monkeypatch):
    data = [Equipment("001", "Микроскоп", "исправно")]
    inputs = iter(["001", "Микроскоп-2", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    equipment.edit(data)
    assert data[0].name == "Микроскоп-2"
    assert data[0].status == "исправно"


def test_delete(monkeypatch):
    data = [Equipment("001", "Микроскоп", "исправно")]
    inputs = iter(["001", "да"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    equipment.delete(data)
    assert len(data) == 0


def test_search(monkeypatch, capsys):
    data = [
        Equipment("001", "Микроскоп", "исправно"),
        Equipment("002", "Центрифуга", "в ремонте"),
    ]
    monkeypatch.setattr("builtins.input", lambda _: "микро")
    equipment.search(data)
    captured = capsys.readouterr()
    assert "Микроскоп" in captured.out
