-- Day 12: SQL Advanced + Python Integration
-- Database: interndb

-- 1. Create departments table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    dept_name TEXT,
    location TEXT,
    budget INTEGER
);

-- 2. Insert departments
INSERT INTO departments (dept_name, location, budget) VALUES
('Engineering', 'Chennai', 500000),
('HR', 'Mumbai', 300000),
('Finance', 'Delhi', 400000),
('Software', 'Bangalore', 450000),
('Marketing', 'Hyderabad', 250000),
('Developer', 'Pune', 350000);

-- 3. Add department_id column to employees
ALTER TABLE employees ADD COLUMN department_id INTEGER;

-- 4. Update department_id values
UPDATE employees SET department_id = 1 WHERE department = 'Engineering';
UPDATE employees SET department_id = 2 WHERE department = 'HR';
UPDATE employees SET department_id = 3 WHERE department = 'Finance';
UPDATE employees SET department_id = 4 WHERE department = 'Software';
UPDATE employees SET department_id = 5 WHERE department = 'Marketing';
UPDATE employees SET department_id = 6 WHERE department = 'Developer';

-- 5. Add foreign key constraint
ALTER TABLE employees
ADD CONSTRAINT fk_department
FOREIGN KEY (department_id)
REFERENCES departments(id);

-- 6. INNER JOIN
SELECT employees.name, employees.salary,
       departments.dept_name, departments.location
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;

-- 7. LEFT JOIN
SELECT employees.name, employees.salary,
       departments.dept_name, departments.location
FROM employees
LEFT JOIN departments
ON employees.department_id = departments.id;

-- 8. Subquery
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);