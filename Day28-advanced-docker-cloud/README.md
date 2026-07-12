# Day 28 - Advanced Docker & Cloud

## 1. Multi-stage Docker Build
- Converted single-stage Dockerfile to multi-stage: Stage 1 (builder) installs
  packages; Stage 2 (final) copies only installed packages + app code, no build tools.
- Image size: 412MB -> 395MB (small drop since most packages use pre-built wheels;
  cryptography likely needed build tools that got discarded).

## 2. AWS RDS (Managed PostgreSQL) Setup
1. AWS Console -> RDS -> add AmazonRDSFullAccess to IAM user (one-time)
2. Create database -> Full configuration -> Engine: PostgreSQL
3. Template: Dev/Test | Availability: Single-AZ (1 instance) - avoids extra cost
4. Identifier: taskapi-db | Username: postgres | set a strong master password
5. Instance class: Burstable -> db.t3.micro (free tier eligible)
6. Storage: General Purpose SSD (gp3), 20 GiB (free tier limit)
7. Connectivity: Public access = Yes | New security group: taskapi-rds-sg
8. Turned OFF: Performance Insights, Enhanced Monitoring, DevOps Guru (avoid cost)
9. Initial database name: taskapi
10. Created, waited ~5-10 min for "Available" status

## 3. Debugging: Docker could not connect to RDS
Problem: App inside Docker got "Connection refused" on port 5432, even though
RDS was Available/Public and psql worked fine directly from Windows PowerShell.

Cause: Docker Desktop (WSL2) uses a different outbound IP than the Windows
host, so the security group's "My IP" rule didn't cover it.

Fix: Changed security group rule source to "Anywhere-IPv4 (0.0.0.0/0)" for
PostgreSQL/5432 on taskapi-rds-sg. (OK for learning, not for real production.)

Verified with: `docker run --rm -it postgres:17 psql -h <rds-endpoint> -p 5432 -U postgres -d taskapi`
(Note: use -it flag so the password prompt works interactively.)

## 4. RDS Connection - Verified
- App logs showed "Application startup complete" - SQLModel created tables
  on RDS via asyncpg.
- Confirmed via `psql \dt`: task and user tables exist in RDS database (taskapi).

## 5. S3 Upload - Complete
Added `POST /v1/tasks/{task_id}/upload` endpoint using boto3.

Issues fixed along the way:
1. Added `boto3` + `python-multipart` to requirements.txt
2. Added `BUCKET_NAME` to .env + docker-compose.yml (missing -> caused NoneType error)
3. Created AWS Access Key ID/Secret for sudhars-dev (needed IAMFullAccess first,
   granted via root login since sudhars-dev couldn't self-grant permissions)
4. Added `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` to
   .env + docker-compose.yml

Verified upload via curl.exe (Swagger UI's authorization header had a
browser-related rendering issue, so tested via curl instead - works reliably).

Result: successfully uploaded test.txt to
https://sudhars-intern-training-day22.s3.amazonaws.com/tasks/1/test.txt

## 6. CloudWatch & Kubernetes/ECS - Theory Only

CloudWatch: centralized logging/metrics/alarms for AWS resources - like CCTV +
alarm system. Similar purpose to Day24's BackgroundTasks logging, but survives
restarts/crashes since it's stored on AWS, not locally.

Kubernetes/ECS: container orchestration - manages multiple containers across
multiple servers (auto-restart, load balancing). Not needed yet for this
project's scale (single EC2 + Docker Compose is sufficient); relevant when
scaling to many users/containers.