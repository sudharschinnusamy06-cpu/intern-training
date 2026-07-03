# Day 12 — SQL Advanced + Python Integration

## Database: interndb | Tables: employees, departments

---

## What we did today — Step by Step

1. `psycopg2-binary` install panninom — Python PostgreSQL driver
2. `departments` table create panninom (id, dept_name, location, budget)
3. 6 departments insert panninom
4. `employees` table la `department_id` column add panninom (ALTER TABLE)
5. Each employee ku correct `department_id` UPDATE panninom
6. Foreign key constraint add panninom (employees.department_id → departments.id)
7. INNER JOIN query run panninom — employee + department data combined
8. LEFT JOIN query run panninom — all employees, NULL if no department
9. Subquery run panninom — above average salary employees filter panninom
10. Python script (`db_connect.py`) write panninom — psycopg2 use pannி PostgreSQL connect panninom, data Python tuples la fetch panninom

---

## New Concepts

### Foreign Key
Links two tables together.
employees.department_id → departments.id
Ensures data integrity — can't assign invalid department_id.

### ALTER TABLE
Adds new column to existing table.
```sql
ALTER TABLE employees ADD COLUMN department_id INTEGER;
```

### INNER JOIN
Returns only matching rows from both tables.
```sql
SELECT employees.name, departments.location
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;
```

### LEFT JOIN
Returns all rows from left table.
Non-matching rows show NULL for right table columns.
```sql
SELECT employees.name, departments.location
FROM employees
LEFT JOIN departments
ON employees.department_id = departments.id;
```

### Subquery
Query inside another query.
```sql
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
Result: Sudhars, Anbu, Priya, Raj (above average salary)

---

## Python + psycopg2

### Connection
```python
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="interndb",
    user="postgres",
    password="yourpassword"
)
```

### Flow
Python script
↓ psycopg2
PostgreSQL server (port 5432)
↓ SQL query
Data returned as Python tuples

### Key objects
| Object | Purpose |
|---|---|
| `conn` | Database connection |
| `cursor` | Execute queries |
| `fetchall()` | Get all rows |
| `fetchone()` | Get one row |

---

## INNER vs LEFT JOIN

| | INNER JOIN | LEFT JOIN |
|---|---|---|
| Returns | Only matching rows | All left table rows |
| No match | Row excluded | NULL shown |
| Use case | Related data only | All records + optional relation |

---

## Connection to future days
- Day 13: Git branches, PR, merge conflict
- Day 17: FastAPI + SQLAlchemy (same psycopg2 concept, ORM layer added!)
- Capstone: Full production app with PostgreSQL
