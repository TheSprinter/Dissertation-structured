# Fraud Management System

A comprehensive fraud detection and management system using AI/ML techniques for fraud detection, risk assessment, and compliance monitoring.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Output](#output)
- [Configuration](#configuration)

## ✨ Features

- **Customer Risk Profiling**: Comprehensive risk assessment based on transaction patterns
- **Anomaly Detection**: Multi-algorithm approach using Isolation Forest and statistical methods
- **Machine Learning**: Predictive models for compliance risk forecasting
- **Visualization**: Interactive dashboards and comprehensive reports
- **Real-time Prediction**: Risk assessment for new transactions

## 📁 Project Structure

```
aml_compliance_system/
│
├── main.py                      # Main execution script
├── requirements.txt             # Python dependencies
├── README.md                   # This file
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── aml_system.py          # Main system orchestrator
│   │
│   └── modules/               # Core modules
│       ├── __init__.py
│       ├── data_manager.py    # Data loading and generation
│       ├── customer_profiler.py   # Customer risk profiling
│       ├── anomaly_detector.py    # Anomaly detection
│       ├── ml_predictor.py    # ML model training and prediction
│       └── visualizer.py      # Visualization and reporting
│
├── data/                      # Data directory (place your CSV files here)
├── output/                    # Generated outputs
│   ├── customer_profiles.csv
│   ├── detected_anomalies.csv
│   ├── dashboard.png
│   ├── detailed_analysis.png
│   └── customer_profiles.png
│
└── tests/                     # Unit tests (to be implemented)
```

## 🚀 Installation

1. **Clone or download the project**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Basic Usage

Run the complete analysis:
```bash
python main.py
```

### Custom Usage

```python
from src.aml_system import AMLComplianceSystem

# Initialize system
aml_system = AMLComplianceSystem()

# Load data
aml_system.load_data('path/to/your/data.csv')

# Run analysis
results = aml_system.run_complete_analysis()

# Predict risk for new transaction
new_txn = {
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

risk = aml_system.predict_compliance_risk(new_txn)
print(risk)
```

## 🧩 Modules

### 1. Data Manager (`data_manager.py`)
- Loads transaction data from CSV files or Google Drive
- Generates synthetic data for testing
- Validates data integrity

### 2. Customer Profiler (`customer_profiler.py`)
- Analyzes customer transaction patterns
- Calculates risk scores (0-100)
- Classifies customers as HIGH, MEDIUM, or LOW risk
- Identifies suspicious behaviors

### 3. Anomaly Detector (`anomaly_detector.py`)
- Uses Isolation Forest algorithm
- Applies statistical Z-score analysis
- Detects unusual transaction patterns
- Identifies time-based anomalies

### 4. ML Predictor (`ml_predictor.py`)
- Trains Random Forest and Gradient Boosting models
- Feature engineering (20+ features)
- Cross-validation for model selection
- Risk probability prediction

### 5. Visualizer (`visualizer.py`)
- Comprehensive dashboard generation
- Customer profile visualizations
- Risk distribution charts
- Compliance reports

## 📊 Output

The system generates several outputs in the `output/` directory:

1. **customer_profiles.csv**: Detailed risk profiles for all customers
2. **detected_anomalies.csv**: List of detected anomalous transactions
3. **dashboard.png**: Main visualization dashboard
4. **detailed_analysis.png**: Additional analysis charts
5. **customer_profiles.png**: Customer-specific visualizations

## ⚙️ Configuration

Edit `src/config.py` to customize:

- Risk thresholds
- High-risk locations
- Model parameters
- Output settings
- Visualization preferences

## 📝 Data Format

Expected CSV format:
```csv
Time,Date,Sender_account,Receiver_account,Amount,Payment_currency,Received_currency,Sender_bank_location,Receiver_bank_location,Payment_type,Is_laundering,Laundering_type
14:30:00,2024-01-15,ACC0001,ACC0002,5000,USD,USD,US-NY,US-NY,Wire,0,None
```

## 🔧 Key Features Explained

### Risk Scoring
- Suspicious transaction ratio: 30%
- High-value transactions: up to 20%
- Cross-border activity: 20%
- High-risk countries: up to 15%
- Structuring indicators: up to 15%

### Anomaly Detection
- **Isolation Forest**: Detects outliers in multi-dimensional feature space
- **Statistical Methods**: Z-score > 3 for amounts, unusual transaction times

### ML Models
- **Random Forest**: Ensemble of decision trees
- **Gradient Boosting**: Sequential ensemble method
- Automatic feature importance analysis

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📜 Academic Project

This project is submitted as part of the **Final Semester Dissertation Project** for the **Master of Technology (MTech) in Artificial Intelligence and Machine Learning (AIML)** degree at **Birla Institute of Technology and Science (BITS), Pilani**.

**Institution**: BITS Pilani  
**Program**: MTech in AIML  
**Project Type**: Dissertation Project  
**Academic Year**: 2025-2026

## 📧 Contact

For academic inquiries or questions about this dissertation project, please contact through the appropriate BITS Pilani academic channels.

---

**Note**: This system is designed for academic research and demonstration purposes as part of an MTech dissertation. For production use, ensure compliance with local regulations and conduct thorough testing.
