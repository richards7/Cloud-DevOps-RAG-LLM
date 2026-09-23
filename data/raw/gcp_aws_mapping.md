# GCP and AWS Service Mapping

Since many engineers learn AWS first, mapping services to Google Cloud
speeds up onboarding to GCP-based teams.

| Category            | AWS                  | Google Cloud                    |
|----------------------|-----------------------|----------------------------------|
| Virtual machines      | EC2                   | Compute Engine                  |
| Object storage        | S3                     | Cloud Storage                    |
| Relational database    | RDS                    | Cloud SQL                        |
| Serverless functions    | Lambda                | Cloud Functions                  |
| Serverless containers   | ECS / Fargate           | Cloud Run                        |
| Managed Kubernetes      | EKS                   | GKE (Google Kubernetes Engine)  |
| Identity & access       | IAM                    | IAM                               |
| ML model hosting/training | SageMaker           | Vertex AI                         |
| CDN                    | CloudFront             | Cloud CDN                         |
| Monitoring/logging       | CloudWatch             | Cloud Monitoring / Cloud Logging |
| Data warehouse           | Redshift               | BigQuery                          |
| Secrets management       | Secrets Manager         | Secret Manager                    |

## Cloud Run in depth
Cloud Run runs stateless containers and scales automatically — including
scaling to zero when there's no traffic, so you pay only for what you use.
It's a strong fit for a Dockerized FastAPI service: you build an image,
push it to Artifact Registry, and deploy it with a single command, without
managing servers or a Kubernetes cluster.

Because Cloud Run instances are stateless and can be stopped at any time,
anything that needs to persist (a database, a vector store, uploaded
files) should live outside the container — for example, in Cloud SQL,
Cloud Storage, or a managed vector database — rather than inside the
container's local filesystem, unless the data is a cache that can be
rebuilt.

## Vertex AI
Vertex AI is Google Cloud's unified ML platform: training custom models,
hosting pre-trained ones, running batch or online predictions, and
accessing Google's foundation models (like Gemini) through a managed API,
including a "Model Garden" of pre-built and third-party models.

## Core cloud concepts
- **IaaS vs PaaS vs SaaS**: IaaS gives you raw infrastructure (e.g.
  Compute Engine); PaaS manages the runtime for you (e.g. Cloud Run,
  App Engine); SaaS is a fully managed application (e.g. Gmail).
- **Regions vs zones**: a region is a geographic area (e.g.
  `asia-south1`); a zone is an isolated location within a region.
  Spreading resources across zones improves availability.
- **Horizontal vs vertical scaling**: horizontal scaling adds more
  instances; vertical scaling adds more resources (CPU/RAM) to an
  existing instance. Cloud-native services like Cloud Run scale
  horizontally by default.
