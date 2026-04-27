#!/bin/bash

# Employee Attrition Prediction - Setup Script

echo "=========================================="
echo "Employee Attrition Prediction System"
echo "Setup Script"
echo "=========================================="

# Check Python version
echo -e "\n✓ Checking Python version..."
python3 --version

# Create virtual environment
echo -e "\n✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "\n✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "\n=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo -e "\nTo run the application:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run the Streamlit app:"
echo "     streamlit run app.py"
echo -e "\nThe app will open at: http://localhost:8501"
