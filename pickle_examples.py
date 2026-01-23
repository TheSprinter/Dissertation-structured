"""
Example: Using Pickle for Model Persistence
============================================

This script demonstrates how to use pickle functionality
in the Fraud Management System.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aml_system import AMLComplianceSystem


def example_train_and_save():
    """Example 1: Train a model and save it"""
    print("="*80)
    print("EXAMPLE 1: TRAIN AND SAVE MODEL")
    print("="*80)
    
    # Initialize system
    aml_system = AMLComplianceSystem()
    
    # Load data (will use synthetic data if path not provided)
    print("\n📂 Loading data...")
    aml_system.load_data()
    
    # Run analysis and train model (model will be saved automatically)
    print("\n🤖 Training model...")
    results = aml_system.run_complete_analysis(save_results=True, save_model=True)
    
    print("\n✅ Model trained and saved successfully!")
    print(f"Model saved to: models/ml_package.pkl")
    
    return aml_system


def example_load_and_predict():
    """Example 2: Load a pre-trained model and make predictions"""
    print("\n" + "="*80)
    print("EXAMPLE 2: LOAD PRE-TRAINED MODEL AND PREDICT")
    print("="*80)
    
    # Initialize system
    aml_system = AMLComplianceSystem()
    
    # Load data first (needed for preprocessing)
    print("\n📂 Loading data...")
    aml_system.load_data()
    
    # Load pre-trained model
    print("\n📂 Loading pre-trained model...")
    success = aml_system.load_pretrained_model()
    
    if success:
        print("\n✅ Model loaded successfully!")
        
        # Make a prediction on a new transaction
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
            'Payment_type': 'Wire Transfer'
        }
        
        print("\n🔍 Predicting risk for new transaction...")
        prediction = aml_system.predict_compliance_risk(new_transaction)
        
        print("\n" + "="*80)
        print("PREDICTION RESULTS")
        print("="*80)
        print(f"Risk Label: {prediction['risk_label']}")
        print(f"Risk Probability: {prediction['risk_probability']:.2%}")
        print(f"Risk Score: {prediction['risk_score']:.2f}/100")
    else:
        print("\n❌ Failed to load model. Please train a model first.")
    
    return aml_system


def example_list_models():
    """Example 3: List all available saved models"""
    print("\n" + "="*80)
    print("EXAMPLE 3: LIST SAVED MODELS")
    print("="*80)
    
    aml_system = AMLComplianceSystem()
    models = aml_system.list_available_models()
    
    return models


def example_save_with_custom_name():
    """Example 4: Save model with custom name"""
    print("\n" + "="*80)
    print("EXAMPLE 4: SAVE MODEL WITH CUSTOM NAME")
    print("="*80)
    
    # Initialize and train
    aml_system = AMLComplianceSystem()
    aml_system.load_data()
    
    print("\n🤖 Training model...")
    aml_system.run_complete_analysis(save_results=False, save_model=False)
    
    # Save with custom name
    custom_path = "models/fraud_model_v1.pkl"
    print(f"\n💾 Saving model to {custom_path}...")
    aml_system.save_trained_model(custom_path)
    
    print(f"\n✅ Model saved to {custom_path}")
    
    return aml_system


def main():
    """Main execution"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║         FRAUD MANAGEMENT SYSTEM - PICKLE EXAMPLES                 ║
    ║                                                                   ║
    ║  Demonstrates model persistence using pickle/joblib              ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    print("\nChoose an example to run:")
    print("1. Train and save a new model")
    print("2. Load pre-trained model and make predictions")
    print("3. List all saved models")
    print("4. Save model with custom name")
    print("5. Run all examples")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == '1':
        example_train_and_save()
    elif choice == '2':
        example_load_and_predict()
    elif choice == '3':
        example_list_models()
    elif choice == '4':
        example_save_with_custom_name()
    elif choice == '5':
        print("\nRunning all examples...\n")
        example_train_and_save()
        example_list_models()
        example_load_and_predict()
    else:
        print("Invalid choice. Please run again and select 1-5.")


if __name__ == "__main__":
    main()
