# Nginx

Nginx is a high-performance web server, reverse proxy, and load balancer — commonly
sitting in front of application servers (like a FastAPI/Node app) to handle TLS
termination, static files, and routing.

## Reverse proxy basics
A reverse proxy sits between clients and backend servers, forwarding requests and
returning responses — clients only ever talk to Nginx, not the backend directly.

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Load balancing
```nginx
upstream backend {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    # least_conn;  # optional: route to the server with fewest active connections
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

## Serving static files + SPA routing
```nginx
server {
    listen 80;
    root /var/www/myapp;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;   # SPA fallback routing
    }
}
```

## Useful commands
```bash
sudo nginx -t                # test config syntax before reloading
sudo systemctl reload nginx  # apply config changes without dropping connections
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Common errors & fixes
- **502 Bad Gateway**: Nginx can't reach the backend — confirm the backend process is
  actually running and listening on the port in `proxy_pass`, and check firewall rules
  if the backend is on a different host.
- **504 Gateway Timeout**: backend took too long — increase
  `proxy_read_timeout`/`proxy_connect_timeout`, or investigate why the backend is slow.
- **413 Request Entity Too Large**: increase `client_max_body_size` in the server block.
- **"nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)"**:
  another process is already using port 80 — `sudo lsof -i :80` to find it.
- **Config changes not taking effect**: always run `nginx -t` then `systemctl reload
  nginx` (not `restart`, which drops active connections unnecessarily).
