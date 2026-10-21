CREATE TABLE IF NOT EXISTS laboratories (
    lab_id TEXT PRIMARY KEY,
    responsible TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT PRIMARY KEY,
    fio TEXT NOT NULL,
    position TEXT NOT NULL,
    lab_id TEXT NOT NULL,
    FOREIGN KEY (lab_id) REFERENCES laboratories(lab_id)
);

CREATE TABLE IF NOT EXISTS equipment (
    inv_num TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY,
    inv_num TEXT NOT NULL,
    emp_id TEXT NOT NULL,
    return_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'активна',
    FOREIGN KEY (inv_num) REFERENCES equipment(inv_num),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);