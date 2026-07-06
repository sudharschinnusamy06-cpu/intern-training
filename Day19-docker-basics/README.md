# Day 19 - Docker Basics

## What I learned
- Docker images vs containers (image = blueprint, container = running instance)
- Docker Hub - pulling and running public images
- Port mapping (-p) to access containers from browser
- Writing a Dockerfile (FROM, WORKDIR, COPY, CMD)
- Building custom image and running it

## Commands used

| Command | Used for |
|---|---|
| `docker --version` | Verify Docker installation |
| `docker run hello-world` | Test Docker engine is working |
| `docker pull nginx` | Download nginx image from Docker Hub |
| `docker images` | List all local images |
| `docker run -d -p 8080:80 --name my-nginx nginx` | Run nginx in background, map container port 80 to laptop port 8080 |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (running + stopped) |
| `docker stop my-nginx` | Stop a running container |
| `docker rm my-nginx` | Delete a stopped container |
| `docker build -t my-python-app .` | Build image from Dockerfile in current folder |
| `docker run my-python-app` | Run container from custom-built image |
| `docker rm <container-id>` | Remove exited/stopped containers |

## Files
- `app.py` - simple Python script
- `Dockerfile` - instructions to containerize app.py

## Key concept
Image = recipe (blueprint, read-only)
Container = actual dish made from recipe (running instance, can create many from one image)