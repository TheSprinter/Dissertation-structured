# Fraud Management System

A comprehensive fraud detection and management system using AI/ML techniques for fraud detection, risk assessment, and compliance monitoring. The system provides both a **Streamlit web application** and a **Python/CLI batch pipeline**, and is developed as part of an MTech AIML dissertation at BITS Pilani.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quickstart – Streamlit Web App](#quickstart--streamlit-web-app)
- [Quickstart – CLI / Batch Pipeline](#quickstart--cli--batch-pipeline)
- [Docker & Cloud Deployment](#docker--cloud-deployment)
- [Core Modules](#core-modules)
- [Output](#output)
- [Configuration](#configuration)
- [Data Format](#data-format)
- [Further Documentation](#further-documentation)
- [Academic Context](#academic-context)
- [Contact](#contact)

## Features

- **Customer Risk Profiling** – Comprehensive customer-level risk assessment based on transaction behaviour
- **Anomaly Detection** – Multi-algorithm approach using Isolation Forest and statistical methods
- **Supervised ML Models** – Predictive models for fraud/compliance risk forecasting
- **Model Persistence** – Save and load trained models using pickle/joblib
- **Dashboards & Reports** – Visual dashboards and analytical plots for investigation
- **Real-time Prediction** – Risk assessment for new transactions via web UI or Python API

## Technologies Used

### Data Processing & Analysis
- pandas (≥ 2.0.0)
- numpy (≥ 1.24.0)
- python-dateutil (≥ 2.8.0)

### Machine Learning
- scikit-learn (≥ 1.3.0)
- joblib (≥ 1.3.0)

### Visualization
- matplotlib (≥ 3.7.0)
- seaborn (≥ 0.12.0)
- Pillow (≥ 10.0.0)

### Web Framework
- Streamlit (≥ 1.30.0)

### Deployment
- Python 3.12 (Docker base image) – local/runtime environment
- Docker & docker-compose – containerization and orchestration

Optional deep learning libraries (TensorFlow / Keras) are listed in `requirements.txt` but commented out by default.

## Architecture Overview

At a high level, the system is organised into three layers:

- **Interface layer** – Streamlit web UI (`app.py`) and optional CLI scripts (`main.py`, `examples.py`).
- **Orchestration layer** – `AMLComplianceSystem` in `src/aml_system.py` coordinates data loading, profiling, anomaly detection, model training, prediction, and report generation.
- **Module layer** – Independent modules under `src/modules/` handle data management, profiling, anomaly detection, ML models, and visualisation.

For detailed diagrams and data-flow descriptions, see:

- `ARCHITECTURE_DIAGRAM.md` – architecture and data flow diagrams
- `STRUCTURE.md` – detailed description of modules and their responsibilities

## Project Structure

Root directory (simplified):

```text
.
├── app.py # Streamlit web application entry point
├── main.py # CLI/batch analysis entry point
├── examples.py # Example usage patterns for developers
├── generate_report.py # Automated dissertation report (DOCX) generator
├── generate_presentation.py # Automated presentation (PPTX) generator
├── requirements.txt # Python dependencies
├── Dockerfile # Docker image definition (Streamlit app)
├── docker-compose.yml # Docker Compose service for the web app
├── MODEL_PERSISTENCE.md # Detailed model persistence guide
├── WEBAPP_README.md # Detailed Streamlit web app usage
├── DEPLOYMENT.md # Deployment options (Docker, cloud, etc.)
├── STRUCTURE.md # Full project structure and module details
├── ARCHITECTURE_DIAGRAM.md # Architecture and data flow diagrams
│
├── src/
│ ├── __init__.py
│ ├── config.py # Global configuration (thresholds, paths, etc.)
│ ├── aml_system.py # AMLComplianceSystem orchestrator
│ └── modules/
│ ├── __init__.py
│ ├── data_manager.py # Data loading, validation, synthetic data
│ ├── customer_profiler.py # Customer risk profiling
│ ├── anomaly_detector.py # Anomaly detection logic
│ ├── ml_predictor.py # ML training and prediction
│ └── visualizer.py # Visualisation and reporting
│
├── models/ # Saved ML models and related artefacts
├── output/ # Generated outputs (CSV, plots, reports)
└── tests/ # Unit tests for core components
```

For a more exhaustive tree and explanation of every directory, see `STRUCTURE.md`.

## Installation

1. **Clone the repository**

    ```bash
    git clone <repo-url>
    cd Dissertation-structured
    ```

2. **(Optional) Create a virtual environment**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    # source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Quickstart – Streamlit Web App

The Streamlit web application is the primary interface for interactive analysis.

### Option 1 – Start script (recommended)

**Windows:**

```bash
start_app.bat
```

**Linux / Mac:**

```bash
chmod +x start_app.sh
./start_app.sh
```

Then open a browser and visit: `http://localhost:8501`.

### Option 2 – Manual start

```bash
pip install -r requirements.txt # if not already installed
streamlit run app.py
```

Key pages in the web app include:

- **Home** – Overview of system capabilities
- **Data Upload & Analysis** – Load data (CSV or sample) and run the full pipeline
- **Transaction Risk Prediction** – Real-time risk scoring for single transactions
- **Customer Risk Profiles** – Explore per-customer risk profiles
- **Dashboard & Reports** – Visual dashboards and downloadable analysis artefacts

For screenshots, troubleshooting, and more detailed instructions, see `WEBAPP_README.md`.

## Quickstart – CLI / Batch Pipeline

You can also run the full analysis pipeline from the command line.

### Basic batch run

```bash
python main.py
```

This will:

- Load transaction data (from a configured path or generate synthetic data if unavailable)
- Run customer profiling, anomaly detection, and ML-based fraud prediction
- Generate CSV outputs and plots into the `output/` directory

### Programmatic usage (Python API)

```python
from src.aml_system import AMLComplianceSystem

aml_system = AMLComplianceSystem()

# Load your own CSV (must follow the current schema)
aml_system.load_data("path/to/transactions.csv")

# Run the complete analysis pipeline
results = aml_system.run_complete_analysis(save_results=True)

# Predict risk for a new transaction (schema-aligned dictionary)
example_txn = {
     "transaction_id": "TXN0000001",
     "customer_id": "CUST00001",
     "transaction_amount": 9500.0,
     "transaction_date": "2024-06-15",
     "transaction_time": "14:30:00",
     "merchant_category": "Electronics",
     "merchant_id": "MERCH0001",
     "payment_method": "Credit Card",
     "transaction_type": "Purchase",
     "location": "US",
     "device_type": "Mobile",
     "ip_country": "US",
     "card_type": "Visa",
     # ... additional optional fields as in data_manager.py ...
}

risk = aml_system.predict_compliance_risk(example_txn)
print(risk)
```

More end-to-end examples are available in `examples.py` and `QUICKSTART.md`.

## Docker & Cloud Deployment

### Docker (local)

Build and run the Streamlit app in a container:

```bash
docker build -t aml-app .
docker run -p 8501:8501 aml-app
```

Or using Docker Compose:

```bash
docker-compose up -d
```

The app will be available at `http://localhost:8501`.

### Cloud deployment

The project includes guidance for deploying to:

- Streamlit Cloud
- Heroku
- Azure App Service
- AWS EC2 (and similar environments)

For step-by-step instructions and configuration details, see `DEPLOYMENT.md`.

## Core Modules

All core modules live under `src/modules/` and are orchestrated by `AMLComplianceSystem`.

### Data Manager (`data_manager.py`)

- Loads transaction data from CSV files or Google Drive links
- Validates dataset against the expected schema
- Generates realistic synthetic data when required columns are missing
- Provides rich data summaries (volume, date range, fraud ratio)

### Customer Profiler (`customer_profiler.py`)

- Analyses customer-level behaviour and transaction history
- Computes risk scores (0–100) per customer
- Classifies customers into HIGH, MEDIUM, or LOW risk

### Anomaly Detector (`anomaly_detector.py`)

- Uses Isolation Forest and statistical methods to detect anomalies
- Flags unusual transaction patterns and temporal anomalies

### ML Predictor (`ml_predictor.py`)

- Trains supervised models (e.g., Random Forest, Gradient Boosting)
- Performs feature engineering and model evaluation
- Provides prediction APIs for single or batch transactions
- Handles model persistence (save/load models with joblib/pickle)

### Visualizer (`visualizer.py`)

- Builds dashboards and detailed analysis plots
- Generates visual artefacts for investigation and reporting

For deeper, implementation-level details, see `STRUCTURE.md` and `ARCHITECTURE_DIAGRAM.md`.

## Output

The system writes outputs into the `output/` directory. Typical artefacts include:

1. `customer_profiles.csv` – Per-customer profiles and risk scores
2. `detected_anomalies.csv` – List of anomalous transactions and associated scores
3. Dashboard and analysis images (`dashboard.png`, `detailed_analysis.png`, etc.)
4. Additional plots and summaries used in the dissertation

These outputs are consumed by the Streamlit web app and can also be used directly in analysis or reporting.

## Configuration

Global configuration is centralised in `src/config.py`. You can adjust, for example:

- Risk thresholds (e.g., `HIGH_RISK_THRESHOLD`, `MEDIUM_RISK_THRESHOLD`)
- Anomaly detection settings (e.g., `CONTAMINATION_RATE` for Isolation Forest)
- Output directory paths
- Visualisation and reporting options

Both the CLI and Streamlit web app honour these shared settings.

## Data Format

The current pipeline expects a **transaction-centric schema**. Key required columns (see `DataManager` in `src/modules/data_manager.py`) include:

- `transaction_id`
- `customer_id`
- `transaction_amount`
- `transaction_date` (YYYY-MM-DD)
- `transaction_time` (HH:MM:SS)
- `merchant_id`
- `merchant_category`
- `payment_method`
- `transaction_type`
- `card_type`
- `location`
- `device_type`
- `ip_country`
- `is_fraud` (0 or 1 – label, if available)

Additional optional fields (billing/shipping countries, verification flags, behavioural features, etc.) are automatically handled and used for richer modelling. If your CSV is missing some of the required columns, the system will warn you and, if necessary, fall back to generating synthetic data for demonstration.

> Note: Older documentation and examples using columns like `Sender_account`, `Receiver_account`, `Is_laundering`, and `Laundering_type` refer to a previous version of the dataset. New experiments should follow the schema implemented in `data_manager.py`.

## Further Documentation

- `WEBAPP_README.md` – Detailed Streamlit web app usage and screenshots
- `DEPLOYMENT.md` – Docker and cloud deployment instructions
- `STRUCTURE.md` – Full project structure and module internals
- `ARCHITECTURE_DIAGRAM.md` – Architecture and data flow diagrams
- `MODEL_PERSISTENCE.md` – Model saving/loading and file layout in `models/`
- `QUICKSTART.md` – Additional developer-focused quickstart and usage patterns
- `PROJECT_SUMMARY.md` – Narrative summary of the refactoring and project evolution

## Academic Context

This project is submitted as part of the **Final Semester Dissertation Project** for the **Master of Technology (MTech) in Artificial Intelligence and Machine Learning (AIML)** degree at **Birla Institute of Technology and Science (BITS), Pilani)**.

- **Institution**: BITS Pilani
- **Program**: MTech in AIML
- **Project Type**: Dissertation Project
- **Academic Year**: 2025–2026

The dissertation investigates the design of a modular, explainable fraud management system that combines anomaly detection, supervised learning, and interactive analytics via a web-based interface.

## Contact

For academic inquiries or questions about this dissertation project, please contact through the appropriate BITS Pilani academic channels.

---

**Note**: This system is designed for academic research and demonstration purposes as part of an MTech dissertation. For production use, ensure compliance with local regulations, integrate with enterprise observability, and conduct thorough testing and validation.
