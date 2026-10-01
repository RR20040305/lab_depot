import os
import pytest
from models import Laboratory
from models import laboratories


@pytest.fixture(autouse=True)
def clean_file():
    if os.path.exists(laboratories.DATA_FILE):
        os.remove(laboratories.DATA_FILE)
    yield
    if os.path.exists(laboratories.DATA_FILE):
        os.remove(laboratories.DATA_FILE)


def test_lab_creation():
    lab = Laboratory("101", "Иванов И.И.", "Корпус А")
    assert lab.lab_id == "101"
    assert lab.responsible == "Иванов И.И."
    assert lab.location == "Корпус А"


def test_lab_str():
    lab = Laboratory("101", "Иванов И.И.", "Корпус А")
    assert "Иванов И.И." in str(lab)


def test_add(monkeypatch):
    inputs = iter(["101", "Иванов И.И.", "Корпус А"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    data = []
    laboratories.add(data)
    assert len(data) == 1
    assert data[0].lab_id == "101"


def test_edit(monkeypatch):
    data = [Laboratory("101", "Иванов И.И.", "Корпус А")]
    inputs = iter(["101", "Петров П.П.", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    laboratories.edit(data)
    assert data[0].responsible == "Петров П.П."
    assert data[0].location == "Корпус А"


def test_delete(monkeypatch):
    data = [Laboratory("101", "Иванов И.И.", "Корпус А")]
    inputs = iter(["101", "да"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    laboratories.delete(data)
    assert len(data) == 0


def test_search(monkeypatch, capsys):
    data = [
        Laboratory("101", "Иванов И.И.", "Корпус А"),
        Laboratory("102", "Петрова А.С.", "Корпус Б"),
    ]
    monkeypatch.setattr("builtins.input", lambda _: "корпус а")
    laboratories.search(data)
    captured = capsys.readouterr()
    assert "Корпус А" in captured.out
