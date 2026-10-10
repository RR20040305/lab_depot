from models import equipment, employees, laboratories, issues

eq = equipment.load()
emp = employees.load()
lab = laboratories.load()
iss = issues.load(eq, emp)

print('Оборудование:', len(eq))
print('Сотрудники:', len(emp))
print('Лаборатории:', len(lab))
print('Выдачи:', len(iss))

if eq:
    print('Пример:', eq[0])
