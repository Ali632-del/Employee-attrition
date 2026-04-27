# Deploy with Docker

## Complete Docker Deployment Guide

Deploy the Employee Attrition Prediction System using Docker containers for maximum portability and scalability.

---

## Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Hub account (optional, for image hosting)
- Project files ready

---

## Step 1: Create Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_CLIENT_SHOWERRORDETAILS=true

# Create .streamlit directory
RUN mkdir -p ~/.streamlit

# Create streamlit config
RUN echo "[theme]\n\
primaryColor = \"#1f77b4\"\n\
backgroundColor = \"#ffffff\"\n\
secondaryBackgroundColor = \"#f0f2f6\"\n\
textColor = \"#262730\"\n\
\n\
[client]\n\
showErrorDetails = true\n\
\n\
[server]\n\
port = 8501\n\
headless = true" > ~/.streamlit/config.toml

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app
CMD ["streamlit", "run", "app.py"]
```

---

## Step 2: Build Docker Image

### 2.1 Build Locally

```bash
cd /home/ubuntu/attrition_project

# Build image
docker build -t employee-attrition:latest .

# Verify build
docker images | grep employee-attrition
```

### 2.2 Build with Custom Tags

```bash
# Tag with version
docker build -t employee-attrition:1.0 .

# Tag with registry
docker build -t myregistry.azurecr.io/employee-attrition:latest .
```

---

## Step 3: Run Docker Container Locally

### 3.1 Basic Run

```bash
docker run -p 8501:8501 employee-attrition:latest
```

### 3.2 Run with Custom Name

```bash
docker run --name attrition-app -p 8501:8501 employee-attrition:latest
```

### 3.3 Run in Background

```bash
docker run -d --name attrition-app -p 8501:8501 employee-attrition:latest
```

### 3.4 View Logs

```bash
# View logs
docker logs attrition-app

# Follow logs
docker logs -f attrition-app
```

### 3.5 Stop Container

```bash
docker stop attrition-app
docker rm attrition-app
```

### 3.6 Access App

- Open browser: `http://localhost:8501`
- Or: `http://127.0.0.1:8501`

---

## Step 4: Push to Docker Hub

### 4.1 Login to Docker Hub

```bash
docker login
# Enter username and password
```

### 4.2 Tag Image

```bash
docker tag employee-attrition:latest YOUR_USERNAME/employee-attrition:latest
docker tag employee-attrition:latest YOUR_USERNAME/employee-attrition:1.0
```

### 4.3 Push Image

```bash
docker push YOUR_USERNAME/employee-attrition:latest
docker push YOUR_USERNAME/employee-attrition:1.0
```

### 4.4 Verify

Go to [Docker Hub](https://hub.docker.com/) and verify your image is published.

---

## Step 5: Deploy to Cloud Platforms

### 5.1 AWS EC2

#### Launch EC2 Instance

1. Go to AWS Console
2. Launch EC2 instance (Ubuntu 22.04)
3. Configure security groups to allow port 8501

#### SSH into Instance

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### Install Docker

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker ubuntu
newgrp docker
```

#### Run Container

```bash
# Pull image
docker pull YOUR_USERNAME/employee-attrition:latest

# Run container
docker run -d -p 8501:8501 YOUR_USERNAME/employee-attrition:latest
```

#### Access App

```
http://your-instance-ip:8501
```

---

### 5.2 Google Cloud Run

#### Prerequisites

```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash

# Initialize
gcloud init

# Set project
gcloud config set project YOUR_PROJECT_ID
```

#### Build and Push to Google Container Registry

```bash
# Configure Docker
gcloud auth configure-docker

# Build image
docker build -t gcr.io/YOUR_PROJECT_ID/employee-attrition:latest .

# Push image
docker push gcr.io/YOUR_PROJECT_ID/employee-attrition:latest
```

#### Deploy to Cloud Run

```bash
gcloud run deploy employee-attrition \
  --image gcr.io/YOUR_PROJECT_ID/employee-attrition:latest \
  --platform managed \
  --region us-central1 \
  --port 8501 \
  --memory 2Gi \
  --timeout 3600
```

#### Get URL

```bash
gcloud run services describe employee-attrition --region us-central1
```

---

### 5.3 Azure Container Instances

#### Prerequisites

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login
```

#### Create Resource Group

```bash
az group create \
  --name attrition-rg \
  --location eastus
```

#### Create Container Registry

```bash
az acr create \
  --resource-group attrition-rg \
  --name attritionregistry \
  --sku Basic
```

#### Build and Push

```bash
az acr build \
  --registry attritionregistry \
  --image employee-attrition:latest .
```

#### Deploy Container

```bash
az container create \
  --resource-group attrition-rg \
  --name attrition-app \
  --image attritionregistry.azurecr.io/employee-attrition:latest \
  --ports 8501 \
  --environment-variables \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true
```

#### Get URL

```bash
az container show \
  --resource-group attrition-rg \
  --name attrition-app \
  --query ipAddress.fqdn
```

---

### 5.4 DigitalOcean App Platform

#### Create App Spec

Create `app.yaml`:

```yaml
name: employee-attrition
services:
- name: web
  github:
    repo: YOUR_USERNAME/employee-attrition
    branch: main
  build_command: pip install -r requirements.txt
  run_command: streamlit run app.py
  http_port: 8501
  envs:
  - key: STREAMLIT_SERVER_PORT
    value: "8501"
  - key: STREAMLIT_SERVER_HEADLESS
    value: "true"
```

#### Deploy

```bash
# Install doctl
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz
tar xf ~/doctl-1.94.0-linux-amd64.tar.gz
sudo mv ~/doctl /usr/local/bin

# Authenticate
doctl auth init

# Create app
doctl apps create --spec app.yaml
```

---

## Step 6: Docker Compose (Multiple Services)

Create `docker-compose.yml` for more complex setups:

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - ./emp_attrition.csv:/app/emp_attrition.csv
      - ./best_model.pkl:/app/best_model.pkl
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: PostgreSQL database
  postgres:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Run with Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Step 7: Optimize Docker Image

### 7.1 Multi-Stage Build

Create optimized `Dockerfile.prod`:

```dockerfile
# Stage 1: Build
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . /app

ENV PATH=/root/.local/bin:$PATH
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build:
```bash
docker build -f Dockerfile.prod -t employee-attrition:prod .
```

### 7.2 Reduce Image Size

```bash
# Check image size
docker images employee-attrition

# Use alpine base (smaller)
FROM python:3.9-alpine

# Install only necessary packages
RUN apk add --no-cache build-base
```

---

## Step 8: Monitoring and Logging

### 8.1 View Container Logs

```bash
# Real-time logs
docker logs -f attrition-app

# Last 100 lines
docker logs --tail 100 attrition-app

# With timestamps
docker logs -t attrition-app
```

### 8.2 Monitor Resources

```bash
# CPU and memory usage
docker stats attrition-app

# Detailed inspection
docker inspect attrition-app
```

### 8.3 Health Checks

```bash
# Check health
docker ps --filter "name=attrition-app"

# Manual health check
curl http://localhost:8501/_stcore/health
```

---

## Step 9: Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
docker run -p 8502:8501 employee-attrition:latest
```

### Issue: Container Exits Immediately

```bash
# Check logs
docker logs attrition-app

# Run with interactive terminal
docker run -it employee-attrition:latest /bin/bash
```

### Issue: Out of Memory

```bash
# Increase memory limit
docker run -m 2g -p 8501:8501 employee-attrition:latest

# Check memory usage
docker stats attrition-app
```

### Issue: File Not Found

```bash
# Check files in container
docker run -it employee-attrition:latest ls -la

# Copy files to container
docker cp emp_attrition.csv attrition-app:/app/
```

---

## Step 10: Security Best Practices

### 10.1 Use Non-Root User

```dockerfile
RUN useradd -m -u 1000 streamlit
USER streamlit
```

### 10.2 Scan for Vulnerabilities

```bash
# Install Trivy
wget https://github.com/aquasecurity/trivy/releases/download/v0.40.0/trivy_0.40.0_Linux-64bit.tar.gz
tar xzf trivy_0.40.0_Linux-64bit.tar.gz

# Scan image
./trivy image employee-attrition:latest
```

### 10.3 Use Private Registry

```bash
# Push to private registry
docker tag employee-attrition:latest myregistry.azurecr.io/employee-attrition:latest
docker push myregistry.azurecr.io/employee-attrition:latest

# Pull from private registry
docker run myregistry.azurecr.io/employee-attrition:latest
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Build image | `docker build -t employee-attrition:latest .` |
| Run container | `docker run -p 8501:8501 employee-attrition:latest` |
| View logs | `docker logs -f container-id` |
| Stop container | `docker stop container-id` |
| Remove container | `docker rm container-id` |
| Push to Hub | `docker push username/employee-attrition:latest` |
| List images | `docker images` |
| List containers | `docker ps -a` |

---

## Useful Links

- **Docker Docs**: https://docs.docker.com/
- **Docker Hub**: https://hub.docker.com/
- **Streamlit Docker**: https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker
- **AWS ECS**: https://aws.amazon.com/ecs/
- **Google Cloud Run**: https://cloud.google.com/run/docs

---

**Last Updated**: April 26, 2026

**Deployment Time**: ~5-15 minutes

**Cost**: Varies by platform (free tier available on most)
