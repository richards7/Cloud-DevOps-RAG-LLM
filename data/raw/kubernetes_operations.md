# Kubernetes — Operations & Troubleshooting

(See kubernetes_basics.md for core objects: Pod, Deployment, Service, ReplicaSet.)

## More core objects
- **Namespace**: a virtual cluster within a cluster, used to separate environments/teams.
- **ConfigMap**: non-sensitive configuration data injected into pods as env vars/files.
- **Secret**: like a ConfigMap but for sensitive data (base64-encoded, not encrypted by
  default — use a proper secrets manager or encryption-at-rest for real security).
- **Ingress**: routes external HTTP(S) traffic to services based on hostname/path,
  usually backed by an Ingress Controller like NGINX or Traefik.
- **PersistentVolume (PV) / PersistentVolumeClaim (PVC)**: how pods get durable storage
  that survives pod restarts.

## Everyday kubectl commands
```bash
kubectl get pods -n mynamespace
kubectl describe pod mypod -n mynamespace     # detailed status + recent events
kubectl logs mypod -n mynamespace              # container logs
kubectl logs mypod -c my-container --previous  # logs from a crashed previous instance
kubectl exec -it mypod -- /bin/sh              # shell into a running pod
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp          # roll back to the previous version
kubectl scale deployment myapp --replicas=5
kubectl port-forward svc/myapp 8080:80         # tunnel a service to your local machine
```

## Common pod states and what they mean
- **Pending**: not yet scheduled — often insufficient cluster resources, or an unmet
  node selector/affinity rule.
- **CrashLoopBackOff**: the container keeps starting and crashing — check
  `kubectl logs` and `kubectl describe pod` for the actual error (bad config, missing
  env var, failing health check).
- **ImagePullBackOff**: Kubernetes can't pull the container image — wrong image name/tag,
  private registry without correct `imagePullSecrets`, or a typo.
- **OOMKilled**: the container exceeded its memory limit — check `resources.limits.memory`
  in the pod spec and actual usage with `kubectl top pod`.

## Common errors & fixes
- **Service not reachable**: check `kubectl get endpoints <service>` — if empty, the
  service's label selector doesn't match any pod's labels.
- **Ingress returns 404/502**: confirm the Ingress Controller is running, the Ingress
  resource's host/path rules match the request, and the backend service+port are correct.
- **"forbidden: User cannot get resource"**: an RBAC issue — check Role/ClusterRole and
  RoleBinding/ClusterRoleBinding for that user/service account.
- **Deployment stuck rolling out**: check `kubectl rollout status` and `kubectl describe
  deployment` — often a readiness probe never succeeding, blocking the rollout from
  progressing past the first new pod.
