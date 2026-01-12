# Project Structure Overview

## Directory Tree

```
aml_compliance_system/
│
├── 📄 main.py                          # Main entry point - Run this!
├── 📄 setup.py                         # Setup and verification script
├── 📄 requirements.txt                 # Python dependencies
├── 📄 README.md                        # Comprehensive documentation
├── 📄 QUICKSTART.md                    # Quick start guide
├── 📄 STRUCTURE.md                     # This file
├── 📄 .gitignore                       # Git ignore rules
│
├── 📁 src/                             # Source code directory
│   ├── 📄 __init__.py                  # Package initializer
│   ├── 📄 config.py                    # Configuration settings
│   ├── 📄 aml_system.py                # Main orchestrator class
│   │
│   └── 📁 modules/                     # Core modules
│       ├── 📄 __init__.py              # Modules package init
│       ├── 📄 data_manager.py          # Data loading & generation
│       ├── 📄 customer_profiler.py     # Customer risk profiling
│       ├── 📄 anomaly_detector.py      # Anomaly detection
│       ├── 📄 ml_predictor.py          # ML model training
│       └── 📄 visualizer.py            # Visualization & reporting
│
├── 📁 data/                            # Data storage
│   └── (place your CSV files here)
│
├── 📁 output/                          # Generated outputs
│   ├── customer_profiles.csv
│   ├── detected_anomalies.csv
│   ├── dashboard.png
│   ├── detailed_analysis.png
│   └── customer_profiles.png
│
└── 📁 tests/                           # Unit tests
    └── 📄 test_system.py               # System tests
```

## Module Dependencies

```
main.py
  └── AMLComplianceSystem (aml_system.py)
       ├── DataManager (data_manager.py)
       ├── CustomerProfiler (customer_profiler.py)
       ├── AnomalyDetector (anomaly_detector.py)
       ├── MLPredictor (ml_predictor.py)
       └── AMLVisualizer (visualizer.py)
```

## Data Flow

```
1. Data Input
   ├── CSV File
   └── Synthetic Generation
        ↓
2. Data Manager
   ├── Load & Validate
   └── Display Summary
        ↓
3. Analysis Pipeline
   ├── Customer Profiling → profiles.csv
   ├── Anomaly Detection → anomalies.csv
   ├── ML Training → model
   └── Visualization → PNG files
        ↓
4. Predictions & Reports
   ├── Risk Prediction
   ├── Customer Profiles
   └── Summary Report
```

## Module Descriptions

### 📄 main.py
**Purpose**: Entry point for running the complete system
- Initializes AMLComplianceSystem
- Loads data
- Runs complete analysis
- Demonstrates prediction capabilities
- Generates summary report

### 📄 src/aml_system.py
**Purpose**: Main orchestrator that coordinates all modules
**Key Methods**:
- `load_data()` - Initialize all modules with data
- `run_complete_analysis()` - Execute full pipeline
- `predict_compliance_risk()` - Predict single transaction
- `get_customer_risk_profile()` - Get customer details
- `generate_summary_report()` - Executive summary

### 📄 src/modules/data_manager.py
**Purpose**: Data loading, validation, and synthetic generation
**Key Methods**:
- `load_data()` - Load from CSV or generate synthetic
- `_display_data_summary()` - Show data overview
- `_generate_synthetic_data()` - Create test data

### 📄 src/modules/customer_profiler.py
**Purpose**: Customer risk profiling and classification
**Key Methods**:
- `analyze_customers()` - Profile all customers
- `_create_customer_profile()` - Single customer profile
- `_calculate_risk_scores()` - Compute risk metrics
**Output**: Customer profiles with risk scores (0-100)

### 📄 src/modules/anomaly_detector.py
**Purpose**: Transaction anomaly detection
**Key Methods**:
- `detect_anomalies()` - Run detection algorithms
- `_isolation_forest_detection()` - ML-based detection
- `_statistical_detection()` - Statistical analysis
**Algorithms**: Isolation Forest, Z-score analysis

### 📄 src/modules/ml_predictor.py
**Purpose**: Machine learning model training and prediction
**Key Methods**:
- `train_compliance_model()` - Train models
- `predict_risk()` - Predict transaction risk
- `_engineer_features()` - Feature engineering
**Models**: Random Forest, Gradient Boosting

### 📄 src/modules/visualizer.py
**Purpose**: Data visualization and reporting
**Key Methods**:
- `create_comprehensive_dashboard()` - Main dashboard
- `generate_compliance_report()` - Text report
- `_plot_customer_profiles()` - Customer charts
**Output**: PNG files with visualizations

### 📄 src/config.py
**Purpose**: Centralized configuration
**Settings**:
- Risk thresholds
- High-risk locations
- Model parameters
- Output settings

## File Sizes (Approximate)

| File | Lines | Size |
|------|-------|------|
| data_manager.py | 120 | 4 KB |
| customer_profiler.py | 160 | 6 KB |
| anomaly_detector.py | 150 | 6 KB |
| ml_predictor.py | 220 | 9 KB |
| visualizer.py | 250 | 10 KB |
| aml_system.py | 140 | 5 KB |
| main.py | 100 | 4 KB |

## Usage Patterns

### Pattern 1: Complete Analysis
```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('data.csv')
results = system.run_complete_analysis()
```

### Pattern 2: Individual Modules
```python
from src.modules.data_manager import DataManager
from src.modules.customer_profiler import CustomerProfiler

dm = DataManager()
df = dm.load_data('data.csv')

profiler = CustomerProfiler(df)
profiles = profiler.analyze_customers()
```

### Pattern 3: Real-time Prediction
```python
system = AMLComplianceSystem()
system.load_data('data.csv')
system.run_complete_analysis()

# Now predict new transactions
risk = system.predict_compliance_risk(new_transaction)
```

## Execution Order

1. **Setup**: `python setup.py` (one-time)
2. **Install**: `pip install -r requirements.txt` (one-time)
3. **Run**: `python main.py` (every time)

## Output Generation

| Step | Module | Output |
|------|--------|--------|
| 1 | Data Manager | Console summary |
| 2 | Customer Profiler | customer_profiles.csv |
| 3 | Anomaly Detector | detected_anomalies.csv |
| 4 | ML Predictor | Trained model (in memory) |
| 5 | Visualizer | dashboard.png, detailed_analysis.png, customer_profiles.png |

## Extension Points

Want to extend the system? Here's where to add features:

- **New data source**: Modify `DataManager.load_data()`
- **New risk factors**: Update `CustomerProfiler._calculate_risk_scores()`
- **New detection algorithm**: Add to `AnomalyDetector`
- **New ML model**: Add to `MLPredictor._train_multiple_models()`
- **New visualization**: Add to `AMLVisualizer`
- **New configuration**: Add to `config.py`

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_system.py

# Run with coverage
python -m pytest tests/ --cov=src
```

---

**Note**: This modular structure allows each component to be used independently or as part of the complete system.
