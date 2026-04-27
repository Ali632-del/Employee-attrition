# Employee Attrition Prediction System

A complete end-to-end machine learning project for predicting employee attrition with an interactive Streamlit web application.

## 📋 Project Overview

This project analyzes employee data to identify key factors driving attrition and builds a predictive model to assess the risk of individual employees leaving the organization. The system provides:

- **Comprehensive Data Analysis**: Exploratory data analysis with visualizations
- **Machine Learning Pipeline**: Data preprocessing, model training, and hyperparameter tuning
- **Interactive Web App**: User-friendly Streamlit application for predictions and insights
- **Production-Ready**: Deployable to Streamlit Community Cloud

## 📊 Dataset

- **Source**: IBM HR Analytics Employee Attrition Dataset
- **Records**: 1,470 employees
- **Features**: 35 attributes (demographics, job details, satisfaction metrics)
- **Target**: Attrition (Yes/No)
- **Attrition Rate**: 16.12%

## 🎯 Key Findings

### Top Attrition Drivers
1. **Overtime Status** - Employees working overtime have significantly higher attrition
2. **Stock Option Level** - Lower stock options correlate with higher attrition
3. **Job Level** - Entry-level positions show higher turnover
4. **Job Role** - Laboratory Technicians have the highest attrition rate
5. **Years with Manager** - Shorter tenure with current manager increases risk

### Model Performance
- **Algorithm**: Gradient Boosting Classifier
- **ROC-AUC Score**: 0.8005
- **Accuracy**: 86.73%
- **F1-Score**: 0.4658
- **Precision**: 0.65
- **Recall**: 0.36

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd employee_attrition_project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

### Local Development
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Features
- **Home**: Project overview and key metrics
- **Data Overview**: Dataset structure and statistics
- **Data Analysis**: Interactive visualizations and insights
- **Predictions**: Make predictions for individual employees
- **Model Info**: Model performance and feature importance

## 📁 Project Structure

```
employee_attrition_project/
├── app.py                      # Main Streamlit application
├── analysis_notebook.py        # Complete analysis and model training
├── best_model.pkl             # Trained Gradient Boosting model
├── preprocessor.pkl           # Data preprocessing pipeline
├── emp_attrition.csv          # Dataset
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .streamlit/
    └── config.toml           # Streamlit configuration
```

## 📊 Analysis Summary

### Data Cleaning
- Removed duplicate rows (0 found)
- Standardized column names to lowercase with underscores
- Validated data types
- Detected and documented outliers using IQR method
- No missing values found

### Exploratory Data Analysis
- **Univariate Analysis**: Distribution analysis, skewness, kurtosis
- **Bivariate Analysis**: Correlation heatmaps, scatter plots, boxplots
- **Multivariate Analysis**: VIF analysis for multicollinearity

### Preprocessing Pipeline
1. **Feature Encoding**
   - Categorical: One-Hot Encoding
   - Numerical: StandardScaler normalization

2. **Class Imbalance Handling**
   - Applied SMOTE (Synthetic Minority Over-sampling Technique)
   - Balanced training data from 1,176 to 1,972 samples

3. **Train-Test Split**
   - 80% training (1,176 samples)
   - 20% testing (294 samples)
   - Stratified split to maintain class distribution

### Model Training
Three models were trained and compared:
- Logistic Regression (ROC-AUC: 0.7860)
- Random Forest (ROC-AUC: 0.7883)
- **Gradient Boosting (ROC-AUC: 0.8005)** ✓ Best Model

## 🔮 Making Predictions

The app allows you to input employee details and get attrition risk predictions:

### Input Features
- Demographics: Age, Gender, Marital Status
- Job Details: Department, Role, Level, Years at Company
- Compensation: Monthly Income, Salary Hike, Stock Options
- Satisfaction: Job, Environment, Relationship, Work-Life Balance
- Work Patterns: Overtime, Business Travel, Distance from Home

### Output
- **Risk Level**: High/Low
- **Attrition Probability**: Percentage chance of leaving
- **Retention Probability**: Percentage chance of staying
- **Recommendations**: Actionable insights for retention

## 🌐 Deployment to Streamlit Community Cloud

### Prerequisites
- GitHub account
- Streamlit Community Cloud account

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/employee-attrition.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and main file (`app.py`)
   - Click "Deploy"

3. **Configure Secrets (if needed)**
   - Add any API keys or sensitive data in the Secrets section

## 📈 Model Interpretation

### Feature Importance
The model identifies the following as most important for predicting attrition:
1. Overtime (25.98%) - Strong indicator of burnout
2. Stock Option Level (10.66%) - Financial incentive
3. Job Level (6.80%) - Career progression
4. Job Role (5.74%) - Role-specific factors
5. Years with Manager (5.39%) - Relationship stability

### Model Assumptions
- Linear relationships between features and target
- No temporal dependencies
- Historical patterns continue into the future
- Data is representative of the employee population

## 🔧 Customization

### Adding New Features
1. Update the input form in `app.py`
2. Retrain the model with new features
3. Update `best_model.pkl` and `preprocessor.pkl`

### Changing the Model
1. Modify the model in `analysis_notebook.py`
2. Retrain and save the new model
3. Update `best_model.pkl`

### Styling
- Modify CSS in the `st.markdown()` sections of `app.py`
- Update color schemes and fonts as needed

## 📝 Files Description

### app.py
Main Streamlit application with:
- Data loading and caching
- Interactive visualizations
- Prediction interface
- Model information dashboard

### analysis_notebook.py
Complete analysis pipeline including:
- Data loading and exploration
- Data cleaning and validation
- EDA with visualizations
- Preprocessing and feature engineering
- Model training and evaluation
- Model persistence

### best_model.pkl
Trained Gradient Boosting Classifier saved with joblib

### preprocessor.pkl
ColumnTransformer pipeline for data preprocessing

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Install missing packages
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError" for CSV or model files
**Solution**: Ensure all files are in the same directory as `app.py`

### Issue: Slow predictions
**Solution**: 
- Reduce dataset size for analysis
- Use a more powerful machine
- Optimize model hyperparameters

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web application framework |
| pandas | 2.0.3 | Data manipulation |
| numpy | 1.24.3 | Numerical computing |
| scikit-learn | 1.3.0 | Machine learning |
| imbalanced-learn | 0.11.0 | SMOTE for class imbalance |
| matplotlib | 3.7.2 | Static visualizations |
| seaborn | 0.12.2 | Statistical visualizations |
| plotly | 5.16.1 | Interactive visualizations |
| joblib | 1.3.1 | Model serialization |
| statsmodels | 0.14.0 | Statistical analysis |

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Plotly Documentation](https://plotly.com/python/)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Consult the documentation links above

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- Dataset: IBM HR Analytics Employee Attrition Dataset
- Built with: Streamlit, Scikit-learn, Pandas, Plotly
- Inspired by: Real-world HR analytics challenges

## 🔄 Version History

### Version 1.0 (2026)
- Initial release
- Gradient Boosting model
- Interactive Streamlit app
- Comprehensive EDA and analysis

---

**Last Updated**: April 26, 2026

**Project Status**: ✓ Production Ready

For deployment and production use, ensure all dependencies are installed and the model files are present in the project directory.
