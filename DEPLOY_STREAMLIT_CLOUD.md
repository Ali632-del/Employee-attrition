# Deploy to Streamlit Community Cloud

## Complete Step-by-Step Guide

Streamlit Community Cloud is the easiest and fastest way to deploy your Streamlit app for free.

---

## Prerequisites

- GitHub account (free)
- Streamlit Community Cloud account (free, linked to GitHub)
- Project pushed to GitHub repository

---

## Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git (if not already done)

```bash
cd /home/ubuntu/attrition_project
git init
```

### 1.2 Configure Git User

```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

### 1.3 Add All Files

```bash
git add .
```

### 1.4 Create Initial Commit

```bash
git commit -m "Initial commit: Employee Attrition Prediction System"
```

### 1.5 Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `employee-attrition`
3. Description: "Employee Attrition Prediction System with ML"
4. Choose: Public (for free deployment)
5. Click "Create repository"

### 1.6 Add Remote and Push

```bash
git remote add origin https://github.com/YOUR_USERNAME/employee-attrition.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Streamlit Cloud

### 2.1 Access Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub repositories

### 2.2 Deploy New App

1. Click "New app" button
2. Fill in deployment details:
   - **Repository**: YOUR_USERNAME/employee-attrition
   - **Branch**: main
   - **Main file path**: app.py
3. Click "Deploy"

### 2.3 Wait for Deployment

- Streamlit will build and deploy your app
- This typically takes 1-2 minutes
- You'll see a URL like: `https://employee-attrition-xxxxx.streamlit.app`

---

## Step 3: Verify Deployment

1. **Check App Status**
   - Go to your app URL
   - Verify all pages load correctly
   - Test predictions functionality

2. **Test Features**
   - Home page loads
   - Data overview displays
   - Visualizations render
   - Predictions work
   - Model info displays

---

## Step 4: Configure App Settings (Optional)

### 4.1 Custom Domain (Premium Feature)

1. Go to app settings
2. Click "Custom domain"
3. Add your domain (requires premium)

### 4.2 Secrets Management

For sensitive data (API keys, credentials):

1. Click "Settings" in app dashboard
2. Go to "Secrets" section
3. Add secrets in TOML format:

```toml
[database]
host = "your-host"
user = "your-user"
password = "your-password"
```

4. Access in code:
```python
import streamlit as st
db_password = st.secrets["database"]["password"]
```

### 4.3 App Configuration

Edit `.streamlit/config.toml` for app settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
showErrorDetails = true
```

---

## Step 5: Update Your App

### 5.1 Make Changes Locally

```bash
cd /home/ubuntu/attrition_project
# Edit files as needed
```

### 5.2 Commit and Push

```bash
git add .
git commit -m "Update: Description of changes"
git push origin main
```

### 5.3 Automatic Redeployment

- Streamlit automatically detects changes
- App redeploys within 1-2 minutes
- No manual action needed

---

## Step 6: Monitor Your App

### 6.1 View Logs

1. Go to app dashboard
2. Click "Manage app"
3. View deployment logs and errors

### 6.2 Check Performance

1. Go to "Manage app"
2. View resource usage
3. Monitor app health

### 6.3 Share App

- Share your app URL: `https://employee-attrition-xxxxx.streamlit.app`
- Anyone can access without authentication (unless you add it)

---

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Cause**: Missing dependencies

**Solution**:
1. Ensure all packages are in `requirements.txt`
2. Push changes to GitHub
3. App will automatically reinstall dependencies

```bash
# Check requirements.txt
cat requirements.txt

# Add missing package
echo "package-name==version" >> requirements.txt
git add requirements.txt
git commit -m "Add missing dependency"
git push origin main
```

### Issue: "FileNotFoundError" for CSV or Model

**Cause**: Files not in repository

**Solution**:
1. Ensure all data files are committed to Git
2. Check file paths are relative (not absolute)

```bash
# Check if files are tracked
git status

# Add files
git add emp_attrition.csv best_model.pkl preprocessor.pkl
git commit -m "Add data and model files"
git push origin main
```

### Issue: App Crashes on Load

**Cause**: Large file or memory issue

**Solution**:
1. Check logs in app dashboard
2. Optimize data loading with caching:

```python
@st.cache_resource
def load_data():
    return pd.read_csv('emp_attrition.csv')

@st.cache_resource
def load_model():
    return joblib.load('best_model.pkl')
```

### Issue: Slow App Performance

**Cause**: Inefficient data processing

**Solution**:
1. Add caching decorators
2. Reduce dataset size for analysis
3. Optimize preprocessing

```python
@st.cache_data
def expensive_computation(data):
    # Your computation here
    return result
```

---

## Performance Optimization

### 1. Use Caching

```python
import streamlit as st
import pandas as pd

@st.cache_resource
def load_model():
    """Load model once, reuse across sessions"""
    return joblib.load('best_model.pkl')

@st.cache_data
def load_data():
    """Cache data loading"""
    return pd.read_csv('emp_attrition.csv')
```

### 2. Lazy Load Visualizations

```python
if st.checkbox("Show detailed analysis"):
    # Only load if user requests
    st.plotly_chart(fig)
```

### 3. Optimize File Sizes

- Compress CSV files
- Use Parquet format for large datasets
- Store large models separately

### 4. Reduce Initial Load

```python
# Load only necessary data initially
df = pd.read_csv('emp_attrition.csv', nrows=100)
```

---

## Security Best Practices

### 1. Use Secrets for Sensitive Data

```python
# DON'T do this
password = "my-secret-password"

# DO this
password = st.secrets["database"]["password"]
```

### 2. Validate User Input

```python
import streamlit as st

age = st.number_input("Age", min_value=18, max_value=65)
if age < 18:
    st.error("Age must be 18 or older")
```

### 3. Limit File Uploads

```python
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
if uploaded_file.size > 10 * 1024 * 1024:  # 10 MB limit
    st.error("File too large")
```

### 4. Add Authentication (Optional)

```python
import streamlit as st

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    password = st.text_input("Password", type="password")
    if password == "your-password":
        st.session_state.password_correct = True
        return True
    return False

if not check_password():
    st.stop()

# Your app code here
st.write("Welcome!")
```

---

## Advanced Configuration

### Custom Favicon

Add to `.streamlit/config.toml`:

```toml
[client]
showErrorDetails = true
favicon = "🎯"
```

### Custom Page Title

In `app.py`:

```python
st.set_page_config(
    page_title="Employee Attrition Prediction",
    page_icon="👥",
    layout="wide"
)
```

### Multi-Page Apps

Create `pages/` directory:

```
app.py
pages/
  ├── 1_Data_Analysis.py
  ├── 2_Predictions.py
  └── 3_Model_Info.py
```

---

## Monitoring and Analytics

### 1. Check App Metrics

- Go to app dashboard
- View usage statistics
- Monitor resource consumption

### 2. Set Up Alerts

- Monitor error rates
- Track performance metrics
- Get notifications for issues

### 3. View Logs

```bash
# View deployment logs
streamlit logs
```

---

## Scaling Your App

### When to Scale

- App gets slow with many users
- Need more resources
- Want higher availability

### Scaling Options

1. **Streamlit Community Cloud**
   - Limited to free tier
   - Upgrade to premium for more resources

2. **Docker + Cloud Platform**
   - More control
   - Better scalability
   - See Docker deployment guide

3. **Load Balancing**
   - Multiple instances
   - Distribute traffic
   - Advanced setup

---

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Model Retraining

```bash
# Retrain model locally
python analysis_notebook.py

# Update model file
git add best_model.pkl
git commit -m "Update trained model"
git push origin main
```

### Backup Your App

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/employee-attrition.git backup/

# Or backup locally
cp -r /home/ubuntu/attrition_project ~/attrition_backup/
```

---

## Useful Links

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud/
- **GitHub**: https://github.com/
- **Streamlit Community**: https://discuss.streamlit.io/

---

## Quick Reference

| Task | Command |
|------|---------|
| Initialize Git | `git init` |
| Add files | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push origin main` |
| Check status | `git status` |
| View logs | `git log` |

---

## Support

- **Streamlit Issues**: https://github.com/streamlit/streamlit/issues
- **Community Forum**: https://discuss.streamlit.io/
- **Stack Overflow**: Tag with `streamlit`

---

**Last Updated**: April 26, 2026

**Deployment Time**: ~2-5 minutes

**Cost**: Free (Community Cloud)
