# Docker Basics

Docker is a containerization platform that packages an application together
with everything it needs to run — code, runtime, libraries, and system
tools — into a single, portable unit called a container.

## Image vs Container
A Docker **image** is a read-only template (built from a Dockerfile) that
defines what goes into a container. A **container** is a running instance
of an image. You can run many containers from the same image.

## Dockerfile
A Dockerfile is a text file with instructions to build an image:
- `FROM` — the base image (e.g. `python:3.11-slim`)
- `WORKDIR` — sets the working directory inside the image
- `COPY` — copies files from the host into the image
- `RUN` — executes a command at build time (e.g. installing dependencies)
- `EXPOSE` — documents which port the container listens on
- `CMD` / `ENTRYPOINT` — the command that runs when the container starts

Example:
```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Layers and caching
Each instruction in a Dockerfile creates a new layer. Docker caches layers,
so ordering matters: put instructions that change rarely (like installing
dependencies) before instructions that change often (like copying source
code), so rebuilds are faster.

## Volumes and networking
Volumes persist data outside a container's lifecycle (e.g. a database
file or a vector store). Docker's default bridge network lets containers
talk to each other by name when using `docker-compose`.

## Multi-stage builds
Multi-stage builds use multiple `FROM` statements to keep the final image
small — for example, compiling in one stage and copying only the compiled
output into a slim final stage. This reduces image size and attack surface.

## Best practices
- Use `.dockerignore` to exclude files like `.env`, `__pycache__`, and `.git`.
- Run containers as a non-root user where possible.
- Pin base image versions instead of using `latest`.
- Keep images small — smaller images start faster and deploy faster,
  which matters directly for services like Cloud Run.
