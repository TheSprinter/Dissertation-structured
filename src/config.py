"""
Configuration Module
====================

Configuration settings for the AML Compliance System.
"""

# System Settings
SYSTEM_NAME = "AML Compliance AI System"
VERSION = "1.0.0"

# Data Settings
DATA_PATH = None  # Set to your data file path
SYNTHETIC_DATA_SIZE = 1000

# Model Settings
TEST_SIZE = 0.3
RANDOM_STATE = 42
CONTAMINATION_RATE = 0.1

# Risk Thresholds
HIGH_RISK_THRESHOLD = 70
MEDIUM_RISK_THRESHOLD = 40

# High-risk Locations
HIGH_RISK_LOCATIONS = ['AE-DXB', 'HK-HKG']

# Output Settings
SAVE_RESULTS = True
OUTPUT_DIR = 'output/'

# Visualization Settings
FIGURE_DPI = 300
DASHBOARD_FIGSIZE = (18, 12)

# Anomaly Detection Settings
ZSCORE_THRESHOLD = 3
EARLY_HOUR_THRESHOLD = 300  # 5 AM in minutes
LATE_HOUR_THRESHOLD = 1320  # 10 PM in minutes

# Structuring Detection
STRUCTURING_MIN = 9000
STRUCTURING_MAX = 10000
