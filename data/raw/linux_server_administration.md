# Linux Server Administration

## Boot process and services (systemd)
Modern Linux distros use **systemd** to manage services (the successor to older
init/upstart systems).

```bash
systemctl status nginx           # check if a service is running
systemctl start|stop|restart nginx
systemctl enable nginx             # start automatically on boot
systemctl disable nginx
systemctl daemon-reload              # reload systemd after editing a unit file
journalctl -u nginx --since "1 hour ago"   # view recent logs for a service
journalctl -xe                               # recent system logs with extra context
```

## Writing a custom systemd service
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My FastAPI App
After=network.target

[Service]
User=myuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp
```
**Use case**: this is how you keep a Python/FastAPI app running persistently on a VM,
restarting automatically if it crashes, without needing a terminal session open.

## User and permission management
```bash
sudo adduser deploy                # create a user
sudo usermod -aG sudo deploy         # give sudo privileges
sudo passwd deploy                     # set/change password
sudo deluser deploy                      # remove a user
groups deploy                              # check a user's group memberships
```

## Firewall management (ufw — common on Ubuntu)
```bash
sudo ufw status
sudo ufw allow 22/tcp        # SSH
sudo ufw allow 80,443/tcp      # HTTP/HTTPS
sudo ufw enable
sudo ufw deny 8080/tcp            # explicitly block a port
```

## Disk and filesystem management
```bash
lsblk                        # list disks/partitions
df -h                          # disk usage per mounted filesystem
mount /dev/sdb1 /mnt/data        # mount a partition
umount /mnt/data                   # unmount
fdisk -l                             # detailed partition info (requires sudo)
```

## Log management
Most system/application logs live under `/var/log/`. Key ones:
- `/var/log/syslog` (or `/var/log/messages` on RHEL) — general system log
- `/var/log/auth.log` — authentication attempts, SSH logins
- `/var/log/nginx/access.log` and `error.log`
- Application-specific logs, often under `/var/log/<app-name>/`

**Log rotation** (via `logrotate`) prevents logs from growing indefinitely:
```
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
}
```

## Monitoring resource usage
```bash
top / htop                  # live CPU/memory/process view
vmstat 1                      # virtual memory stats, updated every 1s
iostat 1                        # disk I/O stats
free -h                            # memory usage summary
```

## Common errors & fixes
- **Service fails to start**: check `journalctl -u <service> -n 50` for the actual
  error — common causes: wrong `WorkingDirectory`, missing environment variables, or
  the `ExecStart` binary path being wrong.
- **"Too many open files"**: hit the OS file descriptor limit — check with `ulimit -n`
  and raise it in `/etc/security/limits.conf` for the affected user.
- **High load average but low CPU usage**: often means processes are stuck waiting on
  I/O (disk/network) — check `iostat` and `vmstat` for I/O wait percentage.
- **Server unreachable after a reboot**: check the service is `enable`d (not just
  `start`ed), and that firewall rules persist across reboot.
- **Disk full crashes the app but `df -h` shows space**: check inode usage too —
  `df -i` — you can run out of inodes (too many small files) even with disk space free.
