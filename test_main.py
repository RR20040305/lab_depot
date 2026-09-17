import json
import os
import pytest
from datetime import date, timedelta
import main


@pytest.fixture
def sample_data():
    """Создаёт тестовые данные и временный файл."""
    data = {
        "equipment": {
            "001": {"name": "Микроскоп", "status": "исправно"},
            "002": {"name": "Центрифуга", "status": "в ремонте"},
            "003": {"name": "Спектрометр", "status": "исправно"}
        },
        "bookings": [
            {"inv_num": "003", "employee": "Иванов И.И.",
             "return_date": str(date.today() + timedelta(days=5)),
             "status": "активна"}
        ]
    }
    # Подменяем файл на временный
    main.DATA_FILE = "test_data.json"
    main.save_data(data)
    yield data
    # Удаляем временный файл
    if os.path.exists("test_data.json"):
        os.remove("test_data.json")


# ---------- Тесты ----------
def test_save_and_load(sample_data):
    loaded = main.load_data()
    assert loaded == sample_data


def test_add_equipment(sample_data, monkeypatch):
    inputs = iter(["004", "Осциллограф", "исправно"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main.add_equipment(sample_data)
    assert "004" in sample_data["equipment"]
    assert sample_data["equipment"]["004"]["name"] == "Осциллограф"


def test_add_duplicate(sample_data, monkeypatch, capsys):
    inputs = iter(["001", "Дубль", "исправно"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main.add_equipment(sample_data)
    captured = capsys.readouterr()
    assert "уже существует" in captured.out


def test_edit_equipment(sample_data, monkeypatch):
    inputs = iter(["001", "Микроскоп-2", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main.edit_equipment(sample_data)
    assert sample_data["equipment"]["001"]["name"] == "Микроскоп-2"
    assert sample_data["equipment"]["001"]["status"] == "исправно"


def test_delete_equipment(sample_data, monkeypatch):
    inputs = iter(["001", "да"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main.delete_equipment(sample_data)
    assert "001" not in sample_data["equipment"]


def test_check_availability_available(sample_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "001")
    main.check_availability(sample_data)
    captured = capsys.readouterr()
    assert "доступно для выдачи" in captured.out


def test_check_availability_busy(sample_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "003")
    main.check_availability(sample_data)
    captured = capsys.readouterr()
    assert "уже выдано" in captured.out


def test_check_availability_repair(sample_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "002")
    main.check_availability(sample_data)
    captured = capsys.readouterr()
    assert "в ремонте" in captured.out


def test_add_booking(sample_data, monkeypatch):
    future = str(date.today() + timedelta(days=3))
    inputs = iter(["001", "Петров П.П.", future])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main.add_booking(sample_data)
    assert any(b["inv_num"] == "001" and b["status"] == "активна"
               for b in sample_data["bookings"])


def test_cancel_booking(sample_data, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "003")
    main.cancel_booking(sample_data)
    assert any(b["inv_num"] == "003" and b["status"] == "завершена"
               for b in sample_data["bookings"])


def test_search_equipment(sample_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "микро")
    main.search_equipment(sample_data)
    captured = capsys.readouterr()
    assert "Микроскоп" in captured.out


def test_statistics(sample_data, capsys):
    main.show_statistics(sample_data)
    captured = capsys.readouterr()
    assert "Всего оборудования: 3" in captured.out
    assert "В ремонте: 1" in captured.out
    assert "Активных выдач: 1" in captured.out