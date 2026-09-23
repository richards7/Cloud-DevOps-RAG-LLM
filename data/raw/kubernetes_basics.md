# Kubernetes Basics

Kubernetes (K8s) is a container orchestration platform: it automates
deploying, scaling, and managing containerized applications across a
cluster of machines. Where Docker runs a single container, Kubernetes
manages many containers across many nodes.

## Core objects
- **Pod**: the smallest deployable unit — one or more tightly coupled
  containers that share networking and storage. Most pods run a single
  container.
- **Deployment**: describes the desired state for a set of pods (how
  many replicas, which image, update strategy) and keeps that state
  running, replacing failed pods automatically.
- **Service**: a stable network endpoint that routes traffic to a set
  of pods, even as individual pods are created or destroyed.
- **ReplicaSet**: ensures a specified number of identical pod replicas
  are running at any time; Deployments manage ReplicaSets automatically.

## How it relates to Docker
Docker builds and runs individual containers. Kubernetes orchestrates
many containers across a cluster — handling scheduling, self-healing
(restarting failed containers), load balancing, and rolling updates.
You still use Docker (or another container runtime) to build the images
that Kubernetes deploys.

## A simple kubectl example
```
kubectl apply -f deployment.yaml     # create/update a deployment
kubectl get pods                      # list running pods
kubectl get services                  # list services
kubectl logs <pod-name>                # view logs from a pod
kubectl scale deployment my-app --replicas=3
```

## When to use Kubernetes vs Cloud Run
Cloud Run is simpler and ideal for stateless, single-container services
like a REST API. Kubernetes (GKE) is a better fit when you need finer
control — multiple interacting services, custom networking, stateful
workloads, or very specific scaling/scheduling rules. For a fresher-level
AI API project, Cloud Run is usually the right choice; Kubernetes is
worth knowing conceptually even if you don't deploy to it directly.
