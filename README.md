---
````markdown
# Food-Nexus: Sentiment Analysis of Food Waste Conversations with Food Balance Data

## Overview

**Food-Nexus** is a Django-based web application designed to analyze sentiment in conversations around food waste and hunger. It leverages actual food balance data from various countries and integrates data visualization and machine learning techniques to raise awareness of food sustainability issues.

The application is containerized using Docker, deployed via Kubernetes with Helm charts, and continuously delivered through ArgoCD following GitOps best practices.

---

## Features

- 🔍 Sentiment analysis API using natural language processing
- 📊 Visualizations via Power BI (embedded or linked)
- 🐳 Dockerized for easy deployment
- ☸️ Kubernetes-ready with Helm charts
- 🚀 ArgoCD GitOps deployment support

---

## Prerequisites

Before getting started, make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Minikube](https://minikube.sigs.k8s.io/docs/) or access to any Kubernetes cluster
- [Helm](https://helm.sh/)
- [ArgoCD](https://argo-cd.readthedocs.io/)
- [Git](https://git-scm.com/)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AnkurMangroliya/Food-Nexus.git
cd Food-Nexus
````

### 2. Set Up Python Virtual Environment (Optional but Recommended)

```bash
python3 -m venv my_env
source my_env/bin/activate  # Linux/macOS
# On Windows PowerShell:
# .\my_env\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations and Start the Server

```bash
python manage.py migrate
python manage.py runserver
```

### 5. Access the Application

Open your browser and navigate to:

```
http://localhost:8000
```

---

## Docker Setup

### 1. Build Docker Image

```bash
docker build -t <your-dockerhub-username>/food-nexus:latest .
```

### 2. Run Docker Container Locally

```bash
docker run -p 8000:8000 <your-dockerhub-username>/food-nexus:latest
```

Visit the app at `http://localhost:8000`

### 3. Push Docker Image to Docker Hub

```bash
docker push <your-dockerhub-username>/food-nexus:latest
```

---

## Kubernetes Deployment Using Helm

### 1. Update `values.yaml`

In the Helm chart directory (`food-nexus-chart/values.yaml`), update the image repository and tag:

```yaml
image:
  repository: <your-dockerhub-username>/food-nexus
  tag: latest
  pullPolicy: IfNotPresent
replicaCount: 2
```

### 2. Deploy Helm Chart

```bash
helm install food-nexus ./food-nexus-chart
```

To upgrade deployment after changes:

```bash
helm upgrade food-nexus ./food-nexus-chart
```

### 3. Access the Application

If no ingress controller is set up, use port forwarding:

```bash
kubectl port-forward svc/food-nexus-service 8080:8000
```

Open in browser:

```
http://localhost:8080
```

---

## Health Check Endpoints

To ensure Kubernetes can monitor pod health, implement these probes.

### 1. Add Health Check View in Django

In `urls.py` or a dedicated views file:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})
```

Add to your URL patterns:

```python
path('healthz/', health_check, name='healthz'),
```

### 2. Configure Probes in Helm Chart Deployment YAML

Example snippet:

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /healthz
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3
```

---

## ArgoCD GitOps Setup

### 1. Install ArgoCD on Your Cluster

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Access ArgoCD UI

Port forward ArgoCD server:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Get the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

Open the UI in your browser:

```
https://localhost:8080
```

Login with username `admin` and the retrieved password.

### 3. Create an Application in ArgoCD

```bash
argocd app create food-nexus \
  --repo https://github.com/AnkurMangroliya/Food-Nexus.git \
  --path food-nexus-chart \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```

### 4. Sync the Application

```bash
argocd app sync food-nexus
```

This will deploy your app to the Kubernetes cluster and ArgoCD will monitor for changes.

---

## Project Structure

```
Food-Nexus/
├── Dockerfile
├── food-nexus-chart/          # Helm chart directory
│   ├── templates/
│   └── values.yaml
├── food_nexus_app/            # Django app source code
│   ├── views.py
│   ├── urls.py
│   └── ...
├── manage.py
├── requirements.txt
└── README.md
```

---

## Contributors

* [Ankur Mangroliya](https://github.com/AnkurMangroliya)
* [Akshar Patel](https://github.com/akshar2223)
* [Arjun Patel](https://github.com/Arjun100701)
* [Happy Mehta](https://github.com/HappyMehta)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

Special thanks to the University of Windsor for their support and guidance throughout this project.
