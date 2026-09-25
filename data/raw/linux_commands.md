# Linux Commands — Basic to Advanced (with use cases)

## Navigation and file basics
```bash
pwd                        # print working directory
ls -la                     # list all files, long format (permissions, size, owner)
cd /var/log                # change directory
mkdir -p a/b/c              # create nested directories in one go
touch file.txt               # create an empty file / update timestamp
cp file.txt backup.txt       # copy a file
cp -r dir1/ dir2/             # copy a directory recursively
mv old.txt new.txt            # rename/move
rm file.txt                    # delete a file
rm -rf dir/                     # delete a directory recursively, forcefully (use with care)
find . -name "*.log"             # search for files by name, from current dir down
find . -mtime -1                  # files modified in the last 1 day — use case: recent changes
```

## Viewing and editing file content
```bash
cat file.txt                # print whole file
less file.txt                # scrollable view of a large file (q to quit)
head -n 20 file.txt            # first 20 lines — use case: check a log's start
tail -n 20 file.txt              # last 20 lines
tail -f app.log                    # follow a log file live — use case: watch a server start up
nano file.txt                        # simple terminal editor
vim file.txt                          # powerful modal editor (i to insert, Esc then :wq to save+quit)
grep "ERROR" app.log                    # search for a pattern in a file
grep -r "TODO" ./src                      # search recursively across a directory
grep -i "error" app.log                    # case-insensitive search
grep -v "DEBUG" app.log                      # invert match — show lines NOT matching
```

## Permissions and ownership
```bash
chmod 755 script.sh          # rwxr-xr-x — owner can read/write/execute, others read/execute
chmod +x script.sh             # add execute permission
chown user:group file.txt        # change owner and group
ls -l file.txt                     # see current permissions: -rwxr-xr-x
```
**Use case**: a script fails with "Permission denied" — `chmod +x script.sh` is
almost always the fix if the script itself is fine.

## Process management
```bash
ps aux                     # list all running processes
ps aux | grep python         # find a specific process
top                            # live view of processes/resource usage
htop                             # nicer interactive version of top (may need install)
kill <pid>                         # gracefully terminate a process
kill -9 <pid>                        # force kill (SIGKILL) — use when kill alone doesn't work
pkill -f "uvicorn"                     # kill by matching process name/command
nohup python app.py &                    # run a process immune to hangup, in the background
jobs                                       # list background jobs in current shell
fg %1                                        # bring job 1 to the foreground
```
**Use case**: a port is stuck occupied — `lsof -i :8080` to find the PID,
`kill -9 <pid>` to free it.

## Disk and system info
```bash
df -h                       # disk space usage, human-readable
du -sh /var/log                # size of a specific directory
free -h                          # memory usage
uname -a                           # kernel/system info
uptime                               # how long the system's been running + load average
lsblk                                  # list block devices/partitions
```

## Networking
```bash
ping google.com                 # test connectivity
curl -I https://example.com        # fetch just the HTTP headers
curl -X POST url -d '{"a":1}' -H "Content-Type: application/json"   # make a POST request
wget https://example.com/file.zip    # download a file
netstat -tulnp                         # list listening ports and owning processes (older systems)
ss -tulnp                                # modern replacement for netstat
lsof -i :8080                              # find what's using port 8080
dig example.com                              # DNS lookup
nslookup example.com                           # simpler DNS lookup
traceroute example.com                           # trace the network path to a host
```

## Package management
```bash
sudo apt update && sudo apt upgrade -y     # Debian/Ubuntu: refresh and upgrade packages
sudo apt install nginx                        # install a package
sudo yum install nginx                          # RHEL/CentOS equivalent
sudo systemctl status nginx                       # check a service's status
sudo systemctl start|stop|restart|reload nginx      # control a service
sudo systemctl enable nginx                           # start automatically on boot
journalctl -u nginx -f                                  # follow a service's logs (systemd)
```

## Archiving and compression
```bash
tar -czvf archive.tar.gz mydir/     # create a gzip-compressed archive
tar -xzvf archive.tar.gz              # extract it
zip -r archive.zip mydir/               # zip a directory
unzip archive.zip                         # unzip
```

## Text processing (advanced)
```bash
awk '{print $1}' file.txt                # print the first column
awk -F',' '{print $2}' data.csv            # use comma as field separator
sed 's/foo/bar/g' file.txt                   # replace all "foo" with "bar"
sed -i 's/foo/bar/g' file.txt                  # same, but edit the file in place
sort file.txt | uniq -c | sort -nr               # count unique lines, sorted by frequency
                                                   # use case: find the most common IP in a log
cut -d':' -f1 /etc/passwd                           # extract the 1st field of each line
wc -l file.txt                                        # count lines
```
**Use case (log analysis)**: find the top 5 IPs hitting a server:
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -5
```

## Piping and redirection
```bash
command1 | command2          # pipe: feed command1's output into command2
command > out.txt               # redirect stdout to a file (overwrite)
command >> out.txt                # redirect stdout, append
command 2> err.txt                  # redirect stderr only
command > out.txt 2>&1                # redirect both stdout and stderr to the same file
command &> out.txt                      # shorthand for the same
```

## SSH and remote access
```bash
ssh user@host                    # connect to a remote machine
ssh -i mykey.pem user@host         # connect using a specific private key
scp file.txt user@host:/path/        # copy a file to a remote host
scp -r dir/ user@host:/path/           # copy a directory recursively
ssh-keygen -t ed25519                    # generate a new SSH key pair
```

## Environment and shell
```bash
echo $PATH                    # print an environment variable
export MY_VAR=value             # set an environment variable for this session
env                                # list all environment variables
which python                         # show the path to an executable
alias ll='ls -la'                      # create a shortcut command
history | grep docker                    # search command history
```

## User and cron management
```bash
whoami                       # current user
sudo adduser newuser            # add a user
sudo usermod -aG docker myuser    # add a user to a group (e.g. to use docker without sudo)
crontab -e                          # edit the current user's scheduled jobs
crontab -l                            # list scheduled jobs
```
**Cron syntax**: `minute hour day month weekday command`
```
0 2 * * *  /path/to/backup.sh    # run daily at 2:00 AM
*/15 * * * * /path/to/check.sh    # run every 15 minutes
```

## Common errors & fixes
- **"Permission denied"**: check file permissions (`ls -l`) and ownership
  (`chown`), or whether the command needs `sudo`.
- **"command not found"**: the tool isn't installed, or isn't on `$PATH` — check with
  `which <command>` and install via the package manager if missing.
- **"No space left on device"**: `df -h` to find the full partition, `du -sh
  /* 2>/dev/null | sort -rh | head` to find what's taking space.
- **"Address already in use"**: another process holds the port — `lsof -i :<port>`
  then `kill -9 <pid>`, or run on a different port.
- **Script has Windows line endings and fails oddly on Linux**: `dos2unix script.sh`,
  or `sed -i 's/\r$//' script.sh`, converts CRLF to LF.
- **"bash: ./script.sh: Permission denied"**: `chmod +x script.sh`.
- **Zombie/defunct processes piling up**: usually a parent process not reaping
  children properly — identify the parent PID with `ps -ef | grep defunct` and
  investigate/restart it.
