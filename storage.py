import json
import os

ENCODINGS = ('utf-8-sig', 'utf-8', 'cp1251')


def _read_text(filename: str) -> str:
    last_error = None
    for encoding in ENCODINGS:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError as error:
            last_error = error
            continue
    raise last_error


def load(filename):
    if not os.path.exists(filename):
        return {}
    content = _read_text(filename).strip()
    if not content:
        return {}
    return json.loads(content)


def load_list(filename):
    if not os.path.exists(filename):
        return []
    content = _read_text(filename).strip()
    if not content:
        return []
    return json.loads(content)


def save(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)