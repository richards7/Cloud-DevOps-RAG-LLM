# Oracle Cloud Infrastructure (OCI)

## Core compute
- **Compute Instances**: VMs, with "Always Free" eligible shapes (e.g. VM.Standard.E2.1.Micro)
  — useful for personal projects/demos at zero cost.
- **OKE (Oracle Kubernetes Engine)**: managed Kubernetes on OCI.
- **Functions**: serverless, based on the open-source Fn Project.

## Storage
- **Object Storage**: OCI's S3-equivalent.
- **Block Volume**: attachable block storage for compute instances.

## Databases (Oracle's core strength)
- **Autonomous Database**: self-patching, self-tuning managed Oracle DB (OLTP or
  analytics-optimized variants).
- **Oracle Database Cloud Service**: traditional managed Oracle DB.

## Networking
- **VCN (Virtual Cloud Network)**: OCI's equivalent of a VPC.
- **Security Lists / Network Security Groups**: firewall rules at subnet or resource level.

## IAM
- **Compartments**: logical grouping for resources and access control — OCI's version of
  resource groups/projects, and central to how OCI IAM policies are scoped.
- **Policies**: written in a near-English syntax, e.g.
  `Allow group Developers to manage instances in compartment MyCompartment`.

## Oracle APEX (relevant for full-stack/low-code work)
A low-code platform for building data-driven web apps directly on Oracle Database —
interactive reports, forms, and dashboards built with SQL/PL/SQL backing them.

## CLI basics
```bash
oci setup config                       # first-time CLI configuration
oci compute instance list --compartment-id <ocid>
oci os bucket list --compartment-id <ocid>
```

## Common errors & fixes
- **"NotAuthorizedOrNotFound"**: OCI IAM policies are compartment-scoped — check the
  compartment ID matches where the resource actually lives.
- **Instance has no internet access**: confirm the VCN has an Internet Gateway and the
  subnet's route table points to it, plus a public IP assigned.
- **Autonomous DB connection failures**: usually a missing/incorrect wallet file (OCI
  requires downloading a connection wallet for secure TLS connections) or an ACL rule
  blocking the client IP.
