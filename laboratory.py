import json
import os

DATA_FILE = "laboratory.json"


def load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add(data):
    lab_id = input("Введите номер лаборатории: ").strip()
    if lab_id in data:
        print("Ошибка: номер уже существует.")
        return
    responsible = input("Ответственное лицо: ").strip()
    location = input("Местоположение: ").strip()
    data[lab_id] = {"responsible": responsible, "location": location}
    save(data)
    print(f"Лаборатория {lab_id} добавлена.")


def edit(data):
    lab_id = input("Введите номер лаборатории: ").strip()
    if lab_id not in data:
        print("Ошибка: не найдено.")
        return
    rec = data[lab_id]
    responsible = input(f"Ответственное лицо ({rec['responsible']}): ").strip()
    location = input(f"Местоположение ({rec['location']}): ").strip()
    if responsible:
        rec["responsible"] = responsible
    if location:
        rec["location"] = location
    save(data)
    print("Запись обновлена.")


def delete(data):
    lab_id = input("Введите номер лаборатории: ").strip()
    if lab_id not in data:
        print("Ошибка: не найдено.")
        return
    confirm = input(f"Удалить {lab_id}? (да/нет): ").strip().lower()
    if confirm == "да":
        del data[lab_id]
        save(data)
        print("Удалено.")
    else:
        print("Отменено.")


def search(data):
    query = input("Часть названия/местоположения: ").strip().lower()
    results = [(k, v) for k, v in data.items()
               if query in k.lower() or query in v["location"].lower()]
    if not results:
        print("Ничего не найдено.")
        return
    for k, v in results:
        print(f"{k}: {v['responsible']} — {v['location']}")