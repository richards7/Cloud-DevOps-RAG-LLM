# Network Security and Cloud Security

## Core networking security concepts
- **Firewall**: filters traffic by IP, port, protocol. Cloud firewalls (Security
  Groups, NSGs) operate at the instance/subnet level rather than physical hardware.
- **Defense in depth**: layer multiple controls (firewall + IAM + encryption +
  monitoring) so no single failure exposes the whole system.
- **Principle of least privilege**: grant only the access needed, nothing more — the
  single most commonly asked cloud security interview question.
- **Zero Trust**: never automatically trust traffic based on network location alone
  (e.g. "it's inside the VPC so it's safe") — verify identity and authorization on
  every request, internal or external.

## Common attack surfaces and mitigations
- **Open ports/services**: only expose what's needed (e.g. don't expose a database
  port to the public internet — keep it in a private subnet).
- **Weak/leaked credentials**: use short-lived credentials (IAM roles/service accounts)
  instead of long-lived access keys where possible; rotate keys regularly.
- **Unencrypted data**: encrypt data at rest (e.g. S3 server-side encryption, EBS
  encryption) and in transit (TLS everywhere, including internal service-to-service
  calls where feasible).
- **Overly permissive security groups**: avoid `0.0.0.0/0` (open to the entire
  internet) except where truly necessary (e.g. a public web server's port 443).

## Cloud-specific security services
- **AWS**: Security Groups, NACLs, IAM, KMS (key management), GuardDuty (threat
  detection), WAF (web application firewall).
- **Azure**: NSGs, Azure AD, Key Vault, Microsoft Defender for Cloud.
- **GCP**: VPC Firewall Rules, IAM, Cloud KMS, Security Command Center.

## DNS, HTTP/HTTPS, gRPC (service-to-service communication)
- **DNS**: resolves hostnames to IP addresses; in Kubernetes, services get automatic
  internal DNS names (e.g. `myservice.mynamespace.svc.cluster.local`).
- **HTTP/HTTPS**: request/response protocol; HTTPS adds TLS encryption (see
  ssl_tls_https_letsencrypt.md).
- **gRPC**: a high-performance RPC framework using HTTP/2 and Protocol Buffers, common
  for internal service-to-service communication where JSON/REST overhead matters.

## Reverse proxies, API gateways, ingress controllers
- **Reverse proxy** (e.g. Nginx): sits in front of one or more backend servers,
  forwarding requests — used for TLS termination, load balancing, caching.
- **API Gateway** (e.g. AWS API Gateway, NGINX as a gateway): a managed entry point for
  APIs, adding rate limiting, authentication, request transformation.
- **Ingress Controller** (Kubernetes): implements Ingress resources to route external
  traffic to services inside the cluster, often also handling TLS termination.

## Common errors & fixes
- **Service reachable internally but not externally**: check both the
  firewall/security group AND that a public-facing load balancer/ingress actually
  routes to it — internal reachability doesn't imply external reachability.
- **"Connection timed out" vs "Connection refused"**: timed out usually means a
  firewall is silently dropping packets; refused means the port is reachable but
  nothing is listening there — this distinction narrows down where to look first.
- **Intermittent connection failures between services**: check DNS resolution first
  (a flaky DNS lookup is a very common hidden cause), then check for connection pool
  exhaustion or load balancer health check misconfiguration.
