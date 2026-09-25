# Bash / Shell Scripting

## Script basics
```bash
#!/bin/bash
# The shebang line tells the OS which interpreter to use.

set -e            # exit immediately if any command fails
set -u            # treat unset variables as an error
set -o pipefail   # a pipeline fails if ANY command in it fails, not just the last

echo "Starting script..."
```
`set -euo pipefail` at the top of a script is a very common, strongly recommended
pattern — it prevents a script from silently continuing after a failure.

## Variables
```bash
NAME="Richard"
echo "Hello, $NAME"
echo "Hello, ${NAME}!"        # braces avoid ambiguity when concatenating

READONLY_VAR="fixed"           # (use `readonly READONLY_VAR="fixed"` to enforce)
```

## Conditionals
```bash
if [ "$ENV" == "production" ]; then
    echo "Running in prod"
elif [ "$ENV" == "staging" ]; then
    echo "Running in staging"
else
    echo "Unknown environment"
fi

# File/condition tests
if [ -f "config.yaml" ]; then echo "config exists"; fi
if [ -d "/var/log/myapp" ]; then echo "log dir exists"; fi
if [ -z "$VAR" ]; then echo "VAR is empty"; fi
```

## Loops
```bash
for file in *.log; do
    echo "Processing $file"
done

for i in {1..5}; do
    echo "Attempt $i"
done

while read -r line; do
    echo "Line: $line"
done < input.txt
```

## Functions
```bash
deploy() {
    local env=$1
    echo "Deploying to $env..."
    # deployment logic here
}

deploy "production"
```

## Command substitution and argument handling
```bash
CURRENT_DATE=$(date +%Y-%m-%d)
FILE_COUNT=$(ls | wc -l)

# Script arguments
echo "Script name: $0"
echo "First arg: $1"
echo "All args: $@"
echo "Arg count: $#"
```

## A real deployment script example
```bash
#!/bin/bash
set -euo pipefail

APP_DIR="/opt/myapp"
BRANCH="${1:-main}"

echo "Deploying branch: $BRANCH"

cd "$APP_DIR"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

docker build -t myapp:latest .
docker compose up -d

echo "Deployment complete."
```

## Common errors & fixes
- **"unbound variable" (with `set -u`)**: a variable was used before being set — check
  for typos in variable names, or provide a default: `${VAR:-default}`.
- **Script works when run with `bash script.sh` but not `./script.sh`**: check the
  shebang line exists and the file has execute permission (`chmod +x script.sh`).
- **"[: too many arguments" in an if statement**: usually an unquoted variable that
  expanded to multiple words or was empty — always quote variables: `[ "$VAR" == "x" ]`
  not `[ $VAR == x ]`.
- **A pipeline "succeeds" even though a command in the middle failed**: add
  `set -o pipefail`, since by default only the last command's exit code is checked.
- **Script has CRLF line endings and fails with cryptic syntax errors**: run
  `sed -i 's/\r$//' script.sh` (common when a script is edited on Windows then run on
  Linux).
