-- 1. Список всего оборудования (SELECT)
SELECT inv_num, name, status FROM equipment ORDER BY name;

-- 2. Список всех лабораторий (SELECT)
SELECT lab_id, responsible, location FROM laboratories ORDER BY lab_id;

-- 3. Поиск оборудования в ремонте (WHERE)
SELECT inv_num, name FROM equipment WHERE status = 'в ремонте';

-- 4. Список сотрудников конкретной лаборатории (WHERE)
SELECT emp_id, fio, position FROM employees WHERE lab_id = ?;

-- 5. Выдачи с названиями оборудования и ФИО сотрудников (JOIN)
SELECT i.id, i.return_date, i.status, e.name AS eq_name, emp.fio AS emp_name
FROM issues i
JOIN equipment e ON i.inv_num = e.inv_num
JOIN employees emp ON i.emp_id = emp.emp_id
ORDER BY i.return_date DESC;

-- 6. Оборудование, которое сейчас выдано (JOIN + WHERE)
SELECT e.inv_num, e.name, emp.fio AS emp_name
FROM equipment e
JOIN issues i ON e.inv_num = i.inv_num
JOIN employees emp ON i.emp_id = emp.emp_id
WHERE i.status = 'активна';

-- 7. Общее количество оборудования (COUNT)
SELECT COUNT(*) AS total_equipment FROM equipment;

-- 8. Количество активных выдач (COUNT + WHERE)
SELECT COUNT(*) AS active_issues FROM issues WHERE status = 'активна';

-- 9. Количество сотрудников в каждой лаборатории (GROUP BY)
SELECT lab_id, COUNT(emp_id) AS emp_count
FROM employees
GROUP BY lab_id
ORDER BY emp_count DESC;

-- 10. Статистика по статусам оборудования (GROUP BY)
SELECT status, COUNT(*) AS count
FROM equipment
GROUP BY status;