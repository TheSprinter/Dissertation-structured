# Pickle Integration - Model Persistence Guide

## Overview

The Fraud Management System now includes comprehensive pickle/joblib integration for model persistence. This allows you to save trained models and reuse them without retraining.

## Features

[PASS] **Save Trained Models**: Save ML models with all preprocessing components 
[PASS] **Load Pre-trained Models**: Quickly load saved models for predictions 
[PASS] **Complete Package**: Saves model, scaler, encoders, features, and metrics 
[PASS] **Model Versioning**: Save multiple model versions with custom names 
[PASS] **List Models**: View all saved models with metadata 
[PASS] **Joblib Support**: Optimized for scikit-learn models (falls back to pickle)

---

## What Gets Saved?

When you save a model, the following components are persisted:

- [PASS] **Trained ML Model** (RandomForest/GradientBoosting)
- [PASS] **StandardScaler** (feature normalization)
- [PASS] **Label Encoders** (categorical variable encoders)
- [PASS] **Feature Names** (column order and names)
- [PASS] **Model Metrics** (accuracy, precision, recall, F1)
- [PASS] **Timestamp** (when model was saved)
- [PASS] **Metadata** (number of features, model type)

---

## Usage

### 1. Using the Web Application (Streamlit)

#### Navigate to " Model Management" page:

**View Saved Models ( View Models Tab):**
- Access all previously saved models in a clean list format
- See numbered list of available models
- **Load button** - Quickly select a model for predictions
- **Info button** - View file details (size, name, timestamp)
- Shows total count of saved models
- Helpful tips for new users
- Display of model components (what gets saved with each model)

**Save Current Model ( Save Model Tab):**
- Train a model via "Data Upload & Analysis" page
- Go to "Model Management" → "Save Model" tab
- Enter custom model name or use default `ml_package.pkl`
- Click " Save Model" button
- Receive success confirmation with balloons 
- Model saved with all preprocessing components

**Load Pre-trained Model ( Load Model Tab):**
- Go to "Model Management" → "Load Model" tab
- Choose default model or custom model path
- Click " Load Model"
- Model and all components ready for predictions
- Use for batch predictions without retraining

**Model Components Saved:**
- Trained ML Model (RandomForest/GradientBoosting)
- Feature Scaler (StandardScaler)
- Label Encoders (for categorical variables)
- Feature Names and Metadata
- Model Metrics (Accuracy, Precision, Recall, F1)
- Training Timestamp

---

### 2. Using Python API

#### Example 1: Train and Save Model
```python
from aml_system import AMLComplianceSystem

# Initialize system
aml_system = AMLComplianceSystem()
aml_system.load_data('your_data.csv')

# Train and automatically save
results = aml_system.run_complete_analysis(save_model=True)

# Model saved to: models/ml_package.pkl
```

#### Example 2: Load Pre-trained Model
```python
from aml_system import AMLComplianceSystem

# Initialize system
aml_system = AMLComplianceSystem()
aml_system.load_data('your_data.csv')

# Load pre-trained model
aml_system.load_pretrained_model()

# Make predictions
prediction = aml_system.predict_compliance_risk({
    'Amount': 9500,
    'Payment_currency': 'USD',
    # ... other features
})
```

#### Example 3: Save with Custom Name
```python
# Save with version number
aml_system.save_trained_model('models/fraud_model_v2.pkl')
```

#### Example 4: List All Models
```python
# List all saved models
models = aml_system.list_available_models()
```

---

### 3. Using Example Script

Run the provided examples:

```bash
python pickle_examples.py
```

Choose from:
1. Train and save a new model
2. Load pre-trained model and make predictions
3. List all saved models
4. Save model with custom name
5. Run all examples

---

## File Locations

**Models Directory**: `models/`
- `ml_package.pkl` - Default complete package
- `fraud_model.pkl` - Just the model (lightweight)
- Custom named models (e.g., `fraud_model_v1.pkl`)

**Output Directory**: `output/`
- Analysis results, profiles, reports

---

## API Reference

### AMLComplianceSystem Methods

#### `run_complete_analysis(save_results=True, save_model=True)`
Run full analysis and optionally save the trained model.

**Parameters:**
- `save_results` (bool): Save analysis outputs to CSV
- `save_model` (bool): Save trained model to disk

**Returns:** Dictionary with results

---

#### `load_pretrained_model(model_path=None)`
Load a pre-trained model from disk.

**Parameters:**
- `model_path` (str, optional): Path to model file. Uses default if None.

**Returns:** bool - Success status

**Example:**
```python
aml_system.load_pretrained_model('models/ml_package.pkl')
```

---

#### `save_trained_model(model_path=None)`
Save currently trained model.

**Parameters:**
- `model_path` (str, optional): Where to save. Uses default if None.

**Returns:** bool - Success status

**Example:**
```python
aml_system.save_trained_model('models/my_model.pkl')
```

---

#### `list_available_models()`
List all saved models in the models directory.

**Returns:** List of model filenames

**Example:**
```python
models = aml_system.list_available_models()
```

---

### MLPredictor Methods

#### `save_model(filename=None)`
Save just the trained model (lightweight).

#### `load_model(filename=None)`
Load just the model file.

#### `save_complete_package(filename=None)`
Save model + all preprocessing components (recommended).

#### `load_complete_package(filename=None)`
Load complete package (recommended).

#### `list_saved_models()`
List all models with metadata.

---

## Best Practices

1. **Use Complete Package**: Always use `save_complete_package()` to ensure all components are saved together

2. **Version Your Models**: Use descriptive names with versions:
   ```python
   aml_system.save_trained_model('models/fraud_model_v1_20260123.pkl')
   ```

3. **Regular Backups**: Keep backup copies of production models

4. **Test After Loading**: Always verify predictions after loading:
   ```python
   if aml_system.load_pretrained_model():
       # Test prediction
       test_result = aml_system.predict_compliance_risk(test_data)
   ```

5. **Monitor File Sizes**: Large models may need compression or pruning

6. **Security**: Only load pickle files from trusted sources (security risk)

---

## Technology Stack

### Model Persistence & Serialization
- **Joblib** (v1.3.0+)
  - Optimized for scikit-learn models and NumPy arrays
  - More efficient compression than standard pickle
  - Better performance for large models
  - Parallel backend support for distributed storage
  - Recommended for production use

- **Python pickle** (Built-in)
  - Standard Python object serialization protocol
  - Used as fallback when joblib is unavailable
  - Secure when used with trusted model sources only
  - Supported protocols: 2, 3, 4, 5 (protocol 5 recommended)

### Model Components Persisted
- **Trained ML Model** - RandomForest/GradientBoosting classifier
- **StandardScaler** - Feature normalization
- **LabelEncoders** - Categorical variable encoding
- **Feature Names** - Column order and metadata
- **Model Metrics** - Accuracy, precision, recall, F1 scores
- **Metadata** - Timestamp, model type, feature count

### Machine Learning & AI
- **Scikit-learn** (v1.3.0+) - ML algorithms with pickle-compatible estimators
- **NumPy** (v1.24.0+) - Numerical computing for preprocessing

### Data Processing
- **Pandas** (v2.0.0+) - Data manipulation and feature engineering
- **Python-dateutil** (v2.8.0+) - Date/time utilities

### Web Framework
- **Streamlit** (v1.30.0+) - Interactive UI for model management and file operations

### Runtime & Deployment
- **Python** (v3.8+) - Programming language
- **Docker** - Containerization with persistent model volumes

### Optional Deep Learning
- **TensorFlow** (v2.13.0+) - Deep learning framework (SavedModel format)
- **Keras** (v2.13.0+) - Neural network API (h5 format support)

### Performance Characteristics
- **Save Time**: < 2 seconds for complete package
- **Load Time**: < 1 second for most models
- **File Size**: 5-50 MB depending on model complexity
- **Compression**: Joblib offers optional compression (gzip)

---

## Troubleshooting

### Model Not Found
```
[WARN] No saved package found at models/ml_package.pkl
```
**Solution:** Train a model first or check the file path.

---

### Import Error
```
AttributeError: module has no attribute 'load'
```
**Solution:** Install joblib:
```bash
pip install joblib
```

---

### Version Mismatch
```
ModuleNotFoundError: No module named 'sklearn.xxx'
```
**Solution:** Ensure scikit-learn version matches:
```bash
pip install scikit-learn>=1.3.0
```

---

## Performance

- **Joblib**: ~2-3x faster than pickle for sklearn models
- **File Size**: Complete package typically 1-5 MB
- **Load Time**: < 1 second for most models
- **Save Time**: < 2 seconds for complete package

---

## Security Note

[WARN] **WARNING**: Never load pickle files from untrusted sources. Malicious pickle files can execute arbitrary code.

**Safe Usage:**
- Only load models you created
- Verify file integrity before loading
- Use in controlled environments

---

## Additional Resources

- [Streamlit App](app.py) - Full web interface
- [Example Script](pickle_examples.py) - Usage examples
- [ML Predictor Module](src/modules/ml_predictor.py) - Implementation
- [Main System](src/aml_system.py) - System integration

---

## Quick Reference

```python
# Train and save
aml_system.run_complete_analysis(save_model=True)

# Load and predict
aml_system.load_pretrained_model()
prediction = aml_system.predict_compliance_risk(data)

# List models
aml_system.list_available_models()

# Custom save
aml_system.save_trained_model('models/my_model.pkl')
```

---

**Last Updated**: January 23, 2026 
**Version**: 1.0
