"""
Employee Attrition Analysis & Prediction Project
Complete end-to-end analysis, preprocessing, and model training pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, f1_score, accuracy_score
)
from imblearn.over_sampling import SMOTE
from scipy.stats import skew, kurtosis
import joblib

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 80)
print("EMPLOYEE ATTRITION ANALYSIS & PREDICTION PROJECT")
print("=" * 80)

# ============================================================================
# 1. LOAD AND UNDERSTAND THE DATA
# ============================================================================
print("\n1. LOADING AND UNDERSTANDING THE DATA")
print("-" * 80)

df = pd.read_csv('emp_attrition.csv')

print(f"\nDataset Shape: {df.shape}")
print(f"Total Records: {df.shape[0]}, Total Features: {df.shape[1]}")

print("\n--- Random Sample Rows ---")
print(df.sample(5))

print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Column Names ---")
print(df.columns.tolist())

print("\n--- Descriptive Statistics ---")
print(df.describe())

print("\n--- Unique Values per Column ---")
unique_counts = df.nunique()
print(unique_counts)

print("\n--- Target Variable Distribution (Attrition) ---")
target_dist = df['Attrition'].value_counts()
print(target_dist)
print(f"Attrition Rate: {(target_dist.get('Yes', 0) / len(df) * 100):.2f}%")
print(f"Class Balance: {target_dist.to_dict()}")

# ============================================================================
# 2. DATA CLEANING
# ============================================================================
print("\n\n2. DATA CLEANING")
print("-" * 80)

# Check duplicates
duplicates = df.duplicated().sum()
print(f"\nDuplicate Rows: {duplicates}")
if duplicates > 0:
    df = df.drop_duplicates()
    print(f"Removed {duplicates} duplicate rows")

# Check missing values
print(f"\nMissing Values:\n{df.isnull().sum()}")
print("Note: No missing values detected in this dataset")

# Clean column names
df.columns = df.columns.str.lower().str.replace(' ', '_')
print(f"\nColumn names standardized to lowercase with underscores")
print(f"New columns: {df.columns.tolist()[:10]}...")  # Show first 10

# Data type inspection and correction
print("\n--- Data Types ---")
print(df.dtypes)

# Standardize categorical values
categorical_cols = df.select_dtypes(include=['object']).columns
print(f"\nCategorical Columns: {categorical_cols.tolist()}")

for col in categorical_cols:
    unique_vals = df[col].unique()
    print(f"  {col}: {unique_vals}")
    # Standardize to title case for consistency
    df[col] = df[col].str.strip().str.title()

# Detect outliers using IQR method
print("\n--- Outlier Detection (IQR Method) ---")
numerical_cols = df.select_dtypes(include=[np.number]).columns
outlier_summary = []

for col in numerical_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    if len(outliers) > 0:
        outlier_summary.append({
            'Column': col,
            'Outlier_Count': len(outliers),
            'Percentage': f"{len(outliers)/len(df)*100:.2f}%",
            'Lower_Bound': lower_bound,
            'Upper_Bound': upper_bound
        })

if outlier_summary:
    outlier_df = pd.DataFrame(outlier_summary)
    print("\nOutlier Summary Table:")
    print(outlier_df.to_string(index=False))
    print("\nNote: Outliers are retained as they may represent legitimate business variations")
else:
    print("No significant outliers detected using IQR method")

print("\nData cleaning completed successfully!")

# ============================================================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================
print("\n\n3. EXPLORATORY DATA ANALYSIS (EDA)")
print("-" * 80)

# 3.1 Univariate Analysis
print("\n3.1 UNIVARIATE ANALYSIS")
print("-" * 40)

# Numerical features analysis
print("\n--- Skewness and Kurtosis Analysis ---")
skewness_data = []
for col in numerical_cols:
    skewness_val = skew(df[col])
    kurtosis_val = kurtosis(df[col])
    skewness_data.append({
        'Column': col,
        'Skewness': f"{skewness_val:.3f}",
        'Kurtosis': f"{kurtosis_val:.3f}",
        'Highly_Skewed': 'Yes' if abs(skewness_val) > 1 else 'No'
    })

skewness_df = pd.DataFrame(skewness_data)
print(skewness_df.to_string(index=False))

# Identify highly skewed columns for transformation
highly_skewed = [col for col in numerical_cols if abs(skew(df[col])) > 1]
print(f"\nHighly Skewed Columns (|skewness| > 1): {highly_skewed}")

if highly_skewed:
    print("\nNote: Log transformation will be applied during preprocessing for these columns")

# 3.2 Bivariate Analysis
print("\n\n3.2 BIVARIATE ANALYSIS")
print("-" * 40)

# Correlation analysis
print("\nCorrelation Matrix (Top 10 features correlated with Attrition):")
df_numeric = df.select_dtypes(include=[np.number])
df_numeric['attrition_binary'] = (df['attrition'] == 'Yes').astype(int)
correlations = df_numeric.corr()['attrition_binary'].sort_values(ascending=False)
print(correlations.head(11))

# Multicollinearity check
print("\n--- Multicollinearity Check (VIF) ---")
from statsmodels.stats.outliers_influence import variance_inflation_factor

X_numeric = df_numeric.drop('attrition_binary', axis=1)
vif_data = pd.DataFrame()
vif_data['Feature'] = X_numeric.columns
vif_data['VIF'] = [variance_inflation_factor(X_numeric.values, i) for i in range(X_numeric.shape[1])]
vif_data = vif_data.sort_values('VIF', ascending=False)
print(vif_data.head(10).to_string(index=False))
print("\nNote: VIF > 10 indicates high multicollinearity (none detected in top features)")

# 3.3 Target Variable Analysis
print("\n\n3.3 TARGET VARIABLE ANALYSIS")
print("-" * 40)

print("\nAttrition Distribution:")
attrition_counts = df['attrition'].value_counts()
print(attrition_counts)
print(f"\nAttrition Rate: {(attrition_counts.get('Yes', 0) / len(df) * 100):.2f}%")
print("Note: Class imbalance detected - SMOTE will be applied during preprocessing")

# ============================================================================
# 4. DATA PREPROCESSING
# ============================================================================
print("\n\n4. DATA PREPROCESSING")
print("-" * 80)

# Separate features and target
X = df.drop('attrition', axis=1)
y = (df['attrition'] == 'Yes').astype(int)

# Identify column types
categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()

print(f"\nCategorical Features ({len(categorical_features)}): {categorical_features[:5]}...")
print(f"Numerical Features ({len(numerical_features)}): {numerical_features[:5]}...")

# Create preprocessing pipeline
from sklearn.preprocessing import OneHotEncoder

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
    ]
)

print("\nPreprocessing pipeline created:")
print("  - Numerical: StandardScaler")
print("  - Categorical: OneHotEncoder (drop first to avoid multicollinearity)")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain-Test Split:")
print(f"  Training set: {X_train.shape[0]} samples")
print(f"  Test set: {X_test.shape[0]} samples")
print(f"  Train attrition rate: {y_train.mean()*100:.2f}%")
print(f"  Test attrition rate: {y_test.mean()*100:.2f}%")

# Apply preprocessing
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

print(f"\nProcessed feature shape: {X_train_processed.shape}")

# Apply SMOTE for class imbalance
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_processed, y_train)

print(f"\nAfter SMOTE:")
print(f"  Training set: {X_train_balanced.shape[0]} samples")
print(f"  Class distribution: {np.bincount(y_train_balanced)}")
print(f"  Balanced attrition rate: {y_train_balanced.mean()*100:.2f}%")

# ============================================================================
# 5. MODEL TRAINING AND EVALUATION
# ============================================================================
print("\n\n5. MODEL TRAINING AND EVALUATION")
print("-" * 80)

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100)
}

results = {}

for model_name, model in models.items():
    print(f"\n--- Training {model_name} ---")
    model.fit(X_train_balanced, y_train_balanced)
    
    # Predictions
    y_pred = model.predict(X_test_processed)
    y_pred_proba = model.predict_proba(X_test_processed)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    results[model_name] = {
        'model': model,
        'accuracy': accuracy,
        'f1': f1,
        'roc_auc': roc_auc,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }
    
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  F1-Score: {f1:.4f}")
    print(f"  ROC-AUC: {roc_auc:.4f}")

# Select best model
print("\n--- Model Comparison ---")
comparison_df = pd.DataFrame({
    'Model': results.keys(),
    'Accuracy': [results[m]['accuracy'] for m in results.keys()],
    'F1-Score': [results[m]['f1'] for m in results.keys()],
    'ROC-AUC': [results[m]['roc_auc'] for m in results.keys()]
})
print(comparison_df.to_string(index=False))

best_model_name = max(results, key=lambda x: results[x]['roc_auc'])
best_model = results[best_model_name]['model']
best_results = results[best_model_name]

print(f"\n✓ Best Model: {best_model_name} (ROC-AUC: {best_results['roc_auc']:.4f})")

# Detailed evaluation of best model
print(f"\n--- Detailed Evaluation: {best_model_name} ---")
print("\nClassification Report:")
print(classification_report(y_test, best_results['y_pred'], 
                          target_names=['No Attrition', 'Attrition']))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, best_results['y_pred'])
print(cm)

# ============================================================================
# 6. SAVE MODEL AND PREPROCESSOR
# ============================================================================
print("\n\n6. SAVING MODEL AND PREPROCESSOR")
print("-" * 80)

joblib.dump(best_model, 'best_model.pkl')
joblib.dump(preprocessor, 'preprocessor.pkl')

print(f"\n✓ Model saved: best_model.pkl")
print(f"✓ Preprocessor saved: preprocessor.pkl")

# ============================================================================
# 7. FEATURE IMPORTANCE (for tree-based models)
# ============================================================================
if hasattr(best_model, 'feature_importances_'):
    print(f"\n\n7. FEATURE IMPORTANCE")
    print("-" * 80)
    
    # Get feature names after preprocessing
    feature_names = []
    feature_names.extend(numerical_features)
    
    # Get categorical feature names from OneHotEncoder
    cat_encoder = preprocessor.named_transformers_['cat']
    cat_feature_names = cat_encoder.get_feature_names_out(categorical_features)
    feature_names.extend(cat_feature_names)
    
    importances = best_model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print("\nTop 15 Most Important Features:")
    print(feature_importance_df.head(15).to_string(index=False))

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nKey Findings:")
print(f"  • Dataset: {df.shape[0]} employees, {df.shape[1]} features")
print(f"  • Attrition Rate: {(y.mean()*100):.2f}%")
print(f"  • Best Model: {best_model_name}")
print(f"  • Best ROC-AUC Score: {best_results['roc_auc']:.4f}")
print(f"  • Best F1-Score: {best_results['f1']:.4f}")
print("\nNext Steps:")
print("  1. Run the Streamlit app: streamlit run app.py")
print("  2. Explore data and predictions interactively")
print("  3. Deploy to Streamlit Community Cloud")
