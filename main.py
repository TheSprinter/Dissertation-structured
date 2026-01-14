"""
Main Execution Script
=====================

Run the complete Fraud Management System analysis.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aml_system import AMLComplianceSystem


def main():
    """Main execution function"""
    
    print("="*80)
    print("FRAUD MANAGEMENT SYSTEM - MAIN EXECUTION")
    print("="*80)
    
    # Initialize the system
    aml_system = AMLComplianceSystem()
    
    # Load data (use your data path or synthetic data will be generated)
    data_path = 'https://drive.google.com/file/d/1AxCyxmfbAMgPMhxQAnyWcieCaDMfhCMQ/view?usp=sharing'
    
    print("\n📂 Loading transaction data...")
    aml_system.load_data(data_path)
    
    # Run complete analysis
    print("\n🔄 Starting complete fraud analysis...")
    analysis_results = aml_system.run_complete_analysis(save_results=True)
    
    # Example: Predict risk for a new transaction
    print("\n" + "="*80)
    print("EXAMPLE: PREDICTING RISK FOR NEW TRANSACTION")
    print("="*80)
    
    new_transaction = {
        'Time': '02:30:00',
        'Date': '2024-06-15',
        'Sender_account': 'ACC0001',
        'Receiver_account': 'ACC0002',
        'Amount': 9500,
        'Payment_currency': 'USD',
        'Received_currency': 'AED',
        'Sender_bank_location': 'US-NY',
        'Receiver_bank_location': 'AE-DXB',
        'Payment_type': 'Wire'
    }
    
    try:
        prediction = aml_system.predict_compliance_risk(new_transaction)
        print("\nTransaction Details:")
        for key, value in new_transaction.items():
            print(f"   {key}: {value}")
        print("\nRisk Assessment:")
        for key, value in prediction.items():
            print(f"   {key}: {value}")
    except Exception as e:
        print(f"Prediction error: {e}")
    
    # Generate summary report
    print("\n" + "="*80)
    print("EXECUTIVE SUMMARY")
    print("="*80)
    
    summary = aml_system.generate_summary_report()
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        elif isinstance(value, int):
            print(f"{key.replace('_', ' ').title()}: {value:,}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE!")
    print("="*80)
    print("\n📁 Generated Files:")
    print("   • output/customer_profiles.csv")
    print("   • output/detected_anomalies.csv")
    print("   • output/dashboard.png")
    print("   • output/detailed_analysis.png")
    print("   • output/customer_profiles.png")


if __name__ == "__main__":
    main()
