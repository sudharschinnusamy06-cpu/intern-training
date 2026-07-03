import psycopg2

# Step 1: Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",        # local machine
    database="interndb",    # our database
    user="postgres",        # postgres user
    password="postgres123"     # your postgres password
)

# Step 2: Create cursor
cursor = conn.cursor()

# Step 3: Run a query
cursor.execute("SELECT * FROM employees")

# Step 4: Fetch results
rows = cursor.fetchall()

# Step 5: Print results
for row in rows:
    print(row)

# Step 6: Close connection
cursor.close()
conn.close()