# Docker Basics — Additional Common Errors & Fixes
(Supplements docker_basics.md already in the knowledge base.)

- **"Cannot connect to the Docker daemon"**: Docker Desktop/daemon isn't running —
  start it, or on Linux: `sudo systemctl start docker`.
- **"permission denied while trying to connect to the Docker daemon socket"**: your
  user isn't in the `docker` group — `sudo usermod -aG docker $USER`, then log out/in.
- **Build works but the container exits immediately**: check `docker logs <container>`
  — often the `CMD` process crashed or exited on its own (e.g. a script that finishes
  instead of running a long-lived server).
- **"no matching manifest for linux/arm64"**: pulling an image that doesn't support
  your CPU architecture (common on Apple Silicon) — look for a multi-arch image or add
  `--platform linux/amd64` (with an emulation performance cost).
- **Image builds are slow every time**: Docker's layer cache is being invalidated —
  reorder the Dockerfile so rarely-changing steps (installing dependencies) come
  before frequently-changing steps (copying source code).
