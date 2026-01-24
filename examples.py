"""
"""Usage Examples for Fraud Management System
=========================================

This file contains practical examples of how to use the system.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aml_system import AMLComplianceSystem
from modules.data_manager import DataManager
from modules.customer_profiler import CustomerProfiler
from modules.anomaly_detector import AnomalyDetector
from modules.ml_predictor import MLPredictor
from modules.visualizer import AMLVisualizer


# =============================================================================
# EXAMPLE 1: Quick Start - Complete Analysis
# =============================================================================

def example_1_quick_start():
    """Run complete analysis with default settings"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Quick Start - Complete Analysis")
    print("="*60)
    
    # Initialize and run
    system = AMLComplianceSystem()
    
    # Load data (will generate synthetic if path is None)
    system.load_data(None)  # Uses synthetic data
    
    # Run complete analysis
    results = system.run_complete_analysis()
    
    print("\n✓ Analysis complete!")
    print(f"Analyzed {len(results['customer_profiles'])} customers")
    print(f"Detected {len(results['anomalies'])} total transactions")


# =============================================================================
# EXAMPLE 2: Load Custom Data
# =============================================================================

def example_2_custom_data():
    """Load data from a custom CSV file"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Load Custom Data")
    print("="*60)
    
    system = AMLComplianceSystem()
    
    # Option 1: Local file
    # system.load_data('data/my_transactions.csv')
    
    # Option 2: Google Drive (will be converted automatically)
    data_path = 'https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing'
    
    # Option 3: Use synthetic data
    system.load_data(None)
    
    print("✓ Data loaded successfully!")


# =============================================================================
# EXAMPLE 3: Risk Prediction for Single Transaction
# =============================================================================

def example_3_single_prediction():
    """Predict risk for a single transaction"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Single Transaction Risk Prediction")
    print("="*60)
    
    # Initialize and train model
    system = AMLComplianceSystem()
    system.load_data(None)
    system.run_complete_analysis()
    
    # Define a high-risk transaction
    high_risk_txn = {
        'Time': '02:30:00',  # Late night
        'Date': '2024-06-15',
        'Sender_account': 'ACC0001',
        'Receiver_account': 'ACC0002',
        'Amount': 9500,  # Just under $10k threshold
        'Payment_currency': 'USD',
        'Received_currency': 'AED',  # Currency conversion
        'Sender_bank_location': 'US-NY',
        'Receiver_bank_location': 'AE-DXB',  # High-risk location
        'Payment_type': 'Wire'
    }
    
    # Predict risk
    risk = system.predict_compliance_risk(high_risk_txn)
    
    print("\nTransaction Analysis:")
    print(f"Amount: ${high_risk_txn['Amount']:,}")
    print(f"Route: {high_risk_txn['Sender_bank_location']} → {high_risk_txn['Receiver_bank_location']}")
    print(f"\nRisk Assessment:")
    print(f"Risk Score: {risk['risk_score']:.2f}%")
    print(f"Classification: {risk['risk_label']}")
    print(f"Probability: {risk['risk_probability']:.4f}")


# =============================================================================
# EXAMPLE 4: Batch Prediction
# =============================================================================

def example_4_batch_prediction():
    """Predict risk for multiple transactions"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Batch Transaction Predictions")
    print("="*60)
    
    import pandas as pd
    
    # Initialize system
    system = AMLComplianceSystem()
    system.load_data(None)
    system.run_complete_analysis()
    
    # Create batch of transactions
    transactions = [
        {'Time': '14:30:00', 'Date': '2024-06-15', 'Sender_account': 'ACC0001',
         'Receiver_account': 'ACC0002', 'Amount': 2500, 'Payment_currency': 'USD',
         'Received_currency': 'USD', 'Sender_bank_location': 'US-NY',
         'Receiver_bank_location': 'US-NY', 'Payment_type': 'ACH'},
        
        {'Time': '02:30:00', 'Date': '2024-06-15', 'Sender_account': 'ACC0003',
         'Receiver_account': 'ACC0004', 'Amount': 9800, 'Payment_currency': 'USD',
         'Received_currency': 'AED', 'Sender_bank_location': 'US-NY',
         'Receiver_bank_location': 'AE-DXB', 'Payment_type': 'Wire'},
        
        {'Time': '16:45:00', 'Date': '2024-06-15', 'Sender_account': 'ACC0005',
         'Receiver_account': 'ACC0006', 'Amount': 150000, 'Payment_currency': 'USD',
         'Received_currency': 'CHF', 'Sender_bank_location': 'UK-LDN',
         'Receiver_bank_location': 'CH-ZRH', 'Payment_type': 'Wire'}
    ]
    
    # Predict for each
    print("\nBatch Predictions:")
    for i, txn in enumerate(transactions, 1):
        risk = system.predict_compliance_risk(txn)
        print(f"\nTransaction {i}:")
        print(f"  Amount: ${txn['Amount']:,}")
        print(f"  Route: {txn['Sender_bank_location']} → {txn['Receiver_bank_location']}")
        print(f"  Risk Score: {risk['risk_score']:.2f}% - {risk['risk_label']}")


# =============================================================================
# EXAMPLE 5: Customer Risk Profile Analysis
# =============================================================================

def example_5_customer_analysis():
    """Analyze specific customer risk profile"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Customer Risk Profile Analysis")
    print("="*60)
    
    # Initialize system
    system = AMLComplianceSystem()
    system.load_data(None)
    results = system.run_complete_analysis()
    
    # Get high-risk customers
    profiles = results['customer_profiles']
    high_risk_customers = profiles[profiles['risk_classification'] == 'HIGH']
    
    print(f"\n📊 Found {len(high_risk_customers)} high-risk customers")
    
    # Analyze first high-risk customer
    if len(high_risk_customers) > 0:
        account_id = high_risk_customers.iloc[0]['account']
        profile = system.get_customer_risk_profile(account_id)
        
        print(f"\nDetailed Profile for {account_id}:")
        print(f"  Risk Score: {profile['risk_score']:.2f}")
        print(f"  Total Transactions: {profile['total_transactions']}")
        print(f"  Suspicious Transactions: {profile['suspicious_transactions']}")
        print(f"  Total Volume: ${profile['total_volume']:,.2f}")
        print(f"  Cross-border Count: {profile['cross_border_count']}")
        print(f"  High-risk Countries: {profile['high_risk_countries']}")


# =============================================================================
# EXAMPLE 6: Using Individual Modules
# =============================================================================

def example_6_individual_modules():
    """Use modules independently"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Using Individual Modules")
    print("="*60)
    
    # 1. Load data
    print("\n1. Loading data...")
    dm = DataManager()
    df = dm.load_data(None)
    
    # 2. Profile customers
    print("\n2. Profiling customers...")
    profiler = CustomerProfiler(df)
    profiles = profiler.analyze_customers(save_results=False)
    
    # 3. Detect anomalies
    print("\n3. Detecting anomalies...")
    detector = AnomalyDetector(df)
    anomalies = detector.detect_anomalies(save_results=False)
    
    # 4. Train ML model
    print("\n4. Training ML model...")
    predictor = MLPredictor(df)
    model = predictor.train_compliance_model()
    
    print("\n✓ All modules executed independently!")


# =============================================================================
# EXAMPLE 7: Custom Risk Threshold Analysis
# =============================================================================

def example_7_custom_thresholds():
    """Analyze data with custom risk thresholds"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Custom Risk Threshold Analysis")
    print("="*60)
    
    # Load and analyze
    system = AMLComplianceSystem()
    system.load_data(None)
    results = system.run_complete_analysis()
    
    profiles = results['customer_profiles']
    
    # Custom thresholds
    critical_threshold = 80
    elevated_threshold = 60
    
    critical = profiles[profiles['risk_score'] >= critical_threshold]
    elevated = profiles[(profiles['risk_score'] >= elevated_threshold) & 
                       (profiles['risk_score'] < critical_threshold)]
    normal = profiles[profiles['risk_score'] < elevated_threshold]
    
    print(f"\nCustom Risk Analysis:")
    print(f"  Critical Risk (≥{critical_threshold}): {len(critical)} customers")
    print(f"  Elevated Risk (≥{elevated_threshold}): {len(elevated)} customers")
    print(f"  Normal Risk (<{elevated_threshold}): {len(normal)} customers")


# =============================================================================
# EXAMPLE 8: Export and Report Generation
# =============================================================================

def example_8_export_reports():
    """Generate and export various reports"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Export and Report Generation")
    print("="*60)
    
    system = AMLComplianceSystem()
    system.load_data(None)
    results = system.run_complete_analysis()  # Already saves CSV files
    
    # Generate summary
    summary = system.generate_summary_report()
    
    print("\n📄 Generated Reports:")
    print("  ✓ output/customer_profiles.csv")
    print("  ✓ output/detected_anomalies.csv")
    print("  ✓ output/dashboard.png")
    print("  ✓ output/detailed_analysis.png")
    print("  ✓ output/customer_profiles.png")
    
    print("\n📊 Executive Summary:")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
        elif isinstance(value, int):
            print(f"  {key.replace('_', ' ').title()}: {value:,}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")


# =============================================================================
# EXAMPLE 9: Visualization Only
# =============================================================================

def example_9_visualization():
    """Generate visualizations without full analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Visualization Only")
    print("="*60)
    
    # Load data
    dm = DataManager()
    df = dm.load_data(None)
    
    # Create visualizer
    viz = AMLVisualizer(df)
    
    # Generate dashboard (without profiles/anomalies)
    viz.create_comprehensive_dashboard()
    
    print("\n✓ Basic dashboard generated!")


# =============================================================================
# EXAMPLE 10: Complete Real-World Workflow
# =============================================================================

def example_10_complete_workflow():
    """Complete workflow from data to prediction"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Complete Real-World Workflow")
    print("="*60)
    
    # Step 1: Initialize system
    print("\n📋 Step 1: Initializing system...")
    system = AMLComplianceSystem()
    
    # Step 2: Load production data
    print("\n📂 Step 2: Loading data...")
    system.load_data(None)  # Replace with actual data path
    
    # Step 3: Run comprehensive analysis
    print("\n🔍 Step 3: Running analysis...")
    results = system.run_complete_analysis()
    
    # Step 4: Review high-risk customers
    print("\n🚨 Step 4: Reviewing high-risk customers...")
    profiles = results['customer_profiles']
    high_risk = profiles[profiles['risk_classification'] == 'HIGH']
    print(f"Found {len(high_risk)} high-risk customers requiring review")
    
    # Step 5: Check anomalies
    print("\n🔍 Step 5: Checking anomalies...")
    anomalies = results['anomalies']
    flagged = anomalies[anomalies['composite_anomaly'] == 1]
    print(f"Detected {len(flagged)} anomalous transactions")
    
    # Step 6: Real-time monitoring
    print("\n📡 Step 6: Real-time transaction monitoring...")
    new_transactions = [
        {'Time': '15:30:00', 'Date': '2024-06-16', 'Sender_account': 'ACC0010',
         'Receiver_account': 'ACC0020', 'Amount': 5000, 'Payment_currency': 'USD',
         'Received_currency': 'USD', 'Sender_bank_location': 'US-NY',
         'Receiver_bank_location': 'US-NY', 'Payment_type': 'Wire'}
    ]
    
    for txn in new_transactions:
        risk = system.predict_compliance_risk(txn)
        if risk['risk_score'] > 70:
            print(f"⚠ HIGH RISK ALERT: Transaction flagged - Score: {risk['risk_score']:.2f}%")
        else:
            print(f"✓ Transaction cleared - Score: {risk['risk_score']:.2f}%")
    
    # Step 7: Generate reports for management
    print("\n📊 Step 7: Generating executive report...")
    summary = system.generate_summary_report()
    print("Report generated successfully!")
    
    print("\n✅ Workflow complete!")


# =============================================================================
# MAIN - Run Examples
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("FRAUD MANAGEMENT SYSTEM - USAGE EXAMPLES")
    print("="*60)
    
    # Uncomment the example you want to run:
    
    # example_1_quick_start()
    # example_2_custom_data()
    # example_3_single_prediction()
    # example_4_batch_prediction()
    # example_5_customer_analysis()
    # example_6_individual_modules()
    # example_7_custom_thresholds()
    # example_8_export_reports()
    # example_9_visualization()
    example_10_complete_workflow()
    
    print("\n" + "="*60)
    print("For more examples, uncomment other functions in this file")
    print("="*60)
