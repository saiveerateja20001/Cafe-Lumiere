Kubernetes Deployment Guide — Cafe Lumiere

Overview
- This guide shows how to deploy the Cafe-Lumiere services on Kubernetes, how services communicate, why you saw cross-node flaky behavior, and how the database is deployed.

Prerequisites
- A functioning Kubernetes cluster with control plane + worker nodes and a CNI installed (Calico, Flannel, etc.).
- `kubectl` configured to talk to the cluster.
- `helm` (if you plan to deploy the bundled Postgres chart).
- Images for services pushed to a registry referenced in `cafe/k8s/deployments.yaml` (or set imagePullPolicy and use local registry).

Files of interest
- `cafe/k8s/deployments.yaml` — namespace, ConfigMap, Secret, Deployments, Services for `order-service`, `kitchen-service`, and `frontend`.
- `cafe/helm/postgresql/` — packaged Helm chart used to deploy Postgres (statefulset + persistent storage).

Why the flaky cross-node behavior happened
- In Docker Compose, services run on the same bridge network and DNS resolution + ordering are simpler.
- On Kubernetes, requests may be routed to pods that are still starting. Without readiness probes Kubernetes can route traffic to a pod before it is ready to accept requests.
- If `kitchen-service` tries to call `order-service` while the `order-service` pod is still initializing (or the database the `order-service` depends on is not ready), the call can fail. This manifests as "works only after multiple clicks" or only one node handling it reliably.
- Additional causes to check: missing CNI or misconfigured cluster networking prevents pod-to-pod traffic across nodes. Ensure your cluster CNI is installed and running.

What I changed to fix it
- Added `readinessProbe` and `livenessProbe` for `order-service`, `kitchen-service`, and `frontend` in `cafe/k8s/deployments.yaml`.
  - Readiness probes keep the Service from sending traffic to a pod until its `/health` endpoint returns OK.
  - Liveness probes allow Kubernetes to restart unhealthy containers.
- These probes reduce race conditions and prevent traffic from being routed to not-ready pods.

Database deployment and initialization
- The repo includes a Helm chart for Postgres at `cafe/helm/postgresql/` (templates include a StatefulSet). Deploying the chart will create a stateful Postgres instance with persistent volume(s).
- `cafe/k8s/deployments.yaml` uses a ConfigMap key `DB_HOST: "cafe-lumiere-postgresql"`. That hostname should match the Service created by the Postgres Helm chart. Confirm the chart creates a Service named `cafe-lumiere-postgresql` or update the ConfigMap to match the Service name produced by your Postgres deployment.
- The `order-service`'s `init_db()` call (in `cafe/order-service/app.py`) runs on startup and creates the `orders` table if it does not exist. This requires the database to be reachable when the `order-service` successfully connects to it.

Deployment steps (apply manifests and Helm)
1. Ensure cluster networking (CNI) is installed and functional.
2. Deploy Postgres (Helm):

```bash
# from repo root
cd cafe/helm/postgresql
helm install cafe-lumiere-postgresql . --namespace cafe-lumiere --create-namespace
```

3. Apply the combined K8s manifests:

```bash
kubectl apply -f cafe/k8s/deployments.yaml
```

4. Watch rollout and readiness:

```bash
kubectl -n cafe-lumiere get pods --watch
kubectl -n cafe-lumiere get services
```

5. Check logs if something is not ready:

```bash
kubectl -n cafe-lumiere describe pod <pod-name>
kubectl -n cafe-lumiere logs <pod-name> -c <container-name>
```

Verification
- Confirm Postgres service exists and is reachable:

```bash
kubectl -n cafe-lumiere get svc
# then from a pod you can test connectivity
kubectl -n cafe-lumiere run -it --rm --restart=Never debug --image=appropriate/curl -- sh
# inside pod
curl http://cafe-lumiere-postgresql:5432 || echo "tcp check failed"
```

- Confirm `order-service` readiness:

```bash
kubectl -n cafe-lumiere get pods -l app=order-service
kubectl -n cafe-lumiere exec -it <order-pod> -- curl -sS http://localhost:5001/health
```

- Confirm `kitchen-service` calls succeed once order-service is ready:

```bash
kubectl -n cafe-lumiere exec -it <kitchen-pod> -- curl -sS http://order-service:5001/health
```

Troubleshooting tips
- If `curl http://order-service:5001/health` fails from `kitchen-service` pod but succeeds locally on node, check cluster DNS and CNI.
- Confirm the Postgres Service name matches `DB_HOST` in the ConfigMap. If mismatched, either change the Helm release/service name or update the ConfigMap in `deployments.yaml`.
- If pods are CrashLooping, `kubectl describe pod` and `kubectl logs` will show the root cause (database connection failures, missing envs, etc.).

Next steps I can do for you
- Run a quick checklist to confirm the Postgres Helm release name and service match the ConfigMap `DB_HOST` value.
- Add explicit `initContainers` to `order-service` to wait for Postgres readiness (optional but robust).

