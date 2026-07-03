# Day 11 — SQL Intermediate

## Database: interndb | Table: employees

---

## Commands Used

### DELETE
Removes a specific row permanently.
```sql
DELETE FROM employees WHERE id = 8;
```
Result: Gokul (Professor) row deleted.

### UPDATE
Modifies existing row data.
```sql
UPDATE employees SET salary = 60000 WHERE id = 4;
```
Result: Raj's salary updated from 55000 → 60000.

### COUNT + GROUP BY
Counts rows grouped by a column.
```sql
SELECT department, COUNT(*) FROM employees GROUP BY department;
```
Result: HR=4, Engineering=3, others=1 each.

### AVG + GROUP BY
Average salary per department.
```sql
SELECT department, AVG(salary) FROM employees GROUP BY department;
```
Result: Finance highest (60000), Software lowest (20000).

### HAVING
Filters GROUP BY results — like WHERE but for groups.
```sql
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 30000;
```
Result: 4 departments (avg > 30000), Marketing + Software filtered out.

### DISTINCT
Returns unique values only, removes duplicates.
```sql
SELECT DISTINCT department FROM employees;
```
Result: 6 unique departments listed.

### LIKE
Pattern matching on text columns.
```sql
SELECT * FROM employees WHERE name LIKE 'S%';
```
Result: Sudhars, Siva, Suresh (names starting with S).

### BETWEEN
Filters rows within a range (inclusive).
```sql
SELECT * FROM employees WHERE salary BETWEEN 30000 AND 50000;
```
Result: 7 employees in that salary range.

### IN
Filters rows matching any value in a list.
```sql
SELECT * FROM employees
WHERE department IN ('HR', 'Engineering', 'Finance');
```
Result: 8 employees from those 3 departments.

---

## Key Differences

| Command | vs | Difference |
|---|---|---|
| WHERE | HAVING | WHERE filters rows, HAVING filters groups |
| DELETE | UPDATE | DELETE removes row, UPDATE modifies row |
| LIKE | IN | LIKE = pattern match, IN = exact list match |
| BETWEEN | WHERE > AND < | BETWEEN is cleaner, inclusive of both ends |

---

## Connection to future days
- Day 12: JOINs + Python psycopg2 integration
- Day 17: FastAPI + PostgreSQL — these queries inside Python functions!