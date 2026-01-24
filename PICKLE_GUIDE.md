# Pickle Integration Guide

> **Complete guide to model persistence in the Fraud Management System**

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Quick Setup](#quick-setup)
3. [How It Works](#how-it-works)
4. [File Structure](#file-structure)
5. [API Reference](#api-reference)
6. [Usage Patterns](#usage-patterns)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

The Fraud Management System uses **joblib** for model persistence, allowing you to:
- ✅ Save trained models to disk
- ✅ Load models instantly (2 seconds vs 5 minutes training)
- ✅ Deploy pre-trained models to production
- ✅ Share models across sessions

### Why Joblib?

- **Fast**: 2-3x faster than standard pickle for ML models
- **Optimized**: Built for scikit-learn and numpy
- **Compressed**: Reduces file sizes by ~50%
- **Reliable**: Industry standard for ML model persistence

---

## Quick Setup

### Installation

```bash
# Install all dependencies (includes joblib)
pip install -r requirements.txt
```

### Verify Setup

```bash
python check_pickle_config.py
```

You should see:
```
🎉 RESULT: Pickle is PROPERLY CONFIGURED!
```

---

## How It Works

### Automatic Mode (Recommended)

The system automatically handles model persistence:

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('data.csv')

# First run: Trains and saves model
results = system.run_complete_analysis()

# Future runs: Loads saved model automatically
results = system.run_complete_analysis()
```

**What happens:**
1. First run: Model trained (5 min) → Auto-saved to `models/`
2. Next runs: Model loaded from disk (2 sec) → Ready instantly!

### Manual Mode (Advanced)

For more control:

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('data.csv')

# Check if model exists
if system.ml_predictor.model_exists():
    # Load existing model
    system.load_saved_model()
    print("✅ Model loaded!")
else:
    # Train new model
    system.train_new_model(save=True)
    print("✅ Model trained and saved!")

# Make predictions
result = system.predict_compliance_risk(transaction_data)
```

---

## File Structure

### Saved Files

When you save a model, 5 files are created:

```
models/
├── fraud_model.pkl         # The trained ML model (10-50 MB)
├── scaler.pkl             # Feature scaler (<1 MB)
├── label_encoders.pkl     # Categorical encoders (<1 MB)
├── feature_names.pkl      # Feature list (<1 KB)
└── model_metadata.pkl     # Training info (<100 KB)
```

### File Contents

#### 1. fraud_model.pkl
- **Contains**: Trained RandomForest or GradientBoosting classifier
- **Purpose**: Core prediction model
- **Size**: 10-50 MB (depends on model complexity)

#### 2. scaler.pkl
- **Contains**: Fitted StandardScaler
- **Purpose**: Normalizes features before prediction
- **Size**: <1 MB

#### 3. label_encoders.pkl
- **Contains**: Dictionary of LabelEncoder objects for:
  - Payment_type
  - Sender_bank_location
  - Receiver_bank_location
  - Payment_currency
  - Received_currency
- **Purpose**: Converts categorical features to numeric
- **Size**: <1 MB

#### 4. feature_names.pkl
- **Contains**: List of feature names (20+ features)
- **Purpose**: Ensures correct feature ordering during prediction
- **Size**: <1 KB

#### 5. model_metadata.pkl
- **Contains**:
  ```python
  {
      'model_metrics': {'accuracy': 0.893, 'precision': 0.650, ...},
      'timestamp': '20260124_143052',
      'feature_count': 23
  }
  ```
- **Purpose**: Track model performance and version
- **Size**: <100 KB

---

## API Reference

### AMLComplianceSystem Methods

#### `run_complete_analysis(save_results=True)`
Run complete analysis with automatic model handling.

```python
system = AMLComplianceSystem()
system.load_data('data.csv')
results = system.run_complete_analysis()  # Auto-loads or trains
```

**Behavior:**
- Checks for saved model
- Loads if exists (fast)
- Trains if not found (saves automatically)

---

#### `train_new_model(save=True)`
Force train a new model (bypass auto-load).

```python
system.train_new_model(save=True)  # Train and save
system.train_new_model(save=False) # Train only (don't save)
```

**Use when:**
- You have new/updated data
- You want to retrain with different parameters
- Model performance has degraded

---

#### `load_saved_model(model_dir='models')`
Explicitly load a saved model.

```python
# Load from default location
success = system.load_saved_model()

# Load from custom location
success = system.load_saved_model(model_dir='my_models')
```

**Returns:** `True` if successful, `False` if no model found

---

#### `save_current_model(model_dir='models')`
Explicitly save the current model.

```python
# Save to default location
system.save_current_model()

# Save to custom location
system.save_current_model(model_dir='backup_models')
```

**Raises:** `ValueError` if no model to save

---

### MLPredictor Methods

#### `save_model_to_disk(model_dir='models')`
Save all model components to disk.

```python
predictor = system.ml_predictor
predictor.save_model_to_disk()  # Default location
predictor.save_model_to_disk('my_models')  # Custom location
```

**Saves:**
- fraud_model.pkl
- scaler.pkl
- label_encoders.pkl
- feature_names.pkl
- model_metadata.pkl

---

#### `load_model_from_disk(model_dir='models')`
Load all model components from disk.

```python
predictor = system.ml_predictor
success = predictor.load_model_from_disk()  # Default location
success = predictor.load_model_from_disk('my_models')  # Custom
```

**Returns:** `True` if successful, `False` otherwise

---

#### `model_exists(model_dir='models')`
Check if a saved model exists.

```python
if predictor.model_exists():
    print("Model found!")
else:
    print("No model saved yet.")
```

**Returns:** `True` if fraud_model.pkl exists

---

#### `train_compliance_model(test_size=0.3, save_model=True)`
Train ML model with optional auto-save.

```python
# Train and save (default)
model = predictor.train_compliance_model()

# Train without saving
model = predictor.train_compliance_model(save_model=False)

# Custom test size
model = predictor.train_compliance_model(test_size=0.2)
```

---

## Usage Patterns

### Pattern 1: Web Application (Streamlit)

```python
# In app.py
def run_analysis():
    system = st.session_state.aml_system
    with st.spinner("Running analysis..."):
        # Automatically loads model if available
        results = system.run_complete_analysis()
        return results
```

**User Experience:**
- First user: 5-minute wait (training)
- Subsequent users: 2-second wait (loading)

---

### Pattern 2: Batch Processing

```python
from src.aml_system import AMLComplianceSystem

# Initialize once
system = AMLComplianceSystem()
system.load_data('data.csv')

# Load model once
system.load_saved_model()

# Process many transactions
for transaction in transactions:
    result = system.predict_compliance_risk(transaction)
    print(f"Risk: {result['risk_label']}")
```

**Performance:** Process 1000s of transactions per second

---

### Pattern 3: Model Updates

```python
from src.aml_system import AMLComplianceSystem

# Load current model
system = AMLComplianceSystem()
system.load_data('updated_data.csv')

# Backup old model
import shutil
shutil.copytree('models', 'models_backup_20260124')

# Train new model
system.train_new_model(save=True)
print("✅ New model saved!")
```

---

### Pattern 4: A/B Testing

```python
# Load model A
system_a = AMLComplianceSystem()
system_a.load_data('data.csv')
system_a.ml_predictor.load_model_from_disk('models_a')

# Load model B
system_b = AMLComplianceSystem()
system_b.load_data('data.csv')
system_b.ml_predictor.load_model_from_disk('models_b')

# Compare predictions
result_a = system_a.predict_compliance_risk(transaction)
result_b = system_b.predict_compliance_risk(transaction)

print(f"Model A: {result_a['risk_score']}")
print(f"Model B: {result_b['risk_score']}")
```

---

## Best Practices

### ✅ Do's

1. **Let auto-save/load handle most cases**
   ```python
   # Good: Automatic handling
   system.run_complete_analysis()
   ```

2. **Retrain periodically**
   ```python
   # Good: Monthly retraining
   if days_since_training > 30:
       system.train_new_model()
   ```

3. **Keep model backups**
   ```python
   # Good: Backup before retraining
   shutil.copytree('models', f'models_backup_{date}')
   system.train_new_model()
   ```

4. **Monitor model age**
   ```python
   # Good: Check model freshness
   import os
   from datetime import datetime
   
   model_time = os.path.getmtime('models/fraud_model.pkl')
   age_days = (datetime.now().timestamp() - model_time) / 86400
   if age_days > 30:
       print("⚠️ Model is old. Consider retraining.")
   ```

5. **Test after loading**
   ```python
   # Good: Validate loaded model
   if system.load_saved_model():
       test_result = system.predict_compliance_risk(test_transaction)
       assert test_result is not None
   ```

### ❌ Don'ts

1. **Don't load untrusted models**
   ```python
   # Bad: Security risk!
   system.load_saved_model('untrusted_source/models')
   ```

2. **Don't commit models to Git**
   ```bash
   # Bad: Models are too large
   git add models/*.pkl  # ❌
   
   # Good: Add to .gitignore
   echo "models/*.pkl" >> .gitignore
   ```

3. **Don't ignore load failures**
   ```python
   # Bad: Silent failure
   system.load_saved_model()
   
   # Good: Handle failures
   if not system.load_saved_model():
       print("Loading failed. Training new model...")
       system.train_new_model()
   ```

4. **Don't load in loops**
   ```python
   # Bad: Inefficient
   for transaction in transactions:
       system.load_saved_model()  # ❌ Loads every iteration
       predict(transaction)
   
   # Good: Load once
   system.load_saved_model()
   for transaction in transactions:
       predict(transaction)
   ```

5. **Don't mix model versions**
   ```python
   # Bad: Incompatible components
   predictor.model = joblib.load('models_v1/fraud_model.pkl')
   predictor.scaler = joblib.load('models_v2/scaler.pkl')  # ❌
   
   # Good: Load complete set
   predictor.load_model_from_disk('models_v1')
   ```

---

## Troubleshooting

### Problem: Model won't load

**Symptoms:**
```
⚠ No saved model found in 'models/' directory
```

**Solutions:**
1. Check if files exist:
   ```bash
   ls models/
   ```

2. Train and save model:
   ```python
   system.train_new_model(save=True)
   ```

---

### Problem: "Module not found" error

**Symptoms:**
```
❌ No module named 'sklearn.ensemble'
```

**Solutions:**
1. Reinstall requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Check scikit-learn version:
   ```bash
   pip show scikit-learn
   ```

---

### Problem: Predictions are wrong

**Symptoms:**
- All predictions return same value
- Predictions don't match expectations

**Solutions:**
1. Retrain with current data:
   ```python
   system.train_new_model(save=True)
   ```

2. Verify model metrics:
   ```python
   import joblib
   metadata = joblib.load('models/model_metadata.pkl')
   print(metadata['model_metrics'])
   ```

---

### Problem: Out of memory

**Symptoms:**
```
❌ MemoryError
```

**Solutions:**
1. Close other applications
2. Use smaller model:
   ```python
   # Reduce estimators
   from sklearn.ensemble import RandomForestClassifier
   model = RandomForestClassifier(n_estimators=50)  # Instead of 100
   ```

---

### Problem: Slow loading

**Symptoms:**
- Loading takes >10 seconds
- App feels sluggish

**Solutions:**
1. Use SSD storage (5-10x faster)
2. Reduce compression:
   ```python
   joblib.dump(model, 'model.pkl', compress=0)  # Faster, larger
   ```
3. Load models at startup, not per-request

---

## Additional Resources

### Documentation
- [README_PICKLE.md](README_PICKLE.md) - Quick start guide
- [MODEL_PERSISTENCE.md](MODEL_PERSISTENCE.md) - Detailed usage
- [ARCHITECTURE_PICKLE.md](ARCHITECTURE_PICKLE.md) - Technical architecture

### Code Examples
- [example_model_persistence.py](example_model_persistence.py) - Interactive examples
- [demo_pickle.py](demo_pickle.py) - Live demonstration
- [pickle_examples.py](pickle_examples.py) - Code snippets

### Testing & Verification
- [test_pickle_integration.py](test_pickle_integration.py) - Integration tests
- [check_pickle_config.py](check_pickle_config.py) - Configuration checker

### External Links
- [Joblib Documentation](https://joblib.readthedocs.io/)
- [Scikit-learn Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [Python Pickle Security](https://docs.python.org/3/library/pickle.html)

---

## Summary

Pickle integration provides:
- ✅ **Automatic** save/load (no configuration)
- ✅ **Fast** loading (99% time reduction)
- ✅ **Complete** persistence (model + all components)
- ✅ **Reliable** error handling
- ✅ **Production-ready** deployment

**Just use `run_complete_analysis()` - everything else is automatic!** 🚀

---

**Version**: 1.0  
**Last Updated**: January 24, 2026  
**Author**: Fraud Management System Team
