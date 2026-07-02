-- Day 10: SQL Basics
-- Database: interndb

-- Create database
CREATE DATABASE interndb;

-- Connect to database
-- \c interndb

-- Create employees table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INT,
    joining_date DATE
);

-- Verify table structure
-- \d employees

-- Insert 12 employees
INSERT INTO employees (name, department, salary, joining_date) VALUES
('Sudhars', 'Engineering', 50000, '2024-01-15'),
('Siva', 'Software', 20000, '2024-02-13'),
('Priya', 'HR', 45000, '2024-02-20'),
('Raj', 'Finance', 55000, '2024-03-10'),
('Suresh', 'Marketing', 25000, '2024-04-13'),
('Harshu', 'HR', 30000, '2025-02-20'),
('Kavya', 'Developer', 35000, '2026-03-01'),
('Gokul', 'Professor', 40000, '2025-06-15'),
('Ram', 'Engineering', 30000, '2026-01-10'),
('Janu', 'HR', 25000, '2025-07-04'),
('Anbu', 'Engineering', 50000, '2024-02-15'),
('Meena', 'HR', 30000, '2024-05-15');

-- UPDATE: Fix duplicate names
UPDATE employees SET name = 'Anbu' WHERE id = 11;
UPDATE employees SET name = 'Meena' WHERE id = 12;

-- SELECT all rows
SELECT * FROM employees;

-- SELECT specific columns only
SELECT name, department, salary FROM employees;

-- SELECT with ORDER BY id
SELECT * FROM employees ORDER BY id;

-- SELECT with ORDER BY salary DESC
SELECT * FROM employees ORDER BY salary DESC;

-- SELECT with ORDER BY salary ASC
SELECT * FROM employees ORDER BY salary ASC;

-- WHERE filter: department
SELECT * FROM employees WHERE department = 'HR';

-- WHERE filter: salary
SELECT * FROM employees WHERE salary > 30000;

-- WHERE + ORDER BY combined
SELECT * FROM employees
WHERE department = 'Engineering'
ORDER BY salary DESC;