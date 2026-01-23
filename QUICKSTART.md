# Quick Start Guide - Fraud Management System

## 🚀 Getting Started in 5 Minutes

### Step 1: Setup
```bash
cd aml_compliance_system
python setup.py
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the System
```bash
python main.py
```

## 📝 Common Tasks

### Load Custom Data
```python
from src.aml_system import AMLComplianceSystem

aml = AMLComplianceSystem()
aml.load_data('path/to/your/data.csv')
```

### Run Analysis
```python
results = aml.run_complete_analysis()
```

### Predict Risk for New Transaction
```python
transaction = {
    'Time': '14:30:00',
    'Date': '2024-06-15',
    'Sender_account': 'ACC0001',
    'Receiver_account': 'ACC0002',
    'Amount': 9500,
    'Payment_currency': 'USD',
    'Received_currency': 'USD',
    'Sender_bank_location': 'US-NY',
    'Receiver_bank_location': 'AE-DXB',
    'Payment_type': 'Wire'
}

risk = aml.predict_compliance_risk(transaction)
print(risk)
```

### Get Customer Profile
```python
profile = aml.get_customer_risk_profile('ACC0001')
print(profile)
```

### Generate Summary
```python
summary = aml.generate_summary_report()
print(summary)
```

## 🎯 Module-Specific Usage

### Data Manager Only
```python
from src.modules.data_manager import DataManager

dm = DataManager()
df = dm.load_data('data.csv')
```

### Customer Profiler Only
```python
from src.modules.customer_profiler import CustomerProfiler

profiler = CustomerProfiler(df)
profiles = profiler.analyze_customers()
```

### Anomaly Detector Only
```python
from src.modules.anomaly_detector import AnomalyDetector

detector = AnomalyDetector(df)
anomalies = detector.detect_anomalies()
```

### ML Predictor Only
```python
from src.modules.ml_predictor import MLPredictor

predictor = MLPredictor(df)
model = predictor.train_compliance_model()
```

### Visualizer Only
```python
from src.modules.visualizer import AMLVisualizer

viz = AMLVisualizer(df)
viz.create_comprehensive_dashboard(profiles, anomalies)
```

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
# Risk Thresholds
HIGH_RISK_THRESHOLD = 70
MEDIUM_RISK_THRESHOLD = 40

# High-risk Locations
HIGH_RISK_LOCATIONS = ['AE-DXB', 'HK-HKG']

# Model Settings
TEST_SIZE = 0.3
CONTAMINATION_RATE = 0.1
```

## 📊 Output Files

After running the analysis:

- `output/customer_profiles.csv` - Customer risk profiles
- `output/detected_anomalies.csv` - Detected anomalies
- `output/dashboard.png` - Main dashboard
- `output/detailed_analysis.png` - Detailed charts
- `output/customer_profiles.png` - Customer visualizations

## 🐛 Troubleshooting

### Import Errors
```bash
# Make sure you're in the project root directory
cd aml_compliance_system

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%\src          # Windows
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Module Not Found
```bash
# Run from project root, not from src/
cd aml_compliance_system
python main.py
```

## 💡 Tips

1. **Synthetic Data**: If no data file is provided, the system automatically generates synthetic data
2. **Parallel Execution**: Modules can be used independently for faster prototyping
3. **Custom Models**: Extend MLPredictor class to add your own ML models
4. **Batch Processing**: Process multiple transactions at once using pandas DataFrames

## 📚 Learn More

- Full documentation: `README.md`
- Module documentation: Check docstrings in each module
- Configuration options: `src/config.py`
- Tests: `tests/test_system.py`

## 🤝 Need Help?

1. Check the README.md file
2. Review module docstrings
3. Run tests to verify setup: `python -m pytest tests/`
4. Open an issue for bugs or questions

---

**Happy Analyzing! 🎉**
