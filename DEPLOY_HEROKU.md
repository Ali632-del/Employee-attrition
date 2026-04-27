# Deploy to Heroku

## Complete Heroku Deployment Guide

Deploy the Employee Attrition Prediction System to Heroku for free or paid hosting.

---

## Prerequisites

- Heroku account ([Sign up](https://www.heroku.com/))
- Heroku CLI installed ([Install](https://devcenter.heroku.com/articles/heroku-cli))
- Git installed
- Project files ready

---

## Step 1: Install Heroku CLI

### macOS

```bash
brew tap heroku/brew && brew install heroku
```

### Windows

Download from [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### Linux

```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Verify Installation

```bash
heroku --version
```

---

## Step 2: Create Heroku Configuration Files

### 2.1 Create Procfile

Create `Procfile` in project root:

```
web: sh setup.sh && streamlit run app.py
```

### 2.2 Create setup.sh

Create `setup.sh`:

```bash
#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"\"\n\
\n\
[client]\n\
showErrorDetails = false\n\
\n\
[server]\n\
port = $PORT\n\
enableXsrfProtection = false\n\
headless = true\n\
" > ~/.streamlit/config.toml
```

### 2.3 Create runtime.txt

Create `runtime.txt`:

```
python-3.9.16
```

### 2.4 Verify requirements.txt

Ensure `requirements.txt` exists with all dependencies:

```bash
cat requirements.txt
```

---

## Step 3: Initialize Git Repository

```bash
cd /home/ubuntu/attrition_project

# Initialize git
git init

# Configure user
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Employee Attrition Prediction System"
```

---

## Step 4: Deploy to Heroku

### 4.1 Login to Heroku

```bash
heroku login
```

Follow the browser prompt to authenticate.

### 4.2 Create Heroku App

```bash
heroku create employee-attrition-app
```

Or with custom name:

```bash
heroku create your-custom-app-name
```

### 4.3 Deploy Code

```bash
git push heroku main
```

Or if using different branch:

```bash
git push heroku your-branch:main
```

### 4.4 View Deployment

```bash
# Open app in browser
heroku open

# View logs
heroku logs --tail
```

---

## Step 5: Configure App

### 5.1 Set Environment Variables

```bash
# Set single variable
heroku config:set STREAMLIT_SERVER_HEADLESS=true

# Set multiple variables
heroku config:set \
  STREAMLIT_SERVER_PORT=8501 \
  STREAMLIT_SERVER_HEADLESS=true \
  STREAMLIT_CLIENT_SHOWERRORDETAILS=false
```

### 5.2 View Configuration

```bash
heroku config
```

### 5.3 Unset Variables

```bash
heroku config:unset VARIABLE_NAME
```

---

## Step 6: Monitor App

### 6.1 View Logs

```bash
# Real-time logs
heroku logs --tail

# Last 50 lines
heroku logs -n 50

# Specific dyno
heroku logs --dyno web
```

### 6.2 Check App Status

```bash
heroku ps
```

### 6.3 Restart App

```bash
heroku restart
```

### 6.4 Scale Dynos

```bash
# View current dynos
heroku ps

# Scale web dyno
heroku ps:scale web=1

# Scale to multiple instances
heroku ps:scale web=2
```

---

## Step 7: Update Your App

### 7.1 Make Local Changes

```bash
# Edit files
nano app.py

# Test locally
streamlit run app.py
```

### 7.2 Commit and Push

```bash
# Stage changes
git add .

# Commit
git commit -m "Update: Description of changes"

# Push to Heroku
git push heroku main
```

### 7.3 Monitor Deployment

```bash
# Watch logs during deployment
heroku logs --tail
```

---

## Step 8: Custom Domain (Optional)

### 8.1 Add Domain

```bash
heroku domains:add www.yourdomain.com
```

### 8.2 Configure DNS

1. Go to your domain registrar
2. Add CNAME record pointing to Heroku
3. Wait for DNS propagation (up to 48 hours)

### 8.3 Verify Domain

```bash
heroku domains
```

---

## Step 9: Add-ons (Optional)

### 9.1 Add PostgreSQL Database

```bash
# Add free tier database
heroku addons:create heroku-postgresql:hobby-dev

# View database URL
heroku config:get DATABASE_URL
```

### 9.2 Add Redis Cache

```bash
heroku addons:create heroku-redis:premium-0
```

### 9.3 View Add-ons

```bash
heroku addons
```

---

## Step 10: Troubleshooting

### Issue: "Slug size too large"

**Cause**: Repository too large

**Solution**:
```bash
# Remove unnecessary files
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".git" >> .gitignore

# Rebuild slug
git add .gitignore
git commit -m "Update gitignore"
git push heroku main
```

### Issue: "No such file or directory: app.py"

**Cause**: File not committed to Git

**Solution**:
```bash
git add app.py
git commit -m "Add app.py"
git push heroku main
```

### Issue: "ModuleNotFoundError"

**Cause**: Missing dependencies

**Solution**:
```bash
# Add to requirements.txt
echo "package-name==version" >> requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Add missing dependency"
git push heroku main
```

### Issue: "Application error"

**Cause**: Runtime error

**Solution**:
```bash
# Check logs
heroku logs --tail

# Restart app
heroku restart

# View recent logs
heroku logs -n 100
```

### Issue: "H14 No web processes running"

**Cause**: Dyno crashed

**Solution**:
```bash
# Check dyno status
heroku ps

# Restart
heroku restart

# Scale
heroku ps:scale web=1
```

---

## Step 11: Performance Optimization

### 11.1 Use Caching

```python
import streamlit as st

@st.cache_resource
def load_model():
    return joblib.load('best_model.pkl')

@st.cache_data
def load_data():
    return pd.read_csv('emp_attrition.csv')
```

### 11.2 Optimize Dependencies

```bash
# Reduce package size
pip install --no-cache-dir -r requirements.txt

# Use slim versions
# Replace: scipy → scipy (already slim)
# Replace: scikit-learn → scikit-learn (already slim)
```

### 11.3 Lazy Load Resources

```python
if st.checkbox("Show analysis"):
    # Only load if user requests
    df = load_data()
    st.write(df)
```

---

## Step 12: Continuous Deployment

### 12.1 Connect GitHub

```bash
# Enable automatic deployment
heroku apps:create --remote heroku
git push heroku main
```

### 12.2 Deploy on Push

1. Go to Heroku Dashboard
2. Select your app
3. Go to "Deploy" tab
4. Connect to GitHub
5. Select repository
6. Enable "Automatic deploys"

### 12.3 Deploy Specific Branch

```bash
# Deploy from different branch
git push heroku develop:main
```

---

## Step 13: Backup and Restore

### 13.1 Backup Database

```bash
# Create backup
heroku pg:backups:capture

# List backups
heroku pg:backups

# Download backup
heroku pg:backups:download
```

### 13.2 Restore Database

```bash
# Restore from backup
heroku pg:backups:restore b001 DATABASE_URL
```

---

## Step 14: Security

### 14.1 Use Environment Variables for Secrets

```python
import os

database_url = os.environ.get('DATABASE_URL')
api_key = os.environ.get('API_KEY')
```

### 14.2 Set Secrets

```bash
heroku config:set API_KEY="your-secret-key"
heroku config:set DATABASE_URL="postgresql://..."
```

### 14.3 Rotate Secrets

```bash
# Update secret
heroku config:set API_KEY="new-secret-key"

# Verify
heroku config:get API_KEY
```

---

## Step 15: Cleanup

### 15.1 Delete App

```bash
heroku apps:destroy --app employee-attrition-app
```

### 15.2 Remove Remote

```bash
git remote remove heroku
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Login | `heroku login` |
| Create app | `heroku create app-name` |
| Deploy | `git push heroku main` |
| View logs | `heroku logs --tail` |
| Restart | `heroku restart` |
| Set config | `heroku config:set KEY=value` |
| Open app | `heroku open` |
| Check status | `heroku ps` |
| Scale | `heroku ps:scale web=2` |
| Delete app | `heroku apps:destroy --app app-name` |

---

## Pricing

### Free Tier
- 1 free dyno (550 hours/month)
- Limited resources
- Sleeps after 30 minutes of inactivity

### Paid Tiers
- **Hobby**: $7/month (always on)
- **Standard**: $25/month (better performance)
- **Performance**: $50+/month (high performance)

---

## Useful Links

- **Heroku Docs**: https://devcenter.heroku.com/
- **Streamlit on Heroku**: https://devcenter.heroku.com/articles/deploying-python-apps-on-heroku
- **Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
- **Procfile**: https://devcenter.heroku.com/articles/procfile

---

**Last Updated**: April 26, 2026

**Deployment Time**: ~2-5 minutes

**Cost**: Free (with limitations) or $7+/month
