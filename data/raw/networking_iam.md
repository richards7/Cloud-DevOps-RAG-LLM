# Cloud Networking and IAM Basics

## Networking fundamentals
- **VPC (Virtual Private Cloud)**: an isolated virtual network within a
  cloud provider where your resources (VMs, containers, databases) live.
- **Subnets**: subdivisions of a VPC, often mapped to a region, used to
  organize and isolate resources.
- **Firewall rules**: control which traffic is allowed in/out of
  resources, based on IP ranges, ports, and protocols.
- **Load balancers**: distribute incoming traffic across multiple
  instances for reliability and scalability.
- **Public vs private IP**: a public IP is reachable from the internet;
  a private IP is only reachable within the VPC (or a connected
  network), which is preferred for internal-only services like
  databases.

## IAM (Identity and Access Management)
IAM controls *who* (identity) can do *what* (permissions) on *which*
resources.

- **Role**: a named collection of permissions (e.g. "Storage Object
  Viewer").
- **Permission**: a specific allowed action (e.g. `storage.objects.get`).
- **Policy**: a binding of roles to identities (users, groups, or
  service accounts) on a resource.
- **Service account**: a non-human identity used by an application or
  VM to authenticate and call other services — this is how a deployed
  API (e.g. on Cloud Run) securely calls other cloud services without
  embedding personal credentials.

## Principle of least privilege
Grant only the permissions an identity actually needs, nothing more.
This limits the damage if credentials are ever leaked or misused, and
is one of the most common security questions asked in cloud interviews.

## Secrets management
API keys and credentials should never be hardcoded or committed to
source control. Use environment variables for local development and a
managed secret store (Google Secret Manager, AWS Secrets Manager) in
production, injecting secrets into the container at deploy time.

## AWS IAM vs GCP IAM
Both follow the same core idea (identities, roles, policies), but GCP
additionally distinguishes **primitive roles** (Owner/Editor/Viewer,
broad), **predefined roles** (fine-grained, service-specific), and
**custom roles** (you define the exact permission set).
