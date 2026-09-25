# Docker Compose

Docker Compose defines and runs multi-container applications using a single YAML file,
instead of chaining many `docker run` commands manually.

## Basic structure
```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db
    volumes:
      - ./app:/app

  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

## Key concepts
- **Services** become containers; Compose creates a default network so services reach
  each other by service name (e.g. `web` connects to `db:5432`, not `localhost:5432`).
- **depends_on** controls start order, but does NOT wait for the app inside to be
  "ready" — only that the container has started. Use a healthcheck or a retry loop in
  the app for true readiness.
- **Volumes**: named volumes (managed by Docker, e.g. `db_data`) persist data
  independent of container lifecycle; bind mounts (`./app:/app`) map a host folder
  directly, useful for live-reloading code during development.

## Common commands
```bash
docker compose up -d          # start all services in the background
docker compose down           # stop and remove containers (add -v to also remove volumes)
docker compose logs -f web    # follow logs for one service
docker compose exec web bash  # shell into a running service
docker compose ps             # list running services
docker compose build          # rebuild images
```

## Common errors & fixes
- **"port is already allocated"**: another process (or a previous compose run) is
  using that host port — `docker ps` to find it, or change the host-side port mapping.
- **Service can't connect to db ("connection refused")**: the db container may not be
  ready yet despite `depends_on` — add a healthcheck:
  ```yaml
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
  ```
  and `depends_on: db: condition: service_healthy` on the dependent service.
- **Changes to code not reflected**: if using bind mounts, confirm the path is correct;
  if not using bind mounts, you must rebuild (`docker compose up --build`).
- **"no space left on device"**: prune unused images/volumes:
  `docker system prune -a --volumes` (careful — this removes anything not in use).
