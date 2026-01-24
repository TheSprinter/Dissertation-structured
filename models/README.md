# Models Directory

This directory stores trained ML models and related files.

## 🛠️ Technologies Used for Model Storage

- **joblib** (v1.3.0+) - Model serialization format for efficient storage and loading
- **scikit-learn** (v1.3.0+) - Generates compatible model files
- **Python pickle** - Binary serialization protocol for Python objects

## Contents (after training):
- fraud_model.pkl - Trained machine learning model
- scaler.pkl - Feature scaler
- label_encoders.pkl - Categorical encoders
- feature_names.pkl - Feature list
- model_metadata.pkl - Training metadata

Note: Model files are generated during training and can be large.
Consider adding *.pkl to .gitignore if not version controlling models.
