-- Day 11: SQL Intermediate
-- Database: interndb, Table: employees

-- 1. DELETE
DELETE FROM employees WHERE id = 8;

-- 2. UPDATE
UPDATE employees SET salary = 60000 WHERE id = 4;

-- 3. COUNT + GROUP BY
SELECT department, COUNT(*)
FROM employees
GROUP BY department;

-- 4. AVG + GROUP BY
SELECT department, AVG(salary)
FROM employees
GROUP BY department;

-- 5. HAVING
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 30000;

-- 6. DISTINCT
SELECT DISTINCT department FROM employees;

-- 7. LIKE
SELECT * FROM employees WHERE name LIKE 'S%';

-- 8. BETWEEN
SELECT * FROM employees WHERE salary BETWEEN 30000 AND 50000;

-- 9. IN
SELECT * FROM employees
WHERE department IN ('HR', 'Engineering', 'Finance');