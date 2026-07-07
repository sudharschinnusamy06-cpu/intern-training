# Day 23 - Capstone: Deploy to AWS

## What I learned
- SSH - connecting securely to a remote Linux server
- Installing Docker + Docker Compose on a fresh Ubuntu EC2 instance
- Cloning a GitHub repo directly onto a server
- Recreating .env manually on the server (secrets never travel through Git)
- Security groups - AWS firewall rules that block traffic by default
- Debugging a real port-mapping mismatch (container mapped 8080->8000, not 8000->8000)
- Verifying data persistence directly in PostgreSQL via psql inside the container

## Steps completed

### 1. Started EC2 instance
- Instance: task-api-server (t3.micro, Ubuntu, ap-southeast-2)
- Public IP (changes each start/stop): 3.26.92.36

### 2. Connected via SSH
ssh -i "task-api-key.pem" ubuntu@3.26.92.36

### 3. Installed Docker + Docker Compose on EC2
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose-v2
sudo docker --version
sudo docker compose version

### 4. Cloned GitHub repo onto EC2
git clone https://github.com/sudharschinnusamy06-cpu/intern-training.git
cd intern-training/Day21-dockerize-combined

### 5. Recreated .env on server (not in Git)
nano .env
Added: DATABASE_PASSWORD, API_KEY, DATABASE_HOST=db

### 6. Ran the full stack
sudo docker compose up --build
Result: db container healthy, api container started, Uvicorn running on port 8000 inside container

### 7. Fixed security group (networking issue)
- Problem: App unreachable from browser (ERR_CONNECTION_TIMED_OUT)
- Cause: Port 8080 (external mapped port, per docker-compose.yml: "8080:8000") was not open in the EC2 security group
- Fix: Added inbound rule - Custom TCP, port 8080, source 0.0.0.0/0
- Also added port 8000 initially (not strictly needed, since app is externally reachable via 8080, not 8000)

### 8. Verified live deployment
- URL: http://3.26.92.36:8080/docs
- Tested GET /tasks, POST /tasks (with API key), GET /tasks again
- Confirmed task persisted by querying PostgreSQL directly:
sudo docker exec -it day21-dockerize-combined-db-1 psql -U postgres -d interndb
SELECT * FROM task;

## Architecture
Browser → EC2 Public IP:8080 → Docker (api container, port 8000 internally) → PostgreSQL (db container, port 5432)
Both containers connected via Docker Compose's internal network, api reaches db using service name "db" (not localhost)

## Key concept
- EC2 = rented Linux server, reachable only through terminal (no GUI)
- Security groups = firewall rules; ports are blocked by default, must be explicitly opened
- .env must be recreated manually on any new server (never committed to Git)
- Same Docker Compose setup works identically on laptop and cloud server - this is the whole point of containerization

### Verified data persistence directly in database
SELECT * FROM task;
Result:
id |    title    |          description           | completed
----+-------------+--------------------------------+-----------
1 | Live on AWS | Testing deployment from Day 23 | f