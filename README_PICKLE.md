# Pickle Model Persistence - Quick Start Guide

> **Save trained models once, use them forever!** ⚡

This guide explains how to use the model persistence feature in the Fraud Management System.

---

## 🎯 What is Model Persistence?

Model persistence allows you to **save trained machine learning models to disk** and **reload them later** without retraining. This dramatically speeds up your workflow!

### Benefits

| Without Pickle | With Pickle |
|----------------|-------------|
| ⏰ Train every time (3-5 min) | ⚡ Load instantly (2 sec) |
| 💻 High CPU usage each run | 🌱 Minimal resource usage |
| 🔄 Inconsistent models | ✅ Same model every time |
| 🚫 Can't deploy without training | ✅ Deploy pre-trained models |

**Time Savings: Train once in 5 minutes, load in 2 seconds = 99% faster! 🚀**

---

## 🚀 Quick Start

### Installation

Pickle support is already installed! If you need to install dependencies:

```bash
pip install -r requirements.txt
```

This includes `joblib>=1.3.0` for model persistence.

### Basic Usage (Automatic Mode)

The easiest way - **everything happens automatically!**

```python
from src.aml_system import AMLComplianceSystem

# Initialize system
system = AMLComplianceSystem()

# Load your data
system.load_data('fraud_management_dataset-1.5L (1).csv')

# Run analysis - model is automatically handled!
results = system.run_complete_analysis()

# ✨ Magic happens:
# - First run: Trains and saves model (5 min)
# - Next runs: Loads saved model (2 sec)
```

**That's it!** No configuration needed. The system automatically:
- ✅ Checks for saved model
- ✅ Loads it if available (fast!)
- ✅ Trains new one if not found
- ✅ Saves after training

---

## 📖 Usage Examples

### Example 1: Web Application (Streamlit)

```python
# In app.py - Already implemented!
def run_analysis():
    aml_system = st.session_state.aml_system
    with st.spinner("Running analysis..."):
        # Auto-loads saved model if available
        results = aml_system.run_complete_analysis()
        return results
```

**User Experience:**
- First user: Waits 5 minutes (training)
- All subsequent users: Wait 2 seconds (loading)

### Example 2: Check if Model Exists

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('data.csv')

# Check before running
if system.ml_predictor.model_exists():
    print("✅ Saved model found! Will load quickly.")
else:
    print("⚠️ No saved model. Will train (takes a few minutes).")

# Run analysis
results = system.run_complete_analysis()
```

### Example 3: Force Retrain Model

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('new_data.csv')

# Train a new model (ignore saved one)
print("Training new model with updated data...")
system.train_new_model(save=True)

# Now use the new model
results = system.run_complete_analysis()
```

### Example 4: Load Specific Saved Model

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('data.csv')

# Load from default location
if system.load_saved_model():
    print("Model loaded successfully!")
    
    # Make predictions immediately
    prediction = system.predict_compliance_risk(transaction_data)
    print(f"Risk: {prediction['risk_label']}")
else:
    print("No saved model found. Training new one...")
    system.train_new_model()
```

### Example 5: Save Current Model

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('data.csv')

# Train model
system.train_new_model(save=False)  # Don't auto-save

# ... test the model ...
# ... satisfied with results ...

# Now save it
system.save_current_model()
print("Model saved!")
```

---

## 📁 Where Are Models Saved?

Models are saved in the **`models/`** directory:

```
models/
├── fraud_model.pkl         # 🤖 The trained ML model
├── scaler.pkl             # 📏 Feature scaling parameters
├── label_encoders.pkl     # 🔤 Categorical encoders
├── feature_names.pkl      # 📝 List of features used
└── model_metadata.pkl     # 📊 Training info & metrics
```

### File Sizes (Approximate)

- `fraud_model.pkl`: 10-50 MB
- `scaler.pkl`: < 1 MB
- `label_encoders.pkl`: < 1 MB
- `feature_names.pkl`: < 1 KB
- `model_metadata.pkl`: < 100 KB

**Total**: ~10-50 MB depending on model complexity

---

## 🎓 How It Works

### The First Time You Run Analysis

```
1. Upload data ────────────────> System checks for saved model
                                            │
2. Run analysis               ┌─────────────┘
                              ▼
                         No saved model found
                              │
3. Training starts ───────────┘
   ├─ Feature engineering
   ├─ Model training (3-5 min)
   ├─ Cross-validation
   └─ Select best model
                              │
4. Auto-save ─────────────────┘
   └─ Saves to models/ directory
                              │
5. Analysis complete ─────────┘
   └─ Results ready!
```

### Every Time After That

```
1. Upload data ────────────────> System checks for saved model
                                            │
2. Run analysis               ┌─────────────┘
                              ▼
                         Saved model found! ✅
                              │
3. Quick load ────────────────┘
   └─ Load from disk (2 sec)
                              │
4. Analysis complete ─────────┘
   └─ Results ready!
```

**Time saved: ~3 minutes per run! ⚡**

---

## 🔧 Advanced Features

### Custom Model Directory

```python
# Save to custom location
system.ml_predictor.save_model_to_disk(model_dir='my_models')

# Load from custom location
system.ml_predictor.load_model_from_disk(model_dir='my_models')

# Check custom location
if system.ml_predictor.model_exists(model_dir='my_models'):
    print("Model found in custom directory!")
```

### Access Model Metadata

```python
import joblib

# Load metadata
metadata = joblib.load('models/model_metadata.pkl')

print(f"Trained on: {metadata['timestamp']}")
print(f"Feature count: {metadata['feature_count']}")
print(f"Metrics: {metadata['model_metrics']}")
```

### Direct MLPredictor Access

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('data.csv')

# Access MLPredictor directly
predictor = system.ml_predictor

# Low-level operations
predictor.save_model_to_disk()
predictor.load_model_from_disk()
predictor.model_exists()
```

---

## ❓ FAQ

### Q: Do I need to do anything special to use pickle?
**A:** No! It's automatic. Just use `run_complete_analysis()` as usual.

### Q: When should I retrain the model?
**A:** Retrain when:
- You have new/updated data
- Model performance degrades
- You want to tune hyperparameters
- It's been a while (e.g., monthly)

### Q: Can I delete saved models?
**A:** Yes! Just delete files in `models/` directory. The system will retrain automatically.

### Q: Are saved models portable?
**A:** Mostly yes, but:
- ✅ Same Python version: Usually works
- ⚠️ Different Python versions: May work
- ❌ Different OS: May have issues
- ❌ Different scikit-learn versions: Often breaks

**Best practice**: Train on the target environment.

### Q: How do I know if a model is loaded?
**A:** Check the console output:
```
✅ Model loaded successfully from 'models/' directory
   - Trained on: 20260124_143052
   - Features: 23
```

### Q: What if loading fails?
**A:** The system automatically falls back to training. You'll see:
```
⚠ No saved model found in 'models/' directory
   Train a new model using train_compliance_model()
```

### Q: Can I version my models?
**A:** Currently, models are overwritten. For versioning:
```python
# Manual versioning
import shutil
shutil.copytree('models', 'models_v1')  # Backup
system.train_new_model()  # Creates new models/
```

See [ARCHITECTURE_PICKLE.md](ARCHITECTURE_PICKLE.md) for planned versioning features.

### Q: Is it safe to use pickle?
**A:** Pickle can execute code during loading, so:
- ✅ Safe: Loading your own models
- ✅ Safe: Models from trusted sources
- ❌ Unsafe: Models from unknown sources
- ❌ Unsafe: User-uploaded pickle files

**This app only loads local models = Safe! 🔒**

### Q: Why joblib instead of pickle?
**A:** Joblib is optimized for scikit-learn:
- Faster for large numpy arrays
- Better compression
- More efficient memory usage
- Industry standard for ML models

---

## 🐛 Troubleshooting

### Problem: Model won't load

**Symptoms:**
```
❌ Error loading model: [Errno 2] No such file or directory
```

**Solution:**
```python
# Check if model exists
import os
print(os.path.exists('models/fraud_model.pkl'))

# If False, train new model
system.train_new_model()
```

### Problem: "Module not found" error

**Symptoms:**
```
❌ Error loading model: No module named 'sklearn.ensemble'
```

**Solution:**
```bash
# Reinstall requirements
pip install -r requirements.txt
```

### Problem: Out of memory when loading

**Symptoms:**
```
❌ Error loading model: MemoryError
```

**Solution:**
- Close other applications
- Increase system RAM
- Use a smaller model (train with fewer estimators)

### Problem: Model predictions seem wrong

**Symptoms:**
- Predictions don't match expectations
- All predictions are the same

**Solution:**
```python
# Retrain with current data
system.train_new_model(save=True)

# Verify with test transaction
test_result = system.predict_compliance_risk(test_transaction)
print(test_result)
```

### Problem: Models directory is huge

**Symptoms:**
- `models/` folder is 100+ MB
- Disk space running low

**Solution:**
```bash
# Check sizes
ls -lh models/

# Delete old models (they'll be recreated)
rm models/*.pkl
```

---

## 📊 Performance Tips

### Tip 1: Use SSD Storage
- Models load 5-10x faster from SSD vs HDD
- Recommended for production deployments

### Tip 2: Optimize Compression
```python
# Default: compress=3 (balanced)
# For faster loading (larger files):
joblib.dump(model, 'model.pkl', compress=0)

# For smaller files (slower loading):
joblib.dump(model, 'model.pkl', compress=9)
```

### Tip 3: Load Models Once
```python
# Bad: Loading in loop
for transaction in transactions:
    system.load_saved_model()  # ❌ Slow!
    predict(transaction)

# Good: Load once, predict many
system.load_saved_model()  # ✅ Fast!
for transaction in transactions:
    predict(transaction)
```

### Tip 4: Monitor Model Age
```python
import os
from datetime import datetime

# Check when model was saved
model_time = os.path.getmtime('models/fraud_model.pkl')
age_days = (datetime.now().timestamp() - model_time) / 86400

if age_days > 30:
    print(f"⚠️ Model is {age_days:.0f} days old. Consider retraining.")
```

---

## 🎯 Best Practices

### ✅ Do's

- ✅ Let auto-save/load handle most cases
- ✅ Retrain monthly or when data changes significantly
- ✅ Keep backups of important models
- ✅ Document when you retrain (in metadata)
- ✅ Test loaded models before production use
- ✅ Monitor model performance over time

### ❌ Don'ts

- ❌ Don't load untrusted pickle files
- ❌ Don't commit models to Git (too large)
- ❌ Don't load models trained with different scikit-learn versions
- ❌ Don't delete models without backup
- ❌ Don't share models between incompatible environments
- ❌ Don't ignore load failures (investigate!)

---

## 📚 Additional Resources

### Documentation
- **[MODEL_PERSISTENCE.md](MODEL_PERSISTENCE.md)** - Detailed usage guide
- **[ARCHITECTURE_PICKLE.md](ARCHITECTURE_PICKLE.md)** - Technical architecture
- **[example_model_persistence.py](example_model_persistence.py)** - Interactive examples

### Testing
- **[test_pickle_integration.py](test_pickle_integration.py)** - Integration tests
- **[check_pickle_config.py](check_pickle_config.py)** - Configuration checker

### External Resources
- [Joblib Documentation](https://joblib.readthedocs.io/)
- [Scikit-learn Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [Python Pickle Security](https://docs.python.org/3/library/pickle.html#module-pickle)

---

## 🎬 Getting Started Checklist

Ready to use pickle? Follow this checklist:

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify installation: `python check_pickle_config.py`
- [ ] Run first analysis: Models will be trained and saved
- [ ] Run second analysis: Models will load instantly ⚡
- [ ] Check `models/` directory: See saved files
- [ ] Try prediction: Use loaded model for fast predictions
- [ ] (Optional) Read [MODEL_PERSISTENCE.md](MODEL_PERSISTENCE.md) for advanced features

---

## 🎉 Success Story

### Before Pickle
```
User 1: Upload data → Wait 5 min → Get results
User 2: Upload data → Wait 5 min → Get results
User 3: Upload data → Wait 5 min → Get results
Total: 15 minutes
```

### After Pickle
```
User 1: Upload data → Wait 5 min → Get results (trains & saves)
User 2: Upload data → Wait 2 sec → Get results (loads model)
User 3: Upload data → Wait 2 sec → Get results (loads model)
Total: 5 minutes 4 seconds
```

**Time saved: 10 minutes (66% faster)** for just 3 users! 🚀

---

## 🆘 Need Help?

### Quick Checks
1. **Run diagnostics**: `python check_pickle_config.py`
2. **Run tests**: `python test_pickle_integration.py`
3. **Check logs**: Look for "✅ Model loaded" or "⚠️ No saved model" messages

### Common Commands
```bash
# Check if models exist
ls models/

# Check model file sizes
du -sh models/*

# Test model loading
python -c "import sys; sys.path.insert(0, 'src'); from aml_system import AMLComplianceSystem; s=AMLComplianceSystem(); s.load_data('data.csv'); print('Loaded:', s.load_saved_model())"

# Remove all models (force retrain)
rm models/*.pkl
```

---

## 📝 Summary

**Pickle model persistence is:**
- ✅ Automatic (no configuration needed)
- ✅ Fast (99% time reduction on subsequent runs)
- ✅ Reliable (comprehensive error handling)
- ✅ Simple (works out of the box)
- ✅ Production-ready (tested and documented)

**Just run your analysis as normal** - pickle handles the rest! 🎯

---

**Version**: 1.0  
**Last Updated**: January 24, 2026  
**Questions?** Check [MODEL_PERSISTENCE.md](MODEL_PERSISTENCE.md) or [ARCHITECTURE_PICKLE.md](ARCHITECTURE_PICKLE.md)

---

**Happy model saving! 🚀**
