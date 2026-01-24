# Pickle Integration Architecture

```
╔═══════════════════════════════════════════════════════════════════════╗
║                 FRAUD MANAGEMENT SYSTEM                               ║
║                  With Pickle Integration                              ║
╚═══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐│
│  │  Streamlit Web   │  │  Python API      │  │  CLI Scripts     ││
│  │  app.py          │  │  (Direct calls)  │  │  Examples/Demo   ││
│  │                  │  │                  │  │                  ││
│  │ • Model Mgmt UI  │  │ • aml_system     │  │ • pickle_        ││
│  │ • View Models    │  │ • ml_predictor   │  │   examples.py    ││
│  │ • Save/Load      │  │ • Direct access  │  │ • demo_pickle.py ││
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘│
│           │                     │                      │          │
└───────────┼─────────────────────┼──────────────────────┼──────────┘
            │                     │                      │
            └─────────────────────┼──────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MAIN SYSTEM LAYER                                │
│                   (src/aml_system.py)                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  class AMLComplianceSystem:                                         │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ ✨ NEW PICKLE METHODS ✨                                 │   │
│    ├─────────────────────────────────────────────────────────┤   │
│    │ • run_complete_analysis(save_results=True)              │   │
│    │   └─ Auto-loads saved model if available                │   │
│    │ • train_new_model(save=True)                            │   │
│    │ • load_saved_model(model_dir='models')                  │   │
│    │ • save_current_model(model_dir='models')                │   │
│    └─────────────────────────────────────────────────────────┘   │
│            │                                                       │
│            ▼                                                       │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ EXISTING FUNCTIONALITY                                   │   │
│    ├─────────────────────────────────────────────────────────┤   │
│    │ • load_data()                                            │   │
│    │ • predict_compliance_risk()                              │   │
│    │ • get_customer_risk_profile()                            │   │
│    └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ML PREDICTOR MODULE                              │
│               (src/modules/ml_predictor.py)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  class MLPredictor:                                                 │
│                                                                     │
│    ┌──────────────────────────────────────────────────────────┐  │
│    │ ✨ PICKLE FUNCTIONALITY ✨                                 │  │
│    ├──────────────────────────────────────────────────────────┤  │
│    │                                                            │  │
│    │  SAVE OPERATION                                            │  │
│    │  └─ save_model_to_disk(model_dir='models')               │  │
│    │      └─ Saves 5 separate pickle files                    │  │
│    │                                                            │  │
│    │  LOAD OPERATION                                            │  │
│    │  └─ load_model_from_disk(model_dir='models')             │  │
│    │      └─ Loads all 5 pickle files                         │  │
│    │                                                            │  │
│    │  CHECK OPERATION                                           │  │
│    │  └─ model_exists(model_dir='models')                     │  │
│    │      └─ Checks if fraud_model.pkl exists                 │  │
│    │                                                            │  │
│    └──────────────────────────────────────────────────────────┘  │
│            │                                                       │
│            ▼                                                       │
│    ┌──────────────────────────────────────────────────────────┐  │
│    │ MODEL TRAINING (Existing)                                 │  │
│    ├──────────────────────────────────────────────────────────┤  │
│    │ • train_compliance_model()                                │  │
│    │ • predict_risk()                                          │  │
│    │ • _prepare_ml_features()                                  │  │
│    └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PERSISTENCE LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐           ┌──────────────────┐             │
│  │  JOBLIB          │           │  PICKLE          │             │
│  │  (Primary)       │           │  (Fallback)      │             │
│  ├──────────────────┤           ├──────────────────┤             │
│  │ • Faster (2-3x)  │           │ • Standard lib   │             │
│  │ • Optimized for  │           │ • Always works   │             │
│  │   sklearn        │           │ • Universal      │             │
│  │ • Compression    │           │                  │             │
│  └────────┬─────────┘           └────────┬─────────┘             │
│           │                              │                        │
│           └──────────────┬───────────────┘                        │
│                          │                                        │
└──────────────────────────┼────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FILE STORAGE                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📁 models/                                                         │
│    ├─ fraud_model.pkl         (Trained ML model - 10-50 MB)       │
│    ├─ scaler.pkl              (StandardScaler - <1 MB)            │
│    ├─ label_encoders.pkl      (Categorical encoders - <1 MB)      │
│    ├─ feature_names.pkl       (Feature list - <1 KB)              │
│    └─ model_metadata.pkl      (Metrics & timestamp - <100 KB)     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                         SAVED FILES CONTENTS
═══════════════════════════════════════════════════════════════════════

When you call save_model_to_disk(), it creates 5 separate files:

┌─────────────────────────────────────────────────────────────────────┐
│  1. fraud_model.pkl                                                 │
│     └─ RandomForestClassifier / GradientBoostingClassifier         │
│        (The actual trained model)                                   │
│                                                                     │
│  2. scaler.pkl                                                      │
│     └─ StandardScaler(...)                                         │
│        (Fitted with training data statistics)                      │
│                                                                     │
│  3. label_encoders.pkl                                             │
│     └─ {                                                           │
│          'Payment_type': LabelEncoder(),                           │
│          'Sender_bank_location': LabelEncoder(),                   │
│          'Receiver_bank_location': LabelEncoder(),                 │
│          'Payment_currency': LabelEncoder(),                       │
│          'Received_currency': LabelEncoder()                       │
│        }                                                            │
│                                                                     │
│  4. feature_names.pkl                                              │
│     └─ ['Amount', 'log_amount', 'hour', 'is_weekend', ...]        │
│        (List of 20+ engineered features)                           │
│                                                                     │
│  5. model_metadata.pkl                                             │
│     └─ {                                                           │
│          'model_metrics': {'accuracy': 0.893, ...},                │
│          'timestamp': '20260124_143052',                           │
│          'feature_count': 23                                       │
│        }                                                            │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                         WORKFLOW EXAMPLES
═══════════════════════════════════════════════════════════════════════

SCENARIO 1: First Time Training (Auto-Save Enabled)
────────────────────────────────────────────────────
User → app.py → AMLSystem.run_complete_analysis()
                                ↓
                    Check: model_exists() → False
                                ↓
                MLPredictor.train_compliance_model(save_model=True)
                                ↓
                    save_model_to_disk()
                                ↓
                Creates 5 files in models/:
                  • fraud_model.pkl
                  • scaler.pkl
                  • label_encoders.pkl
                  • feature_names.pkl
                  • model_metadata.pkl


SCENARIO 2: Subsequent Runs (Auto-Load Enabled)
────────────────────────────────────────────────
User → app.py → AMLSystem.run_complete_analysis()
                                ↓
                MLPredictor.load_model_from_disk()
                                ↓
                    Check: fraud_model.pkl exists? → Yes
                                ↓
                Load all 5 files:
                  • Load fraud_model.pkl → self.model
                  • Load scaler.pkl → self.scaler
                  • Load label_encoders.pkl → self.label_encoders
                  • Load feature_names.pkl → self.feature_names
                  • Load model_metadata.pkl → self.model_metrics
                                ↓
                    READY FOR PREDICTIONS (2 seconds!)


SCENARIO 3: Making Predictions with Loaded Model
─────────────────────────────────────────────────
User → AMLSystem.predict_compliance_risk(transaction)
              ↓
       MLPredictor.predict_risk()
              ↓
       Uses: self.model + self.scaler + self.label_encoders
              ↓
       Returns: {
         'risk_probability': 0.75,
         'risk_label': 'High Risk',
         'risk_score': 75.0
       }


═══════════════════════════════════════════════════════════════════════
                         KEY BENEFITS
═══════════════════════════════════════════════════════════════════════

✅ Automatic Save/Load
   Training auto-saves → Subsequent runs auto-load
   No manual intervention required!

✅ Lightning Fast
   Training: 3-5 minutes → Loading: 2 seconds
   99% time reduction on subsequent runs

✅ Production Ready
   Train once in dev → Deploy pre-trained model to prod
   No training pipeline needed in production

✅ Complete Persistence
   Saves model + scaler + encoders + features + metadata
   Everything needed for predictions included

✅ Transparent Integration
   Auto-load in run_complete_analysis()
   Fallback to training if load fails
   Zero configuration needed

✅ Joblib Optimized
   Compression enabled (compress=3)
   Faster for scikit-learn models
   Efficient numpy array handling


═══════════════════════════════════════════════════════════════════════
```