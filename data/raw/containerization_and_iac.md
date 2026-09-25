# Containerization and Infrastructure as Code — Concepts

## Containerization (the "why", beyond Docker mechanics)
A container packages an application with its exact dependencies (libraries, runtime,
config) so it runs identically across environments — "works on my machine" becomes
"works everywhere," since the machine's differences no longer matter.

### Containers vs virtual machines
- **VM**: virtualizes hardware, runs a full guest OS — heavier (GBs), slower to start
  (minutes), but strong isolation.
- **Container**: virtualizes at the OS level, sharing the host kernel — lightweight
  (MBs), starts in seconds, slightly weaker isolation than a full VM.
This is one of the most common interview comparison questions in DevOps.

### Why containers pair naturally with microservices
Each service ships as its own container with only what it needs, deployed and scaled
independently — the isolation containers provide maps directly onto the independence
microservices need.

## Infrastructure as Code (IaC) — the underlying idea
Instead of manually clicking through a cloud console to create servers/networks
(error-prone, unrepeatable, undocumented), you describe the desired infrastructure in
version-controlled code and let a tool (Terraform, CloudFormation, ARM templates)
reconcile reality to match it.

### Declarative vs imperative IaC
- **Declarative** (Terraform, CloudFormation): you describe the end state you want;
  the tool figures out how to get there. Generally preferred for infrastructure.
- **Imperative** (a bash script calling `aws ec2 run-instances`): you specify the exact
  steps to take — more control, but you own tracking what already exists and handling
  partial failures yourself.

### Benefits (a frequent "why does this matter" interview answer)
- **Reproducibility**: identical environments for dev/staging/prod, reducing
  "it worked in staging" surprises.
- **Version control**: infrastructure changes are code-reviewed and tracked in Git,
  just like application code.
- **Disaster recovery**: if infrastructure is destroyed, it can be recreated from code
  rather than from memory/tribal knowledge.
- **Drift detection**: tools like `terraform plan` reveal when live infrastructure has
  diverged from the declared configuration.

## Common errors & fixes
- **"It works when I create it manually but not via IaC"**: often a missing default
  the console silently set for you — compare the console-created resource's full
  config against your IaC definition field by field.
- **Container works locally but fails when deployed**: check for environment
  differences the container didn't actually capture (e.g. relying on a host file/env
  var that wasn't baked into the image or passed at runtime).
- **IaC state doesn't match reality**: someone made a manual change outside the tool —
  reconcile via the tool's import/refresh capability rather than manually editing state.
