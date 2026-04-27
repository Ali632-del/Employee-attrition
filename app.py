import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Employee Attrition Prediction",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .section-header {
        color: #1f77b4;
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA AND MODELS
# ============================================================================
@st.cache_resource
def load_data_and_models():
    """Load dataset, trained model, and preprocessor"""
    df = pd.read_csv('emp_attrition.csv')
    model = joblib.load('best_model.pkl')
    preprocessor = joblib.load('preprocessor.pkl')
    return df, model, preprocessor

df, model, preprocessor = load_data_and_models()

# Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.markdown("# 📊 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["🏠 Home", "📈 Data Overview", "🔍 Data Analysis", "🎯 Predictions", "📋 Model Info"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This application helps predict employee attrition using machine learning. "
    "Explore the data, understand key drivers, and make predictions for individual employees."
)

# ============================================================================
# PAGE: HOME
# ============================================================================
if page == "🏠 Home":
    st.markdown('<div class="header-title">👥 Employee Attrition Prediction System</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Employees",
            value=f"{len(df):,}",
            delta="Dataset Size"
        )
    
    with col2:
        attrition_rate = (df['attrition'] == 'Yes').sum() / len(df) * 100
        st.metric(
            label="Attrition Rate",
            value=f"{attrition_rate:.2f}%",
            delta=f"{(df['attrition'] == 'Yes').sum()} employees left"
        )
    
    with col3:
        st.metric(
            label="Model ROC-AUC",
            value="0.8005",
            delta="Gradient Boosting"
        )
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">📌 Project Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Objective
        This project aims to:
        - **Identify** key factors driving employee attrition
        - **Predict** which employees are at risk of leaving
        - **Enable** proactive retention strategies
        
        ### 📊 Dataset
        - **1,470** employees analyzed
        - **35** features including demographics, job details, and satisfaction metrics
        - **16.12%** attrition rate
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 Machine Learning Model
        - **Algorithm**: Gradient Boosting Classifier
        - **ROC-AUC Score**: 0.8005
        - **Accuracy**: 86.73%
        - **F1-Score**: 0.4658
        
        ### 🔑 Top Attrition Drivers
        1. Overtime Status
        2. Stock Option Level
        3. Job Level
        4. Job Role (Lab Technician)
        5. Years with Current Manager
        """)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">🚀 Getting Started</div>', unsafe_allow_html=True)
    
    st.markdown("""
    1. **📈 Data Overview** - Explore the dataset structure and basic statistics
    2. **🔍 Data Analysis** - Visualize patterns and relationships in the data
    3. **🎯 Predictions** - Make predictions for individual employees
    4. **📋 Model Info** - Understand model performance and feature importance
    """)

# ============================================================================
# PAGE: DATA OVERVIEW
# ============================================================================
elif page == "📈 Data Overview":
    st.markdown('<div class="section-header">📈 Dataset Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Total Features", df.shape[1])
    with col3:
        st.metric("Attrition (Yes)", (df['attrition'] == 'Yes').sum())
    with col4:
        st.metric("Retention (No)", (df['attrition'] == 'No').sum())
    
    st.markdown("---")
    
    # Data Preview
    st.markdown("### 📋 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Data Info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Data Types")
        dtype_info = pd.DataFrame({
            'Type': df.dtypes.value_counts().index,
            'Count': df.dtypes.value_counts().values
        })
        st.dataframe(dtype_info, use_container_width=True)
    
    with col2:
        st.markdown("### 🔢 Numerical Features Statistics")
        st.dataframe(df.describe().T[['count', 'mean', 'std', 'min', 'max']], use_container_width=True)
    
    # Missing Values
    st.markdown("### ⚠️ Data Quality")
    missing_data = df.isnull().sum()
    if missing_data.sum() == 0:
        st.success("✓ No missing values detected in the dataset")
    else:
        st.dataframe(missing_data[missing_data > 0], use_container_width=True)
    
    # Categorical Features
    st.markdown("### 🏷️ Categorical Features")
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    col1, col2 = st.columns(2)
    for idx, col in enumerate(categorical_cols):
        if idx % 2 == 0:
            with col1:
                st.write(f"**{col}**")
                st.write(df[col].value_counts())
        else:
            with col2:
                st.write(f"**{col}**")
                st.write(df[col].value_counts())

# ============================================================================
# PAGE: DATA ANALYSIS
# ============================================================================
elif page == "🔍 Data Analysis":
    st.markdown('<div class="section-header">🔍 Exploratory Data Analysis</div>', unsafe_allow_html=True)
    
    # Attrition Distribution
    st.markdown("### 📊 Attrition Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        attrition_counts = df['attrition'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=attrition_counts.index,
            values=attrition_counts.values,
            hole=0.3,
            marker=dict(colors=['#2ecc71', '#e74c3c'])
        )])
        fig.update_layout(
            title="Attrition Distribution",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Key Insights")
        st.markdown(f"""
        - **Total Employees**: {len(df):,}
        - **Attrition Count**: {(df['attrition'] == 'Yes').sum()}
        - **Retention Count**: {(df['attrition'] == 'No').sum()}
        - **Attrition Rate**: {(df['attrition'] == 'Yes').sum() / len(df) * 100:.2f}%
        
        The dataset shows a **16.12% attrition rate**, indicating that 
        approximately 1 in 6 employees leave the company.
        """)
    
    st.markdown("---")
    
    # Attrition by Department
    st.markdown("### 🏢 Attrition by Department")
    dept_attrition = pd.crosstab(df['department'], df['attrition'], normalize='index') * 100
    
    fig = go.Figure()
    for col in dept_attrition.columns:
        fig.add_trace(go.Bar(
            name=col,
            x=dept_attrition.index,
            y=dept_attrition[col],
            marker_color='#2ecc71' if col == 'No' else '#e74c3c'
        ))
    
    fig.update_layout(
        title="Attrition Rate by Department",
        xaxis_title="Department",
        yaxis_title="Percentage (%)",
        barmode='stack',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Attrition by Job Role
    st.markdown("### 💼 Attrition by Job Role")
    role_attrition = pd.crosstab(df['jobrole'], df['attrition'])
    role_attrition['Attrition_Rate'] = role_attrition['Yes'] / (role_attrition['Yes'] + role_attrition['No']) * 100
    role_attrition = role_attrition.sort_values('Attrition_Rate', ascending=False)
    
    fig = px.bar(
        role_attrition.reset_index(),
        x='jobrole',
        y='Attrition_Rate',
        title="Attrition Rate by Job Role",
        labels={'jobrole': 'Job Role', 'Attrition_Rate': 'Attrition Rate (%)'},
        color='Attrition_Rate',
        color_continuous_scale='RdYlGn_r',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Age Distribution
    st.markdown("### 👤 Age Distribution by Attrition Status")
    
    fig = go.Figure()
    for status in ['Yes', 'No']:
        fig.add_trace(go.Histogram(
            x=df[df['attrition'] == status]['age'],
            name=f"Attrition: {status}",
            opacity=0.7,
            nbinsx=20
        ))
    
    fig.update_layout(
        title="Age Distribution by Attrition Status",
        xaxis_title="Age",
        yaxis_title="Count",
        barmode='overlay',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Monthly Income
    st.markdown("### 💰 Monthly Income by Attrition Status")
    
    fig = go.Figure()
    for status in ['Yes', 'No']:
        fig.add_trace(go.Box(
            y=df[df['attrition'] == status]['monthlyincome'],
            name=f"Attrition: {status}",
            boxmean='sd'
        ))
    
    fig.update_layout(
        title="Monthly Income Distribution by Attrition Status",
        yaxis_title="Monthly Income ($)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Job Satisfaction
    st.markdown("### 😊 Job Satisfaction by Attrition Status")
    
    satisfaction_attrition = pd.crosstab(df['jobsatisfaction'], df['attrition'], normalize='index') * 100
    
    fig = go.Figure()
    for col in satisfaction_attrition.columns:
        fig.add_trace(go.Bar(
            name=col,
            x=satisfaction_attrition.index,
            y=satisfaction_attrition[col],
            marker_color='#2ecc71' if col == 'No' else '#e74c3c'
        ))
    
    fig.update_layout(
        title="Attrition Rate by Job Satisfaction Level",
        xaxis_title="Job Satisfaction (1=Low, 4=High)",
        yaxis_title="Percentage (%)",
        barmode='stack',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: PREDICTIONS
# ============================================================================
elif page == "🎯 Predictions":
    st.markdown('<div class="section-header">🎯 Employee Attrition Prediction</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Enter employee details below to predict the likelihood of attrition.
    The model will analyze the information and provide a risk assessment.
    """)
    
    st.markdown("---")
    
    # Create input form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=65, value=30)
        distance_from_home = st.number_input("Distance from Home (km)", min_value=1, max_value=30, value=10)
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=100)
        years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5)
    
    with col2:
        department = st.selectbox("Department", df['department'].unique())
        job_role = st.selectbox("Job Role", df['jobrole'].unique())
        education = st.number_input("Education Level (1-5)", min_value=1, max_value=5, value=3)
        job_satisfaction = st.number_input("Job Satisfaction (1-4)", min_value=1, max_value=4, value=3)
    
    with col3:
        business_travel = st.selectbox("Business Travel", df['businesstravel'].unique())
        overtime = st.selectbox("Overtime", ['Yes', 'No'])
        stock_option_level = st.number_input("Stock Option Level (0-3)", min_value=0, max_value=3, value=1)
        years_with_manager = st.number_input("Years with Current Manager", min_value=0, max_value=40, value=3)
    
    st.markdown("---")
    
    # Additional fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        environment_satisfaction = st.number_input("Environment Satisfaction (1-4)", min_value=1, max_value=4, value=3)
        relationship_satisfaction = st.number_input("Relationship Satisfaction (1-4)", min_value=1, max_value=4, value=3)
        work_life_balance = st.number_input("Work-Life Balance (1-4)", min_value=1, max_value=4, value=3)
    
    with col2:
        job_level = st.number_input("Job Level (1-4)", min_value=1, max_value=4, value=2)
        job_involvement = st.number_input("Job Involvement (1-4)", min_value=1, max_value=4, value=3)
        years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, max_value=15, value=1)
        num_companies_worked = st.number_input("Number of Companies Worked", min_value=1, max_value=9, value=2)
    
    with col3:
        percent_salary_hike = st.number_input("Percent Salary Hike (%)", min_value=11, max_value=25, value=15)
        daily_rate = st.number_input("Daily Rate ($)", min_value=100, max_value=1500, value=800)
        hourly_rate = st.number_input("Hourly Rate ($)", min_value=30, max_value=100, value=65)
    
    st.markdown("---")
    
    # Prediction button
    if st.button("🔮 Predict Attrition Risk", use_container_width=True):
        # Create input dataframe
        input_data = pd.DataFrame({
            'age': [age],
            'attrition': ['No'],  # Placeholder, will be removed
            'businesstravel': [business_travel],
            'dailyrate': [daily_rate],
            'department': [department],
            'distancefromhome': [distance_from_home],
            'education': [education],
            'educationfield': ['Life Sciences'],  # Default
            'employeecount': [1],  # Placeholder
            'employeenumber': [1],  # Placeholder
            'environmentsatisfaction': [environment_satisfaction],
            'gender': ['Male'],  # Default
            'hourlyrate': [hourly_rate],
            'joblevel': [job_level],
            'jobinvolvement': [job_involvement],
            'jobrole': [job_role],
            'jobsatisfaction': [job_satisfaction],
            'maritalstatus': ['Single'],  # Default
            'monthlyincome': [monthly_income],
            'monthlyrate': [1500],  # Placeholder
            'numcompaniesworked': [num_companies_worked],
            'numemployeesreporting': [1],  # Placeholder
            'over18': ['Y'],  # Placeholder
            'overtime': [overtime],
            'percentsalaryhike': [percent_salary_hike],
            'performancerating': [3],  # Default
            'relationshipsatisfaction': [relationship_satisfaction],
            'standardhours': [8],  # Placeholder
            'stockoptionlevel': [stock_option_level],
            'totalworkingyears': [years_at_company],
            'trainingtimeslastyear': [3],  # Default
            'worklifebalance': [work_life_balance],
            'yearsatcompany': [years_at_company],
            'yearsincurrentrole': [years_at_company],
            'yearswithcurrmanager': [years_with_manager],
            'yearssincelastpromotion': [years_since_last_promotion]
        })
        
        # Remove attrition column for preprocessing
        X_input = input_data.drop('attrition', axis=1)

        # ✅ FIX: ensure all expected columns exist
        expected_cols = preprocessor.feature_names_in_

        # add missing columns with default value
        for col in expected_cols:
          if col not in X_input.columns:
            X_input[col] = df[col].mode()[0]

        # keep only expected columns + correct order
        X_input = X_input[expected_cols]

        # Preprocess
        X_input_processed = preprocessor.transform(X_input)
        
        # Predict
        prediction = model.predict(X_input_processed)[0]
        probability = model.predict_proba(X_input_processed)[0]
        
        # Display results
        st.markdown("---")
        st.markdown("### 📊 Prediction Results")
        st.write("Missing columns fixed:", set(expected_cols) - set(input_data.columns))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if prediction == 1:
                st.error("⚠️ HIGH RISK - Employee is likely to leave")
                risk_level = "High"
                attrition_prob = probability[1]
            else:
                st.success("✓ LOW RISK - Employee is likely to stay")
                risk_level = "Low"
                attrition_prob = probability[1]
            
            st.markdown(f"""
            **Risk Level**: {risk_level}
            
            **Attrition Probability**: {attrition_prob*100:.2f}%
            
            **Retention Probability**: {probability[0]*100:.2f}%
            """)
        
        with col2:
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=attrition_prob * 100,
                title={'text': "Attrition Risk (%)"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 33], 'color': "#2ecc71"},
                        {'range': [33, 66], 'color': "#f39c12"},
                        {'range': [66, 100], 'color': "#e74c3c"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 💡 Recommendations")
        
        if prediction == 1:
            st.markdown("""
            Based on the high attrition risk, consider:
            - 🎯 Schedule a career development discussion
            - 💰 Review compensation and benefits package
            - 🤝 Improve work-life balance initiatives
            - 📈 Discuss growth opportunities and career path
            - 👥 Increase manager engagement and support
            """)
        else:
            st.markdown("""
            Employee shows low attrition risk. Continue:
            - 👍 Maintaining current engagement level
            - 📊 Regular performance reviews
            - 🎓 Professional development opportunities
            - 🤝 Strong manager-employee relationship
            """)

# ============================================================================
# PAGE: MODEL INFO
# ============================================================================
elif page == "📋 Model Info":
    st.markdown('<div class="section-header">📋 Model Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🤖 Model Details")
        st.markdown("""
        **Algorithm**: Gradient Boosting Classifier
        
        **Training Data**: 1,176 employees (80%)
        
        **Test Data**: 294 employees (20%)
        
        **Features**: 47 (after preprocessing)
        
        **Class Balance**: SMOTE applied
        """)
    
    with col2:
        st.markdown("### 📊 Performance Metrics")
        st.markdown("""
        **Accuracy**: 86.73%
        
        **ROC-AUC Score**: 0.8005
        
        **F1-Score**: 0.4658
        
        **Precision**: 0.65
        
        **Recall**: 0.36
        """)
    
    st.markdown("---")
    
    st.markdown("### 🔑 Top 15 Feature Importance")
    
    feature_importance_data = {
        'Feature': [
            'Overtime',
            'Stock Option Level',
            'Job Level',
            'Job Role (Lab Technician)',
            'Years with Current Manager',
            'Business Travel (Frequently)',
            'Marital Status (Single)',
            'Age',
            'Job Satisfaction',
            'Department (R&D)',
            'Environment Satisfaction',
            'Work-Life Balance',
            'Number of Companies Worked',
            'Relationship Satisfaction',
            'Education Field (Life Sciences)'
        ],
        'Importance': [
            0.2598, 0.1066, 0.0680, 0.0574, 0.0539,
            0.0536, 0.0434, 0.0376, 0.0289, 0.0257,
            0.0257, 0.0243, 0.0186, 0.0160, 0.0143
        ]
    }
    
    fig = px.bar(
        feature_importance_data,
        x='Importance',
        y='Feature',
        orientation='h',
        title="Feature Importance in Predicting Attrition",
        labels={'Importance': 'Importance Score', 'Feature': 'Feature'},
        color='Importance',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 📈 Model Comparison")
    
    comparison_data = {
        'Model': ['Logistic Regression', 'Random Forest', 'Gradient Boosting'],
        'Accuracy': [0.7823, 0.8469, 0.8673],
        'F1-Score': [0.4921, 0.2623, 0.4658],
        'ROC-AUC': [0.7860, 0.7883, 0.8005]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    st.markdown("""
    **Why Gradient Boosting?**
    
    Gradient Boosting was selected as the best model because:
    - ✓ Highest ROC-AUC score (0.8005)
    - ✓ Best balance between precision and recall
    - ✓ Handles class imbalance well
    - ✓ Provides strong feature importance insights
    - ✓ Robust to outliers and non-linear relationships
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔄 Data Preprocessing Pipeline")
    
    st.markdown("""
    1. **Data Cleaning**
       - Removed duplicate rows
       - Standardized column names to lowercase with underscores
       - Validated data types
    
    2. **Feature Encoding**
       - Categorical features: One-Hot Encoding
       - Numerical features: StandardScaler normalization
    
    3. **Class Imbalance Handling**
       - Applied SMOTE (Synthetic Minority Over-sampling Technique)
       - Balanced training data from 1,176 to 1,972 samples
    
    4. **Train-Test Split**
       - 80% training data (1,176 samples)
       - 20% test data (294 samples)
       - Stratified split to maintain class distribution
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>Employee Attrition Prediction System | Built with Streamlit | Last Updated: 2026</p>
</div>
""", unsafe_allow_html=True)


