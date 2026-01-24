"""
Pickle Examples - Code Snippets
=================================

Collection of practical code examples for model persistence.
Copy and paste these snippets into your own code!
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# ============================================================================
# EXAMPLE 1: Basic Auto-Save/Load (Recommended)
# ============================================================================

def example_1_basic_usage():
    """
    Most common pattern: Let the system handle everything automatically.
    """
    print("="*70)
    print("EXAMPLE 1: Basic Auto-Save/Load")
    print("="*70)
    
    from aml_system import AMLComplianceSystem
    
    # Initialize
    system = AMLComplianceSystem()
    
    # Load data
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    
    # Run analysis - model is automatically handled!
    # First run: Trains and saves (5 min)
    # Next runs: Loads from disk (2 sec)
    results = system.run_complete_analysis()
    
    print("✅ Analysis complete!")
    print(f"   Customer profiles: {len(results['customer_profiles'])}")
    print(f"   Anomalies: {len(results['anomalies'])}")
    print(f"   Model ready: {results['model'] is not None}")


# ============================================================================
# EXAMPLE 2: Check Before Load/Train
# ============================================================================

def example_2_check_before_load():
    """
    Check if model exists before deciding to load or train.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Check Before Load/Train")
    print("="*70)
    
    from aml_system import AMLComplianceSystem
    
    system = AMLComplianceSystem()
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    
    # Check if model exists
    if system.ml_predictor.model_exists():
        print("✅ Found saved model. Loading...")
        system.load_saved_model()
        print("   Model loaded in ~2 seconds!")
    else:
        print("⚠️ No saved model. Training new one...")
        system.train_new_model(save=True)
        print("   Model trained and saved!")
    
    # Now ready for predictions
    print("\n🎯 Model is ready for predictions")


# ============================================================================
# EXAMPLE 3: Explicit Save and Load
# ============================================================================

def example_3_explicit_save_load():
    """
    Manual control over saving and loading.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Explicit Save and Load")
    print("="*70)
    
    from aml_system import AMLComplianceSystem
    
    # === PART 1: Train and Save ===
    print("\n[Part 1] Training and saving...")
    
    system = AMLComplianceSystem()
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    
    # Train without auto-save
    system.train_new_model(save=False)
    print("✅ Model trained (not saved yet)")
    
    # Explicitly save
    system.save_current_model()
    print("✅ Model saved to models/")
    
    # === PART 2: Load Later ===
    print("\n[Part 2] Loading saved model...")
    
    # New system instance (simulates new session)
    system2 = AMLComplianceSystem()
    system2.load_data('fraud_management_dataset-1.5L (1).csv')
    
    # Explicitly load
    if system2.load_saved_model():
        print("✅ Model loaded successfully!")
    else:
        print("❌ Failed to load model")


# ============================================================================
# EXAMPLE 4: Custom Model Directory
# ============================================================================

def example_4_custom_directory():
    """
    Save and load models from custom directories.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom Model Directory")
    print("="*70)
    
    from aml_system import AMLComplianceSystem
    
    system = AMLComplianceSystem()
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    
    # Save to custom directory
    custom_dir = 'my_models'
    print(f"\n💾 Saving to custom directory: {custom_dir}/")
    
    system.train_new_model(save=False)  # Train first
    system.ml_predictor.save_model_to_disk(model_dir=custom_dir)
    print(f"✅ Model saved to {custom_dir}/")
    
    # Load from custom directory
    print(f"\n📂 Loading from custom directory: {custom_dir}/")
    system2 = AMLComplianceSystem()
    system2.load_data('fraud_management_dataset-1.5L (1).csv')
    
    if system2.ml_predictor.load_model_from_disk(model_dir=custom_dir):
        print(f"✅ Model loaded from {custom_dir}/")


# ============================================================================
# EXAMPLE 5: Batch Predictions (Efficient)
# ============================================================================

def example_5_batch_predictions():
    """
    Load model once, make many predictions (efficient).
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Batch Predictions")
    print("="*70)
    
    from aml_system import AMLComplianceSystem
    
    # Initialize and load model ONCE
    system = AMLComplianceSystem()
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    system.load_saved_model()
    
    print("✅ Model loaded once")
    
    # Sample transactions
    transactions = [
        {
            'Time': '14:30:00', 'Date': '2024-06-15',
            'Sender_account': 'ACC001', 'Receiver_account': 'ACC002',
            'Amount': 9500, 'Payment_currency': 'USD',
            'Received_currency': 'USD', 'Sender_bank_location': 'US-NY',
            'Receiver_bank_location': 'AE-DXB', 'Payment_type': 'Wire'
        },
        {
            'Time': '09:15:00', 'Date': '2024-06-15',
            'Sender_account': 'ACC003', 'Receiver_account': 'ACC004',
            'Amount': 500, 'Payment_currency': 'USD',
            'Received_currency': 'USD', 'Sender_bank_location': 'US-CA',
            'Receiver_bank_location': 'US-NY', 'Payment_type': 'ACH'
        }
    ]
    
    print(f"\n🎯 Processing {len(transactions)} transactions...")
    
    # Process all transactions efficiently
    for i, transaction in enumerate(transactions, 1):
        result = system.predict_compliance_risk(transaction)
        print(f"   Transaction {i}: {result['risk_label']} "
              f"(Score: {result['risk_score']:.1f})")
    
    print("\n✅ All predictions complete!")


# ============================================================================
# EXAMPLE 6: Model Versioning (Manual)
# ============================================================================

def example_6_model_versioning():
    """
    Manually version models by saving to different directories.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Model Versioning")
    print("="*70)
    
    from aml_system import AMLComplianceSystem
    from datetime import datetime
    
    system = AMLComplianceSystem()
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    
    # Train model
    system.train_new_model(save=False)
    
    # Save with version/date
    version = datetime.now().strftime('%Y%m%d_%H%M%S')
    version_dir = f'models_v{version}'
    
    print(f"\n💾 Saving versioned model: {version_dir}/")
    system.ml_predictor.save_model_to_disk(model_dir=version_dir)
    print(f"✅ Model saved with version: {version}")
    
    # Load specific version
    print(f"\n📂 Loading versioned model...")
    system2 = AMLComplianceSystem()
    system2.load_data('fraud_management_dataset-1.5L (1).csv')
    
    if system2.ml_predictor.load_model_from_disk(model_dir=version_dir):
        print(f"✅ Loaded model version: {version}")


# ============================================================================
# EXAMPLE 7: Model Backup Before Retraining
# ============================================================================

def example_7_backup_before_retrain():
    """
    Backup existing model before training a new one.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Backup Before Retraining")
    print("="*70)
    
    import shutil
    from datetime import datetime
    from aml_system import AMLComplianceSystem
    
    # Check if model exists
    if os.path.exists('models/fraud_model.pkl'):
        # Backup existing model
        backup_dir = f"models_backup_{datetime.now().strftime('%Y%m%d')}"
        print(f"\n💾 Backing up current model to: {backup_dir}/")
        
        if os.path.exists('models'):
            shutil.copytree('models', backup_dir, dirs_exist_ok=True)
            print(f"✅ Backup created: {backup_dir}/")
    
    # Train new model
    print("\n🤖 Training new model...")
    system = AMLComplianceSystem()
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    system.train_new_model(save=True)
    
    print("✅ New model trained and saved!")
    print("   Old model is backed up and safe")


# ============================================================================
# EXAMPLE 8: Error Handling
# ============================================================================

def example_8_error_handling():
    """
    Proper error handling for load failures.
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Error Handling")
    print("="*70)
    
    from aml_system import AMLComplianceSystem
    
    system = AMLComplianceSystem()
    system.load_data('fraud_management_dataset-1.5L (1).csv')
    
    print("\n🔄 Attempting to load model...")
    
    try:
        # Try to load
        if system.load_saved_model():
            print("✅ Model loaded successfully!")
            
            # Verify it works
            sample_transaction = {
                'Time': '14:30:00', 'Date': '2024-06-15',
                'Sender_account': 'ACC001', 'Receiver_account': 'ACC002',
                'Amount': 1000, 'Payment_currency': 'USD',
                'Received_currency': 'USD', 'Sender_bank_location': 'US-NY',
                'Receiver_bank_location': 'US-CA', 'Payment_type': 'Wire'
            }
            
            result = system.predict_compliance_risk(sample_transaction)
            print(f"   Test prediction: {result['risk_label']}")
            
        else:
            print("⚠️ No saved model found")
            print("   Training new model as fallback...")
            system.train_new_model(save=True)
            print("✅ New model trained and saved!")
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("   Recommended action: Retrain model")


# ============================================================================
# EXAMPLE 9: Check Model Freshness
# ============================================================================

def example_9_check_model_age():
    """
    Check model age and decide if retraining is needed.
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: Check Model Freshness")
    print("="*70)
    
    from datetime import datetime
    from aml_system import AMLComplianceSystem
    
    model_path = 'models/fraud_model.pkl'
    
    if os.path.exists(model_path):
        # Get model age
        mtime = os.path.getmtime(model_path)
        model_date = datetime.fromtimestamp(mtime)
        age_days = (datetime.now() - model_date).days
        
        print(f"\n📅 Model Information:")
        print(f"   Last trained: {model_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Age: {age_days} days")
        
        # Decision logic
        if age_days > 30:
            print(f"\n⚠️ Model is {age_days} days old (>30 days)")
            print("   Recommendation: Retrain model with fresh data")
            
            # Retrain
            system = AMLComplianceSystem()
            system.load_data('fraud_management_dataset-1.5L (1).csv')
            system.train_new_model(save=True)
            print("✅ Model retrained and saved!")
        else:
            print(f"\n✅ Model is recent ({age_days} days old)")
            print("   No retraining needed")
    else:
        print("\n⚠️ No model found. Training new one...")


# ============================================================================
# EXAMPLE 10: Model Metadata Access
# ============================================================================

def example_10_access_metadata():
    """
    Access and display saved model metadata.
    """
    print("\n" + "="*70)
    print("EXAMPLE 10: Access Model Metadata")
    print("="*70)
    
    import joblib
    
    metadata_path = 'models/model_metadata.pkl'
    
    if os.path.exists(metadata_path):
        print("\n📊 Loading model metadata...")
        
        metadata = joblib.load(metadata_path)
        
        print("\nModel Metadata:")
        print(f"  Training timestamp: {metadata.get('timestamp', 'Unknown')}")
        print(f"  Feature count: {metadata.get('feature_count', 'Unknown')}")
        
        if 'model_metrics' in metadata:
            print("\n  Performance Metrics:")
            for model_name, metrics in metadata['model_metrics'].items():
                print(f"\n    {model_name.upper()}:")
                print(f"      Accuracy:  {metrics.get('accuracy', 0):.3f}")
                print(f"      Precision: {metrics.get('precision', 0):.3f}")
                print(f"      Recall:    {metrics.get('recall', 0):.3f}")
                print(f"      F1-Score:  {metrics.get('f1_score', 0):.3f}")
    else:
        print("\n⚠️ No metadata found. Train a model first.")


# ============================================================================
# MAIN MENU
# ============================================================================

def show_menu():
    """Display menu and run selected example"""
    examples = {
        '1': ('Basic Auto-Save/Load', example_1_basic_usage),
        '2': ('Check Before Load/Train', example_2_check_before_load),
        '3': ('Explicit Save and Load', example_3_explicit_save_load),
        '4': ('Custom Model Directory', example_4_custom_directory),
        '5': ('Batch Predictions', example_5_batch_predictions),
        '6': ('Model Versioning', example_6_model_versioning),
        '7': ('Backup Before Retraining', example_7_backup_before_retrain),
        '8': ('Error Handling', example_8_error_handling),
        '9': ('Check Model Freshness', example_9_check_model_age),
        '10': ('Access Model Metadata', example_10_access_metadata),
    }
    
    while True:
        print("\n" + "="*70)
        print("  PICKLE EXAMPLES - Choose an example to run")
        print("="*70)
        
        for key, (name, _) in examples.items():
            print(f"  {key:>2}. {name}")
        print(f"   0. Exit")
        
        choice = input("\nEnter your choice (0-10): ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            break
        elif choice in examples:
            name, func = examples[choice]
            try:
                func()
                input("\nPress Enter to continue...")
            except FileNotFoundError as e:
                print(f"\n⚠️ File not found: {e}")
                print("   Make sure 'fraud_management_dataset-1.5L (1).csv' exists")
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\nPress Enter to continue...")
        else:
            print("\n⚠️ Invalid choice")


if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              PICKLE CODE EXAMPLES                                 ║
║              Copy these snippets for your own use!                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    show_menu()
