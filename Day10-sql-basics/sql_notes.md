# Day 10 — SQL Basics

## Setup
- Database: PostgreSQL 17 (port 5432)
- Database name: interndb
- Table: employees

---

## Key Concepts

### Relational Database
Data is stored in tables (like spreadsheets) with rows and columns.
Multiple tables can relate to each other via foreign keys (Day 12).

### SQL Data Types Used
| Type | Description | Example |
|------|-------------|---------|
| SERIAL | Auto-increment integer | id (1,2,3...) |
| INTEGER | Whole number | salary |
| TEXT | Any length string | name, department |
| DATE | Date value (YYYY-MM-DD) | joining_date |

### PRIMARY KEY
- Unique identifier for each row
- Cannot be NULL, cannot repeat
- id SERIAL PRIMARY KEY = auto-generated unique number

---

## Commands Used

### CREATE TABLE
Defines table structure with column names and data types.
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INT,
    joining_date DATE
);
```

### INSERT
Adds new rows to the table.
```sql
INSERT INTO employees (name, department, salary, joining_date)
VALUES ('Sudhars', 'Engineering', 50000, '2024-01-15');
```

### SELECT
Fetches data from the table.
```sql
SELECT * FROM employees;              -- all columns
SELECT name, salary FROM employees;   -- specific columns only
```

### WHERE
Filters rows based on condition.
```sql
SELECT * FROM employees WHERE department = 'HR';
SELECT * FROM employees WHERE salary > 30000;
```

### ORDER BY
Sorts results.
```sql
SELECT * FROM employees ORDER BY salary DESC;  -- highest first
SELECT * FROM employees ORDER BY salary ASC;   -- lowest first
```

### UPDATE
Modifies existing row data.
```sql
UPDATE employees SET name = 'Anbu' WHERE id = 11;
```

### WHERE + ORDER BY combined
```sql
SELECT * FROM employees
WHERE department = 'Engineering'
ORDER BY salary DESC;
```

---

## Observations
- SERIAL id auto-increments — deleted id (7) never reused
- id=7 was accidentally deleted, gap is normal PostgreSQL behavior
- ORDER BY default is ASC (ascending)
- SELECT specific columns reduces unnecessary data — useful for APIs
- PostgreSQL already running on port 5432 (confirmed in Day 9!)

---

## Connection to future days
- Day 11: UPDATE, DELETE, aggregates (COUNT, AVG, SUM), GROUP BY
- Day 12: JOINs + Python psycopg2 integration
- Day 17: FastAPI + PostgreSQL = Task Management API with real database!