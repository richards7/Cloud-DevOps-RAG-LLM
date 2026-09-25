# GCP/AWS Mapping — Additional Common Errors & Fixes
(Supplements gcp_aws_mapping.md already in the knowledge base.)

- **Confusing GCP's global VPC with AWS's regional VPC model**: in GCP, a single VPC
  can span all regions with subnets per region; in AWS, a VPC is created within one
  region — this trips up engineers moving between the two.
- **Cloud Run container fails to deploy from a working local Docker image**: almost
  always a port mismatch — Cloud Run requires the container to listen on the `$PORT`
  environment variable (defaults to 8080), not a hardcoded port.
- **"quota exceeded" errors on either platform**: both AWS and GCP have per-region,
  per-service default quotas for new/free-tier accounts — request a quota increase via
  the respective console before assuming something is broken.
