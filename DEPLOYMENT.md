# Deployment Guide - Employee Attrition Prediction System

## 📋 Table of Contents

1. [Local Development](#local-development)

1. [Streamlit Community Cloud](#streamlit-community-cloud)

1. [Docker Deployment](#docker-deployment)

1. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Python 3.8 or higher

- pip or conda package manager

- Git (for version control)

### Step-by-Step Setup

#### Option 1: Using Setup Script (Recommended)

```bash
# Navigate to project directory
cd employee_attrition_project

# Run setup script
bash setup.sh

# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run app.py
```

#### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Accessing the Application

- **Local URL**: [http://localhost:8501](http://localhost:8501)

- **Network URL**: http://{your-ip}:8501

### Development Tips

- Use `--logger.level=debug` for detailed logs

- Use `--client.toolbarMode=developer` for development mode

- Hot reload is enabled by default

---

## Streamlit Community Cloud

### Prerequisites

- GitHub account

- Streamlit Community Cloud account (free )

- Project pushed to GitHub

### Deployment Steps

#### 1. Prepare Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Employee Attrition Prediction System"

# Add remote repository
git remote add origin https://github.com/yourusername/employee-attrition.git

# Push to GitHub
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

1. Click "New app"

1. Select your repository:
  - **Repository**: yourusername/employee-attrition
  - **Branch**: main
  - **Main file path**: app.py

1. Click "Deploy"

#### 3. Configure Settings (if needed)

- **Advanced settings**: Configure environment variables

- **Secrets**: Add sensitive data (API keys, etc.)

- **Resources**: Adjust CPU/RAM allocation

### Monitoring Deployment

- View logs in the Streamlit Cloud dashboard

- Check app status and performance metrics

- Monitor resource usage

### Updating Deployment

Simply push changes to GitHub:

```bash
git add .
git commit -m "Update: Description of changes"
git push origin main
```

The app will automatically redeploy with the latest changes.

---

## Docker Deployment

### Prerequisites

- Docker installed

- Docker Hub account (for image hosting)

### Create Dockerfile

```
FROM python:3.9-slim

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Run the app
CMD ["streamlit", "run", "app.py"]
```

### Build and Run Docker Image

#### Build Image

```bash
docker build -t employee-attrition:latest .
```

#### Run Container

```bash
docker run -p 8501:8501 employee-attrition:latest
```

#### Push to Docker Hub

```bash
# Tag image
docker tag employee-attrition:latest yourusername/employee-attrition:latest

# Login to Docker Hub
docker login

# Push image
docker push yourusername/employee-attrition:latest
```

### Deploy to Cloud Platforms

#### AWS EC2

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum install docker -y
sudo systemctl start docker

# Pull and run image
docker run -d -p 8501:8501 yourusername/employee-attrition:latest
```

#### Google Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/your-project/employee-attrition

# Deploy
gcloud run deploy employee-attrition \
  --image gcr.io/your-project/employee-attrition \
  --platform managed \
  --region us-central1 \
  --port 8501
```

#### Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry myregistry --image employee-attrition:latest .

# Deploy
az container create \
  --resource-group mygroup \
  --name employee-attrition \
  --image myregistry.azurecr.io/employee-attrition:latest \
  --ports 8501 \
  --environment-variables STREAMLIT_SERVER_PORT=8501
```

---

## Production Considerations

### Security

- [ ] Use HTTPS/SSL certificates

- [ ] Implement authentication (OAuth, API keys)

- [ ] Secure sensitive data in environment variables

- [ ] Use secrets management (AWS Secrets Manager, etc.)

- [ ] Enable CORS if needed

### Performance

- [ ] Enable caching with `@st.cache_resource`

- [ ] Optimize data loading

- [ ] Use CDN for static assets

- [ ] Monitor resource usage

- [ ] Set up auto-scaling if needed

### Monitoring & Logging

- [ ] Set up application monitoring (DataDog, New Relic)

- [ ] Configure logging (CloudWatch, ELK Stack)

- [ ] Set up alerts for errors

- [ ] Monitor model performance drift

- [ ] Track user interactions

### Maintenance

- [ ] Regular backups of data and models

- [ ] Version control for all changes

- [ ] Regular dependency updates

- [ ] Model retraining schedule

- [ ] Documentation updates

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError"

**Problem**: Missing Python packages

```bash
# Solution
pip install -r requirements.txt
```

#### 2. "FileNotFoundError" for CSV or Model Files

**Problem**: Files not in correct location

```bash
# Solution: Ensure all files are in project directory
ls -la app.py best_model.pkl preprocessor.pkl emp_attrition.csv
```

#### 3. Slow App Performance

**Problem**: Large dataset or inefficient code

```python
# Solution: Add caching
@st.cache_resource
def load_data():
    return pd.read_csv('emp_attrition.csv')
```

#### 4. Port Already in Use

**Problem**: Port 8501 is occupied

```bash
# Solution: Use different port
streamlit run app.py --server.port 8502
```

#### 5. Memory Issues

**Problem**: App crashes due to memory

```bash
# Solution: Reduce dataset size or optimize preprocessing
# Use sampling for large datasets
df = df.sample(frac=0.8, random_state=42)
```

### Debugging

#### Enable Debug Mode

```bash
streamlit run app.py --logger.level=debug
```

#### Check Logs

```bash
# View Streamlit logs
tail -f ~/.streamlit/logs/

# View Docker logs
docker logs container-id
```

#### Performance Profiling

```python
import streamlit as st
import time

@st.cache_resource
def load_model():
    start = time.time()
    model = joblib.load('best_model.pkl')
    st.write(f"Model loaded in {time.time() - start:.2f}s")
    return model
```

---

## Deployment Checklist

- [ ] All dependencies listed in requirements.txt

- [ ] Model and preprocessor files present

- [ ] Dataset file included

- [ ] README.md updated with instructions

- [ ] Code tested locally

- [ ] No hardcoded paths or credentials

- [ ] Environment variables configured

- [ ] Error handling implemented

- [ ] Logging configured

- [ ] Performance optimized

- [ ] Security measures in place

- [ ] Documentation complete

---

## Support & Resources

- **Streamlit Docs**: [https://docs.streamlit.io/](https://docs.streamlit.io/)

- **Streamlit Community**: [https://discuss.streamlit.io/](https://discuss.streamlit.io/)

- **GitHub Issues**: Create an issue in your repository

- **Stack Overflow**: Tag with `streamlit`

---

## Additional Resources

### Streamlit Deployment Options

- [Streamlit Cloud](https://streamlit.io/cloud)

- [Heroku](https://www.heroku.com/)

- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)

- [Google Cloud Run](https://cloud.google.com/run)

- [Azure Container Instances](https://azure.microsoft.com/services/container-instances/)

### Model Serving Alternatives

- [FastAPI](https://fastapi.tiangolo.com/) - REST API

- [Flask](https://flask.palletsprojects.com/) - Web framework

- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving) - Model serving

- [Seldon Core](https://www.seldon.io/) - ML model deployment

---

**Last Updated**: April 26, 2026

