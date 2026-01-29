# Fraud Management System - Architecture Diagram

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACES LAYER                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────┐              ┌─────────────────────┐              │
│  │   Streamlit Web App │              │  CLI Interface      │              │
│  │     (app.py)        │              │    (main.py)        │              │
│  │  ┌───────────────┐  │              │  ┌───────────────┐  │              │
│  │  │ Dashboard     │  │              │  │ Batch Process │  │              │
│  │  │ Upload Data   │  │              │  │ Automated Run │  │              │
│  │  │ Real-time     │  │              │  │ Script Exec   │  │              │
│  │  │ Predictions   │  │              │  └───────────────┘  │              │
│  │  │ Visualizations│  │              │                     │              │
│  │  └───────────────┘  │              │                     │              │
│  └──────────┬──────────┘              └──────────┬──────────┘              │
│             │                                    │                          │
└─────────────┼────────────────────────────────────┼──────────────────────────┘
              │                                    │
              └────────────────┬───────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │                                 │
┌─────────────▼───────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │              AMLComplianceSystem (aml_system.py)                       │ │
│  │                     Main System Orchestrator                            │ │
│  │                                                                          │ │
│  │  ┌────────────────────────────────────────────────────────────────┐   │ │
│  │  │  Core Functions:                                                │   │ │
│  │  │  • load_data()         - Initialize data across all modules    │   │ │
│  │  │  • run_complete_analysis() - Execute full fraud analysis       │   │ │
│  │  │  • predict_risk()      - Real-time risk prediction             │   │ │
│  │  │  • get_analysis_results() - Retrieve comprehensive results     │   │ │
│  │  └────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                          │ │
│  └───┬──────────┬──────────┬──────────┬──────────┬──────────────────────┘ │
│      │          │          │          │          │                          │
└──────┼──────────┼──────────┼──────────┼──────────┼──────────────────────────┘
       │          │          │          │          │
       │          │          │          │          │
┌──────▼──────────▼──────────▼──────────▼──────────▼──────────────────────────┐
│                          PROCESSING MODULES LAYER                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Module 1  │  │   Module 2  │  │   Module 3  │  │   Module 4  │       │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤       │
│  │    DATA     │  │  CUSTOMER   │  │  ANOMALY    │  │     ML      │       │
│  │  MANAGER    │  │  PROFILER   │  │  DETECTOR   │  │ PREDICTOR   │       │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤       │
│  │             │  │             │  │             │  │             │       │
│  │ Functions:  │  │ Functions:  │  │ Functions:  │  │ Functions:  │       │
│  │             │  │             │  │             │  │             │       │
│  │ • Load CSV  │  │ • Analyze   │  │ • Prepare   │  │ • Train     │       │
│  │ • Validate  │  │   customers │  │   features  │  │   models    │       │
│  │ • Generate  │  │ • Create    │  │ • Isolation │  │ • Random    │       │
│  │   synthetic │  │   profiles  │  │   Forest    │  │   Forest    │       │
│  │   data      │  │ • Calculate │  │ • Statisti- │  │ • Gradient  │       │
│  │ • Clean     │  │   risk      │  │   cal       │  │   Boosting  │       │
│  │   data      │  │   scores    │  │   methods   │  │ • Feature   │       │
│  │             │  │ • Risk      │  │ • Combine   │  │   engineer  │       │
│  │             │  │   classifi- │  │   results   │  │ • Predict   │       │
│  │             │  │   cation    │  │ • Anomaly   │  │ • Cross-val │       │
│  │             │  │             │  │   scoring   │  │ • Metrics   │       │
│  │             │  │             │  │             │  │ • Save/Load │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │                │               │
│         │                │                │                │               │
│  ┌──────▼────────────────▼────────────────▼────────────────▼──────┐       │
│  │                     Module 5: VISUALIZER                         │       │
│  │                    (visualizer.py)                               │       │
│  ├──────────────────────────────────────────────────────────────────┤       │
│  │  Functions:                                                      │       │
│  │  • generate_comprehensive_report()                               │       │
│  │  • create_transaction_heatmap()                                  │       │
│  │  • create_risk_distribution_chart()                              │       │
│  │  • create_network_graph()                                        │       │
│  │  • create_time_series_analysis()                                 │       │
│  │  • create_anomaly_plots()                                        │       │
│  │  • create_feature_importance_chart()                             │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                               │
└───────────────────────────────────┬───────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼───────────────────────────────────────────┐
│                            DATA STORAGE LAYER                                 │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │    INPUT     │  │    OUTPUT    │  │    MODELS    │  │    CONFIG    │    │
│  │    DATA      │  │    FILES     │  │    FOLDER    │  │    FILES     │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │              │  │              │  │              │  │              │    │
│  │ • CSV files  │  │ • customer_  │  │ • ml_model_  │  │ • config.py  │    │
│  │ • Google     │  │   profiles   │  │   [date].pkl │  │              │    │
│  │   Drive URLs │  │   .csv       │  │ • scaler_    │  │ Settings:    │    │
│  │ • Direct     │  │              │  │   [date].pkl │  │ • Paths      │    │
│  │   uploads    │  │ • detected_  │  │ • label_     │  │ • Thresholds │    │
│  │              │  │   anomalies  │  │   encoders_  │  │ • Model      │    │
│  │              │  │   .csv       │  │   [date].pkl │  │   params     │    │
│  │              │  │              │  │              │  │              │    │
│  │              │  │ • visualiza- │  │ (Pickle      │  │              │    │
│  │              │  │   tions      │  │  format)     │  │              │    │
│  │              │  │   (charts/   │  │              │  │              │    │
│  │              │  │   graphs)    │  │              │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│   User      │
│  Input      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. DATA INGESTION                                           │
│    • CSV File / Google Drive Link / File Upload            │
│    • Validation & Cleaning                                  │
│    • Synthetic Data Generation (if needed)                  │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CUSTOMER PROFILING                                       │
│    • Transaction Aggregation                                │
│    • Pattern Analysis                                       │
│    • Risk Score Calculation                                 │
│    • Risk Classification (Low/Medium/High/Critical)         │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ANOMALY DETECTION                                        │
│    • Feature Engineering                                    │
│    • Isolation Forest Algorithm                             │
│    • Statistical Methods                                    │
│    • Combined Anomaly Scoring                               │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ML PREDICTION                                            │
│    • Feature Preparation                                    │
│    • Model Training (RF, GradientBoosting)                  │
│    • Cross-validation                                       │
│    • Performance Metrics                                    │
│    • Model Persistence (Save to Disk)                       │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. VISUALIZATION & REPORTING                                │
│    • Comprehensive Analytics Report                         │
│    • Interactive Dashboards                                 │
│    • Network Graphs                                         │
│    • Time Series Analysis                                   │
│    • Feature Importance Charts                              │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. OUTPUT & RESULTS                                         │
│    • Customer Profiles CSV                                  │
│    • Detected Anomalies CSV                                 │
│    • Visual Reports                                         │
│    • Real-time Predictions                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Module Interaction Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SYSTEM INITIALIZATION                            │
│                                                                     │
│  User Request                                                       │
│       │                                                             │
│       ▼                                                             │
│  AMLComplianceSystem.__init__()                                    │
│       │                                                             │
│       ├──► Initialize all module references                         │
│       ├──► Set up system configuration                              │
│       └──► Display system ready message                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA LOADING PHASE                               │
│                                                                     │
│  aml_system.load_data(data_path)                                   │
│       │                                                             │
│       ├──► DataManager.load_data()                                 │
│       │    ├─ Validate CSV structure                               │
│       │    ├─ Handle Google Drive links                            │
│       │    └─ Generate synthetic data if needed                    │
│       │                                                             │
│       ├──► CustomerProfiler.__init__(df)                           │
│       ├──► AnomalyDetector.__init__(df)                            │
│       ├──► MLPredictor.__init__(df)                                │
│       └──► AMLVisualizer.__init__(df)                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 COMPLETE ANALYSIS EXECUTION                         │
│                                                                     │
│  aml_system.run_complete_analysis()                                │
│       │                                                             │
│       ├──► 1. CustomerProfiler.analyze_customers()                 │
│       │    ├─ Profile each account                                 │
│       │    ├─ Calculate risk scores                                │
│       │    ├─ Classify risk levels                                 │
│       │    └─ Save customer_profiles.csv                           │
│       │                                                             │
│       ├──► 2. AnomalyDetector.detect_anomalies()                   │
│       │    ├─ Prepare numerical features                           │
│       │    ├─ Run Isolation Forest                                 │
│       │    ├─ Run Statistical Detection                            │
│       │    ├─ Combine anomaly scores                               │
│       │    └─ Save detected_anomalies.csv                          │
│       │                                                             │
│       ├──► 3. MLPredictor.train_compliance_model()                 │
│       │    ├─ Feature engineering                                  │
│       │    ├─ Train multiple models                                │
│       │    ├─ Evaluate & select best model                         │
│       │    ├─ Analyze feature importance                           │
│       │    └─ Save model to models/ folder                         │
│       │                                                             │
│       └──► 4. AMLVisualizer.generate_comprehensive_report()        │
│            ├─ Create transaction heatmaps                          │
│            ├─ Generate risk distributions                          │
│            ├─ Build network graphs                                 │
│            ├─ Produce time series analysis                         │
│            └─ Create feature importance charts                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    REAL-TIME PREDICTION                             │
│                                                                     │
│  aml_system.predict_risk(new_transaction)                          │
│       │                                                             │
│       └──► MLPredictor.predict(new_transaction)                    │
│            ├─ Load saved model                                     │
│            ├─ Preprocess input features                            │
│            ├─ Generate risk prediction                             │
│            └─ Return risk score & classification                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Details

### 1. **Data Manager Module**
```
┌───────────────────────────────────────┐
│       DataManager                     │
├───────────────────────────────────────┤
│ Purpose:                              │
│ • Data loading and validation         │
│ • Synthetic data generation           │
│ • Data quality checks                 │
│                                       │
│ Key Methods:                          │
│ • load_data(path)                     │
│ • _generate_synthetic_data(n)         │
│ • _display_data_summary()             │
│                                       │
│ Input:                                │
│ • CSV files                           │
│ • Google Drive links                  │
│                                       │
│ Output:                               │
│ • Validated DataFrame                 │
└───────────────────────────────────────┘
```

### 2. **Customer Profiler Module**
```
┌───────────────────────────────────────┐
│     CustomerProfiler                  │
├───────────────────────────────────────┤
│ Purpose:                              │
│ • Customer behavior analysis          │
│ • Risk scoring                        │
│ • Pattern recognition                 │
│                                       │
│ Key Methods:                          │
│ • analyze_customers()                 │
│ • _create_customer_profile()          │
│ • _calculate_risk_scores()            │
│                                       │
│ Risk Factors:                         │
│ • Transaction volume                  │
│ • Cross-border activity               │
│ • Structuring indicators              │
│ • High-risk locations                 │
│ • Rapid transactions                  │
│                                       │
│ Output:                               │
│ • customer_profiles.csv               │
│ • Risk classifications                │
└───────────────────────────────────────┘
```

### 3. **Anomaly Detector Module**
```
┌───────────────────────────────────────┐
│      AnomalyDetector                  │
├───────────────────────────────────────┤
│ Purpose:                              │
│ • Identify unusual transactions       │
│ • Multi-algorithm approach            │
│ • Anomaly scoring                     │
│                                       │
│ Algorithms:                           │
│ • Isolation Forest                    │
│ • Statistical Methods (Z-score)       │
│                                       │
│ Key Methods:                          │
│ • detect_anomalies()                  │
│ • _isolation_forest_detection()       │
│ • _statistical_detection()            │
│ • _combine_anomaly_results()          │
│                                       │
│ Features Used:                        │
│ • Amount, Time                        │
│ • Location, Payment type              │
│ • Cross-border indicators             │
│                                       │
│ Output:                               │
│ • detected_anomalies.csv              │
│ • Anomaly scores                      │
└───────────────────────────────────────┘
```

### 4. **ML Predictor Module**
```
┌───────────────────────────────────────┐
│       MLPredictor                     │
├───────────────────────────────────────┤
│ Purpose:                              │
│ • Train predictive models             │
│ • Risk prediction                     │
│ • Model persistence                   │
│                                       │
│ Models:                               │
│ • Random Forest Classifier            │
│ • Gradient Boosting Classifier        │
│                                       │
│ Key Methods:                          │
│ • train_compliance_model()            │
│ • predict(transaction)                │
│ • save_model_to_disk()                │
│ • load_model_from_disk()              │
│ • _analyze_feature_importance()       │
│                                       │
│ Features:                             │
│ • Engineered features                 │
│ • Encoded categoricals                │
│ • Scaled numericals                   │
│                                       │
│ Metrics:                              │
│ • Accuracy, Precision, Recall         │
│ • F1-Score, ROC-AUC                   │
│                                       │
│ Output:                               │
│ • Trained model (.pkl)                │
│ • Scaler & encoders (.pkl)            │
│ • Performance metrics                 │
└───────────────────────────────────────┘
```

### 5. **Visualizer Module**
```
┌───────────────────────────────────────┐
│       AMLVisualizer                   │
├───────────────────────────────────────┤
│ Purpose:                              │
│ • Generate visual reports             │
│ • Interactive dashboards              │
│ • Data insights                       │
│                                       │
│ Visualizations:                       │
│ • Transaction heatmaps                │
│ • Risk distribution charts            │
│ • Network graphs                      │
│ • Time series analysis                │
│ • Feature importance plots            │
│ • Anomaly visualizations              │
│                                       │
│ Key Methods:                          │
│ • generate_comprehensive_report()     │
│ • create_transaction_heatmap()        │
│ • create_network_graph()              │
│ • create_time_series_analysis()       │
│                                       │
│ Libraries Used:                       │
│ • Matplotlib                          │
│ • Seaborn                             │
│ • Plotly (for web app)                │
│                                       │
│ Output:                               │
│ • Interactive charts                  │
│ • Static reports                      │
└───────────────────────────────────────┘
```

---

## 🔐 Security & Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT OPTIONS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────┐      ┌────────────────┐              │
│  │   LOCAL        │      │   HEROKU       │              │
│  │   DEPLOYMENT   │      │   DEPLOYMENT   │              │
│  ├────────────────┤      ├────────────────┤              │
│  │ • Python 3.8+  │      │ • Procfile     │              │
│  │ • Virtual env  │      │ • runtime.txt  │              │
│  │ • CLI/Web      │      │ • Web process  │              │
│  └────────────────┘      └────────────────┘              │
│                                                             │
│  ┌────────────────┐      ┌────────────────┐              │
│  │   DOCKER       │      │   CLOUD        │              │
│  │   DEPLOYMENT   │      │   DEPLOYMENT   │              │
│  ├────────────────┤      ├────────────────┤              │
│  │ • Dockerfile   │      │ • AWS/Azure    │              │
│  │ • docker-      │      │ • GCP          │              │
│  │   compose.yml  │      │ • Scalable     │              │
│  └────────────────┘      └────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Frontend:                                                   │
│ • Streamlit (Web Interface)                                 │
│ • HTML/CSS (Custom styling)                                 │
│ • Plotly (Interactive charts)                               │
│                                                             │
│ Backend:                                                    │
│ • Python 3.8+                                               │
│ • Pandas (Data manipulation)                                │
│ • NumPy (Numerical operations)                              │
│                                                             │
│ Machine Learning:                                           │
│ • scikit-learn (Models & preprocessing)                     │
│ • Random Forest                                             │
│ • Gradient Boosting                                         │
│ • Isolation Forest                                          │
│                                                             │
│ Visualization:                                              │
│ • Matplotlib                                                │
│ • Seaborn                                                   │
│ • Plotly                                                    │
│                                                             │
│ Model Persistence:                                          │
│ • Pickle / Joblib                                           │
│                                                             │
│ Deployment:                                                 │
│ • Docker                                                    │
│ • Heroku                                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Execution Workflow

### **CLI Execution (main.py)**
```
1. User runs: python main.py
   │
2. Initialize AMLComplianceSystem
   │
3. Load transaction data
   │
4. Run complete analysis
   ├─ Customer profiling
   ├─ Anomaly detection
   ├─ ML model training
   └─ Visualization
   │
5. Generate reports
   │
6. Predict risk for new transactions
   │
7. Display results to console
```

### **Web App Execution (app.py)**
```
1. User runs: streamlit run app.py
   │
2. Web interface loads
   │
3. User interactions:
   ├─ Upload data / Use sample data
   ├─ View dashboard
   ├─ Analyze transactions
   ├─ Real-time predictions
   └─ Download reports
   │
4. Background processing:
   ├─ Run analysis on demand
   ├─ Generate visualizations
   └─ Update results dynamically
```

---

## 🔍 Key Features Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    FEATURE ARCHITECTURE                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ 1. CUSTOMER RISK PROFILING                                     │
│    ├─ Transaction aggregation                                  │
│    ├─ Risk score calculation                                   │
│    ├─ Multi-factor analysis                                    │
│    └─ Risk classification (Low/Medium/High/Critical)           │
│                                                                │
│ 2. ANOMALY DETECTION                                           │
│    ├─ Isolation Forest algorithm                               │
│    ├─ Statistical outlier detection                            │
│    ├─ Combined anomaly scoring                                 │
│    └─ Confidence levels                                        │
│                                                                │
│ 3. MACHINE LEARNING PREDICTION                                 │
│    ├─ Ensemble models (RF + GB)                                │
│    ├─ Feature engineering                                      │
│    ├─ Cross-validation                                         │
│    ├─ Model persistence                                        │
│    └─ Real-time prediction                                     │
│                                                                │
│ 4. COMPREHENSIVE REPORTING                                     │
│    ├─ Interactive dashboards                                   │
│    ├─ Network visualization                                    │
│    ├─ Time series analysis                                     │
│    ├─ Feature importance                                       │
│    └─ Export capabilities                                      │
│                                                                │
│ 5. MODEL PERSISTENCE                                           │
│    ├─ Save trained models                                      │
│    ├─ Load pre-trained models                                  │
│    ├─ Version management                                       │
│    └─ Incremental updates                                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 System Metrics & KPIs

```
┌────────────────────────────────────────────────────────────────┐
│                    KEY PERFORMANCE INDICATORS                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ Model Performance:                                             │
│ • Accuracy: ML model classification accuracy                   │
│ • Precision: True positive rate                                │
│ • Recall: Sensitivity to fraud detection                       │
│ • F1-Score: Harmonic mean of precision and recall              │
│                                                                │
│ System Metrics:                                                │
│ • Processing speed: Transactions per second                    │
│ • Model training time: Time to train models                    │
│ • Prediction latency: Response time for predictions            │
│                                                                │
│ Business Metrics:                                              │
│ • False positive rate: Legitimate transactions flagged         │
│ • False negative rate: Missed fraud cases                      │
│ • Detection rate: % of fraud caught                            │
│ • Customer risk distribution: Risk level breakdown             │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Summary

This Fraud Management System employs a **modular, layered architecture** with:

1. **User Interface Layer**: CLI and Web interfaces for different use cases
2. **Orchestration Layer**: Central system coordinator (AMLComplianceSystem)
3. **Processing Layer**: Five specialized modules for specific tasks
4. **Data Layer**: Persistent storage for inputs, outputs, and models

The system follows **best practices** including:
- ✅ Separation of concerns
- ✅ Modular design
- ✅ Scalability
- ✅ Model persistence
- ✅ Comprehensive logging
- ✅ Error handling
- ✅ Flexible deployment options

Each module is **independent yet integrated**, allowing for easy maintenance, testing, and future enhancements.
