# Deployment Quick Start Guide

## Choose Your Deployment Platform

Quick comparison and setup instructions for all deployment options.

---

## Platform Comparison

| Platform | Cost | Setup Time | Ease | Best For |
|----------|------|-----------|------|----------|
| **Streamlit Cloud** | Free | 2-5 min | ⭐⭐⭐⭐⭐ | Fastest deployment |
| **Heroku** | Free/Paid | 5-10 min | ⭐⭐⭐⭐ | Simple apps |
| **Docker + AWS** | Paid | 15-30 min | ⭐⭐⭐ | Scalable apps |
| **Google Cloud Run** | Free/Paid | 10-15 min | ⭐⭐⭐ | Serverless |
| **Azure** | Free/Paid | 10-15 min | ⭐⭐⭐ | Enterprise |

---

## 🚀 Fastest: Streamlit Cloud (Recommended)

### 5-Minute Setup

```bash
# 1. Push to GitHub
cd /home/ubuntu/attrition_project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/employee-attrition.git
git push -u origin main

# 2. Deploy
# Go to: https://share.streamlit.io
# Click "New app"
# Select your repository and app.py
# Done! ✅
```

**Pros:**
- ✅ Completely free
- ✅ Automatic deployment on push
- ✅ No configuration needed
- ✅ Built for Streamlit

**Cons:**
- ❌ Limited to Streamlit apps
- ❌ Free tier has resource limits

**See**: `DEPLOY_STREAMLIT_CLOUD.md`

---

## 💰 Affordable: Heroku

### 10-Minute Setup

```bash
# 1. Install Heroku CLI
brew install heroku  # macOS
# or download from heroku.com

# 2. Create Procfile
echo "web: sh setup.sh && streamlit run app.py" > Procfile

# 3. Deploy
heroku login
heroku create employee-attrition-app
git push heroku main
heroku open
```

**Pros:**
- ✅ Simple deployment
- ✅ Free tier available
- ✅ Good documentation
- ✅ Custom domains

**Cons:**
- ❌ Free tier sleeps after 30 min
- ❌ Paid tier required for production

**Cost**: Free or $7+/month

**See**: `DEPLOY_HEROKU.md`

---

## 🐳 Scalable: Docker + Cloud

### AWS EC2 (15 minutes)

```bash
# 1. Build Docker image
docker build -t employee-attrition:latest .

# 2. Tag for AWS
docker tag employee-attrition:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/employee-attrition:latest

# 3. Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/employee-attrition:latest

# 4. Launch EC2 and run:
docker run -p 8501:8501 YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/employee-attrition:latest
```

**Pros:**
- ✅ Highly scalable
- ✅ Full control
- ✅ Production-ready
- ✅ Cost-effective

**Cons:**
- ❌ More complex setup
- ❌ Requires AWS knowledge
- ❌ Pay for compute

**Cost**: $5-20+/month

**See**: `DEPLOY_DOCKER.md`

---

### Google Cloud Run (15 minutes)

```bash
# 1. Build image
docker build -t gcr.io/YOUR_PROJECT/employee-attrition:latest .

# 2. Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT/employee-attrition:latest

# 3. Deploy
gcloud run deploy employee-attrition \
  --image gcr.io/YOUR_PROJECT/employee-attrition:latest \
  --platform managed \
  --region us-central1 \
  --port 8501
```

**Pros:**
- ✅ Serverless (no server management)
- ✅ Pay per use
- ✅ Auto-scaling
- ✅ Free tier available

**Cons:**
- ❌ Slightly higher latency
- ❌ Cold start delays

**Cost**: Free tier + pay per use

**See**: `DEPLOY_DOCKER.md`

---

## 📋 Step-by-Step Decision Tree

```
Start Here
    ↓
Do you want the fastest setup?
    ├─ YES → Use Streamlit Cloud ⭐
    └─ NO → Continue
         ↓
    Do you have AWS/GCP/Azure account?
         ├─ YES → Use Docker + Cloud ⭐⭐
         └─ NO → Continue
              ↓
         Do you want free tier?
              ├─ YES → Use Heroku Free ⭐
              └─ NO → Use Heroku Paid ⭐⭐
```

---

## Pre-Deployment Checklist

- [ ] All files committed to Git
- [ ] `requirements.txt` up to date
- [ ] `app.py` runs locally without errors
- [ ] Model files (`best_model.pkl`, `preprocessor.pkl`) present
- [ ] Dataset file (`emp_attrition.csv`) present
- [ ] README.md updated
- [ ] `.gitignore` configured
- [ ] No hardcoded secrets or passwords
- [ ] Environment variables documented

---

## Deployment Verification

After deployment, verify:

1. **App Loads**
   - Navigate to app URL
   - Check for errors in browser console

2. **Navigation Works**
   - Click through all pages
   - Verify sidebar navigation

3. **Data Loads**
   - Check Data Overview page
   - Verify dataset displays

4. **Visualizations Render**
   - Go to Data Analysis page
   - Check all charts load

5. **Predictions Work**
   - Go to Predictions page
   - Enter sample data
   - Verify prediction output

6. **Model Info Displays**
   - Go to Model Info page
   - Check feature importance chart

---

## Common Issues & Quick Fixes

### "ModuleNotFoundError"
```bash
# Add missing package to requirements.txt
echo "package-name==version" >> requirements.txt
git add requirements.txt
git commit -m "Add dependency"
git push
```

### "FileNotFoundError"
```bash
# Ensure files are tracked in Git
git add emp_attrition.csv best_model.pkl preprocessor.pkl
git commit -m "Add data and models"
git push
```

### "App Too Slow"
```python
# Add caching to app.py
@st.cache_resource
def load_model():
    return joblib.load('best_model.pkl')
```

### "Port Already in Use"
```bash
# Use different port locally
streamlit run app.py --server.port 8502
```

---

## Monitoring After Deployment

### Streamlit Cloud
- Dashboard shows usage stats
- View logs in app settings
- Monitor resource usage

### Heroku
```bash
heroku logs --tail  # Real-time logs
heroku ps           # Check dyno status
```

### Docker + Cloud
- Use cloud provider's monitoring
- Set up CloudWatch/Stackdriver
- Configure alerts

---

## Update Your App

### For All Platforms

```bash
# Make changes locally
nano app.py

# Test locally
streamlit run app.py

# Commit and push
git add .
git commit -m "Update: description"
git push origin main

# For Heroku specifically:
git push heroku main
```

**Automatic Redeployment:**
- Streamlit Cloud: Automatic on push
- Heroku: Automatic if connected to GitHub
- Docker: Manual redeploy needed

---

## Performance Tips

1. **Use Caching**
   ```python
   @st.cache_resource
   def load_model():
       return joblib.load('best_model.pkl')
   ```

2. **Lazy Load Data**
   ```python
   if st.checkbox("Show data"):
       df = load_data()
   ```

3. **Optimize Images**
   - Compress images before upload
   - Use appropriate formats (PNG, JPEG)

4. **Reduce Package Size**
   - Remove unused dependencies
   - Use slim versions

---

## Cost Breakdown

### Monthly Costs (Approximate)

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Streamlit Cloud | ✅ Unlimited | N/A |
| Heroku | ✅ Limited | $7-50+ |
| AWS EC2 | ❌ (12 months) | $5-20+ |
| Google Cloud Run | ✅ Limited | Pay per use |
| Azure | ✅ Limited | Pay per use |

---

## Support Resources

### Streamlit
- Docs: https://docs.streamlit.io/
- Community: https://discuss.streamlit.io/
- GitHub: https://github.com/streamlit/streamlit

### Heroku
- Docs: https://devcenter.heroku.com/
- Support: https://help.heroku.com/

### Docker
- Docs: https://docs.docker.com/
- Hub: https://hub.docker.com/

### Cloud Providers
- AWS: https://aws.amazon.com/support/
- GCP: https://cloud.google.com/support
- Azure: https://azure.microsoft.com/support/

---

## Next Steps

1. **Choose Platform** - Pick from the comparison table
2. **Read Full Guide** - See specific deployment guide
3. **Deploy** - Follow step-by-step instructions
4. **Verify** - Test all features
5. **Monitor** - Watch logs and performance
6. **Update** - Push changes as needed

---

## Quick Links

- **Streamlit Cloud**: https://share.streamlit.io/
- **Heroku**: https://www.heroku.com/
- **AWS**: https://aws.amazon.com/
- **Google Cloud**: https://cloud.google.com/
- **Azure**: https://azure.microsoft.com/
- **Docker Hub**: https://hub.docker.com/

---

**Recommended for First-Time Users**: Streamlit Cloud ⭐

**Recommended for Production**: Docker + AWS/GCP ⭐⭐⭐

---

**Last Updated**: April 26, 2026

**Total Deployment Options**: 5+

**Estimated Setup Time**: 2-30 minutes (depending on platform)
