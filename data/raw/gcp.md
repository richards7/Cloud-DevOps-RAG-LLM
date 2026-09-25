# Google Cloud Platform (GCP)

(See gcp_aws_mapping.md for a side-by-side service comparison with AWS.)

## Core compute
- **Compute Engine**: virtual machines, customizable machine types.
- **Cloud Run**: serverless containers, scales to zero, ideal for stateless HTTP services.
- **GKE (Google Kubernetes Engine)**: managed Kubernetes — Google originated Kubernetes,
  so GKE tends to track upstream K8s features fastest among the big three clouds.
- **Cloud Functions**: event-driven serverless functions.

## Storage
- **Cloud Storage**: object storage, with storage classes Standard/Nearline/Coldline/Archive.
- **Persistent Disk**: block storage for Compute Engine VMs.

## Databases
- **Cloud SQL**: managed MySQL/PostgreSQL/SQL Server.
- **Firestore/Datastore**: NoSQL document databases.
- **BigQuery**: serverless data warehouse for large-scale analytics using SQL.

## Networking
- **VPC**: global by default (unlike AWS's regional VPCs) — subnets can span regions.
- **Firewall rules**: apply at the VPC level, target by network tags or service accounts.
- **Cloud Load Balancing**: global HTTP(S) load balancing built on Google's edge network.

## IAM
- **Service accounts**: an identity for workloads (like AWS IAM roles), can be attached
  to a VM/Cloud Run service so it can call other GCP APIs securely.
- **Roles**: primitive (Owner/Editor/Viewer — broad), predefined (fine-grained), custom.

## Project structure
- **Projects**: the basic organizing unit and billing boundary (roughly like an AWS
  account or Azure subscription). Projects belong to a Folder/Organization hierarchy.

## CLI basics (gcloud)
```bash
gcloud auth login
gcloud config set project my-project-id
gcloud compute instances list
gcloud run deploy my-service --image gcr.io/my-project/my-image --region asia-south1
gcloud logging read "resource.type=cloud_run_revision" --limit 20
```

## Common errors & fixes
- **"PERMISSION_DENIED"**: the service account/user lacks the IAM role for that API —
  check with `gcloud projects get-iam-policy <project-id>`.
- **Cloud Run deploy fails to start**: container must listen on the `$PORT` env var
  (default 8080) — a hardcoded port mismatch is the most common cause.
- **"API not enabled"**: run `gcloud services enable <api>.googleapis.com` — GCP APIs
  are off by default per project.
- **Billing account errors**: a project needs an active billing account linked before
  most services (Compute Engine, Cloud Run with custom domains, etc.) will work.
