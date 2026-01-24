# Model Persistence with Pickle/Joblib

This project now includes **model persistence** functionality, allowing you to save trained ML models to disk and reload them without retraining.

## 🎯 Overview

The system uses **joblib** (optimized for scikit-learn) to serialize and save:
- ✅ Trained ML models
- ✅ Feature scalers
- ✅ Label encoders
- ✅ Feature names
- ✅ Model metrics and metadata

## 📁 Saved Files Structure

```
models/
├── fraud_model.pkl         # Trained RandomForest/GradientBoosting model
├── scaler.pkl             # StandardScaler for feature normalization
├── label_encoders.pkl     # LabelEncoders for categorical features
├── feature_names.pkl      # List of feature names
└── model_metadata.pkl     # Training timestamp, metrics, feature count
```

## 🚀 Usage

### 1. Automatic Model Saving (Default)

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('your_data.csv')

# Run analysis - model is automatically saved
system.run_complete_analysis()
```

### 2. Explicit Model Training & Saving

```python
# Train and save model
system.ml_predictor.train_compliance_model(save_model=True)

# Train without saving
system.ml_predictor.train_compliance_model(save_model=False)
```

### 3. Loading Saved Models

```python
from src.aml_system import AMLComplianceSystem

system = AMLComplianceSystem()
system.load_data('your_data.csv')

# Load pre-trained model
if system.ml_predictor.load_model_from_disk():
    print("Model loaded successfully!")
    # Ready to make predictions
else:
    print("No saved model found. Training new model...")
    system.ml_predictor.train_compliance_model()
```

### 4. Smart Loading (Check Before Load)

```python
# Check if model exists
if system.ml_predictor.model_exists():
    system.ml_predictor.load_model_from_disk()
else:
    system.ml_predictor.train_compliance_model()
```

### 5. System-Level Methods

```python
# Load saved model
system.load_saved_model()

# Train new model
system.train_new_model(save=True)

# Save current model
system.save_current_model()
```

## 📊 Complete Analysis with Persistence

The `run_complete_analysis()` method now **automatically**:
1. Checks for saved model
2. Loads it if available
3. Trains new model only if needed

```python
system = AMLComplianceSystem()
system.load_data('fraud_management_dataset-1.5L (1).csv')

# Will use saved model if available, or train new one
results = system.run_complete_analysis()
```

## 🔧 Custom Model Directory

```python
# Save to custom directory
system.ml_predictor.save_model_to_disk(model_dir='my_models')

# Load from custom directory
system.ml_predictor.load_model_from_disk(model_dir='my_models')

# Check custom directory
system.ml_predictor.model_exists(model_dir='my_models')
```

## 🎓 Example Scripts

Run the included example script:

```bash
python example_model_persistence.py
```

This demonstrates:
- Training and saving models
- Loading pre-trained models
- Smart model management
- Complete analysis workflow

## 🔍 Benefits

### ⏱️ Time Savings
- **No retraining needed** - Load models instantly
- Training takes minutes, loading takes seconds

### 💾 Resource Efficiency
- **Save computational resources** - Train once, use many times
- Ideal for production deployments

### 🔄 Version Control
- **Track model versions** with timestamps
- Easy rollback to previous models

### 🚀 Production Ready
- **Deploy trained models** without training pipeline
- Consistent predictions across sessions

## 📝 API Reference

### MLPredictor Methods

```python
# Save model
ml_predictor.save_model_to_disk(model_dir='models')

# Load model
success = ml_predictor.load_model_from_disk(model_dir='models')

# Check if model exists
exists = ml_predictor.model_exists(model_dir='models')

# Train with/without saving
ml_predictor.train_compliance_model(save_model=True)
```

### AMLComplianceSystem Methods

```python
# Load saved model
system.load_saved_model(model_dir='models')

# Train new model
system.train_new_model(save=True)

# Save current model
system.save_current_model(model_dir='models')
```

## ⚠️ Important Notes

1. **Train before Save**: Model must be trained before saving
2. **Load after Data**: Load data before loading model (needs same features)
3. **Feature Consistency**: Loaded model requires same features as training
4. **Joblib Dependency**: Ensure `joblib>=1.3.0` is installed

## 🔒 Security

- Pickle can execute arbitrary code - only load trusted models
- Don't share pickled models from untrusted sources
- Use joblib compression (compress=3) for efficiency

## 🛠️ Troubleshooting

### Model Not Loading
```python
# Check if file exists
import os
print(os.path.exists('models/fraud_model.pkl'))

# Check directory contents
print(os.listdir('models/'))
```

### Feature Mismatch Error
- Ensure data has same columns as training data
- Check feature_names.pkl for required features

### Corrupted Model File
- Retrain and save new model
- Check disk space and permissions

## 📈 Performance

| Operation | Time (approx) |
|-----------|---------------|
| Train model | 2-5 minutes |
| Save model | 1-2 seconds |
| Load model | 1-2 seconds |
| Prediction | < 1 second |

## 🎉 Summary

Model persistence is now **fully integrated** into your fraud detection system:
- ✅ Automatic saving after training
- ✅ Smart loading in analysis pipeline
- ✅ Complete metadata tracking
- ✅ Production-ready implementation

Train once, predict forever! 🚀
