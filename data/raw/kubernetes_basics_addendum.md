# Kubernetes Basics — Additional Common Errors & Fixes
(Supplements kubernetes_basics.md; see also kubernetes_operations.md for deeper
operational troubleshooting.)

- **"error: You must be logged in to the server (Unauthorized)"**: your kubeconfig
  context/credentials are stale — re-run the cluster's get-credentials command (e.g.
  `gcloud container clusters get-credentials` or `aws eks update-kubeconfig`).
- **`kubectl` commands hang with no error**: usually a networking issue reaching the
  cluster's API server — check VPN/firewall rules if the cluster is private.
- **Pod stuck in "ContainerCreating"**: check `kubectl describe pod` for the actual
  cause — commonly a volume mount failing, or the image pull taking unusually long.
