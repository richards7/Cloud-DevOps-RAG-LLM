# Networking & IAM — Additional Common Errors & Fixes
(Supplements networking_iam.md already in the knowledge base.)

- **IAM changes don't seem to take effect immediately**: IAM policy propagation can
  take a short time (seconds to a couple of minutes) to fully apply across a cloud
  provider's infrastructure — wait briefly and retry before assuming the policy is
  wrong.
- **Service account works in one project but "permission denied" in another**: IAM
  roles/bindings are typically scoped per-project (GCP) or per-account (AWS) — the
  same service account needs its own role binding in each project/account it needs
  access to.
- **Firewall rule added but traffic still blocked**: check rule priority/order (some
  systems evaluate rules in order and stop at the first match) and confirm the rule
  applies to the correct direction (ingress vs egress) and the correct resource
  tag/target.
