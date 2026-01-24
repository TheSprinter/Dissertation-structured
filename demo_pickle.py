"""
Demo: Pickle Model Persistence
================================

Interactive demonstration of model persistence features.
Run this script to see pickle in action!
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_step(step_num, description):
    """Print a step description"""
    print(f"\n[Step {step_num}] {description}")
    print("-" * 70)

def wait_for_user():
    """Wait for user to press Enter"""
    input("\nPress Enter to continue...")

def demo_check_configuration():
    """Demo: Check if pickle is configured"""
    print_header("DEMO 1: Check Pickle Configuration")
    
    print("\n✓ Checking joblib installation...")
    import joblib
    print(f"  Joblib version: {joblib.__version__}")
    
    print("\n✓ Checking models directory...")
    if os.path.exists('models'):
        print(f"  Models directory exists: ✅")
        files = os.listdir('models')
        if files:
            print(f"  Files found: {len(files)}")
            for f in files:
                print(f"    - {f}")
        else:
            print(f"  Directory is empty (ready for first save)")
    else:
        print(f"  Models directory not found ⚠️")
    
    print("\n✓ Checking AMLComplianceSystem...")
    from aml_system import AMLComplianceSystem
    system = AMLComplianceSystem()
    
    methods = ['train_new_model', 'load_saved_model', 'save_current_model']
    for method in methods:
        if hasattr(system, method):
            print(f"  {method}(): ✅")
    
    print("\n🎉 Pickle is configured and ready!")
    wait_for_user()

def demo_check_existing_model():
    """Demo: Check if model exists"""
    print_header("DEMO 2: Check for Existing Model")
    
    from aml_system import AMLComplianceSystem
    
    print_step(1, "Initialize system")
    system = AMLComplianceSystem()
    
    # Load sample data
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    if not os.path.exists(data_path):
        print(f"\n⚠️ Sample data not found: {data_path}")
        print("Please ensure the dataset file exists in the project root.")
        return
    
    print(f"Loading data from: {data_path}")
    system.load_data(data_path)
    
    print_step(2, "Check if saved model exists")
    if system.ml_predictor.model_exists():
        print("✅ Saved model found!")
        print("   Location: models/fraud_model.pkl")
        
        # Get file info
        model_path = 'models/fraud_model.pkl'
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        mtime = os.path.getmtime(model_path)
        from datetime import datetime
        mod_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Last modified: {mod_date}")
    else:
        print("⚠️ No saved model found")
        print("   Run demo_train_and_save() to create one")
    
    wait_for_user()

def demo_train_and_save():
    """Demo: Train and save model"""
    print_header("DEMO 3: Train and Save Model")
    
    from aml_system import AMLComplianceSystem
    
    print_step(1, "Initialize system and load data")
    system = AMLComplianceSystem()
    
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    if not os.path.exists(data_path):
        print(f"\n⚠️ Sample data not found: {data_path}")
        return
    
    print(f"Loading data from: {data_path}")
    system.load_data(data_path)
    print("✅ Data loaded successfully")
    
    print_step(2, "Train machine learning model")
    print("⚠️ This will take 3-5 minutes...")
    print("   Training RandomForest and GradientBoosting models")
    print("   Performing cross-validation")
    print("   Selecting best model")
    
    start_time = time.time()
    model = system.train_new_model(save=True)
    elapsed = time.time() - start_time
    
    print(f"\n✅ Training complete in {elapsed:.1f} seconds")
    
    print_step(3, "Model automatically saved!")
    print("Files created in models/ directory:")
    for filename in os.listdir('models'):
        filepath = os.path.join('models', filename)
        if os.path.isfile(filepath):
            size_kb = os.path.getsize(filepath) / 1024
            if size_kb > 1024:
                print(f"  ✓ {filename} ({size_kb/1024:.2f} MB)")
            else:
                print(f"  ✓ {filename} ({size_kb:.2f} KB)")
    
    print("\n🎉 Model trained and saved successfully!")
    wait_for_user()

def demo_load_model():
    """Demo: Load existing model"""
    print_header("DEMO 4: Load Saved Model")
    
    from aml_system import AMLComplianceSystem
    
    print_step(1, "Initialize system and load data")
    system = AMLComplianceSystem()
    
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    if not os.path.exists(data_path):
        print(f"\n⚠️ Sample data not found: {data_path}")
        return
    
    system.load_data(data_path)
    
    print_step(2, "Load saved model from disk")
    print("⚡ Loading model (this is FAST!)...")
    
    start_time = time.time()
    success = system.load_saved_model()
    elapsed = time.time() - start_time
    
    if success:
        print(f"\n✅ Model loaded in {elapsed:.2f} seconds!")
        print("\n📊 Model is ready for predictions")
        
        # Show model info
        import joblib
        metadata = joblib.load('models/model_metadata.pkl')
        print("\nModel Information:")
        print(f"  Training date: {metadata.get('timestamp', 'Unknown')}")
        print(f"  Features: {metadata.get('feature_count', 'Unknown')}")
        if 'model_metrics' in metadata:
            metrics = metadata['model_metrics']
            if metrics:
                best_model = list(metrics.keys())[0]
                m = metrics[best_model]
                print(f"\n  Performance Metrics ({best_model}):")
                print(f"    Accuracy:  {m.get('accuracy', 0):.3f}")
                print(f"    Precision: {m.get('precision', 0):.3f}")
                print(f"    Recall:    {m.get('recall', 0):.3f}")
                print(f"    F1-Score:  {m.get('f1_score', 0):.3f}")
    else:
        print("\n⚠️ Failed to load model")
        print("   No saved model found. Run demo_train_and_save() first.")
    
    wait_for_user()

def demo_compare_speed():
    """Demo: Compare training vs loading speed"""
    print_header("DEMO 5: Training vs Loading Speed Comparison")
    
    from aml_system import AMLComplianceSystem
    
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    if not os.path.exists(data_path):
        print(f"\n⚠️ Sample data not found: {data_path}")
        return
    
    print("\n📊 Speed Comparison:")
    print("-" * 70)
    
    # Check if model exists
    if os.path.exists('models/fraud_model.pkl'):
        print("\n⚡ LOADING SAVED MODEL:")
        system = AMLComplianceSystem()
        system.load_data(data_path)
        
        start_time = time.time()
        system.load_saved_model()
        load_time = time.time() - start_time
        
        print(f"   Time taken: {load_time:.2f} seconds")
        print(f"   Status: ✅ Ready for predictions!")
        
        print("\n🐢 IF WE HAD TO TRAIN:")
        print(f"   Estimated time: 180-300 seconds (3-5 minutes)")
        print(f"   Status: ⏰ Much slower!")
        
        print(f"\n💡 SPEED IMPROVEMENT:")
        estimated_train_time = 240  # Average 4 minutes
        speedup = estimated_train_time / load_time
        time_saved = estimated_train_time - load_time
        print(f"   {speedup:.0f}x faster!")
        print(f"   Time saved: {time_saved:.0f} seconds ({time_saved/60:.1f} minutes)")
    else:
        print("\n⚠️ No saved model found")
        print("   Run demo_train_and_save() first to see the comparison")
    
    wait_for_user()

def demo_make_prediction():
    """Demo: Make prediction with loaded model"""
    print_header("DEMO 6: Make Predictions")
    
    from aml_system import AMLComplianceSystem
    
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    if not os.path.exists(data_path):
        print(f"\n⚠️ Sample data not found: {data_path}")
        return
    
    print_step(1, "Load system and model")
    system = AMLComplianceSystem()
    system.load_data(data_path)
    
    if not system.load_saved_model():
        print("⚠️ No model found. Train one first with demo_train_and_save()")
        return
    
    print("✅ Model loaded and ready")
    
    print_step(2, "Create sample transaction")
    
    sample_transaction = {
        'Time': '14:30:00',
        'Date': '2024-06-15',
        'Sender_account': 'ACC123456',
        'Receiver_account': 'ACC789012',
        'Amount': 9500,
        'Payment_currency': 'USD',
        'Received_currency': 'USD',
        'Sender_bank_location': 'US-NY',
        'Receiver_bank_location': 'AE-DXB',
        'Payment_type': 'Wire'
    }
    
    print("\nTransaction Details:")
    print(f"  Amount: ${sample_transaction['Amount']:,}")
    print(f"  From: {sample_transaction['Sender_bank_location']}")
    print(f"  To: {sample_transaction['Receiver_bank_location']}")
    print(f"  Type: {sample_transaction['Payment_type']}")
    
    print_step(3, "Predict fraud risk")
    
    try:
        result = system.predict_compliance_risk(sample_transaction)
        
        print("\n🎯 PREDICTION RESULTS:")
        print("-" * 70)
        print(f"  Risk Label:       {result['risk_label']}")
        print(f"  Risk Probability: {result['risk_probability']:.2%}")
        print(f"  Risk Score:       {result['risk_score']:.1f}/100")
        
        if result['risk_probability'] > 0.7:
            print("\n  ⚠️  HIGH RISK - Recommend manual review")
        elif result['risk_probability'] > 0.4:
            print("\n  ⚡ MEDIUM RISK - Monitor transaction")
        else:
            print("\n  ✅ LOW RISK - Transaction appears normal")
    
    except Exception as e:
        print(f"\n❌ Prediction failed: {e}")
    
    wait_for_user()

def demo_menu():
    """Show interactive menu"""
    while True:
        print_header("Pickle Model Persistence - Interactive Demo")
        
        print("\nChoose a demonstration:\n")
        print("  1. Check Configuration")
        print("  2. Check for Existing Model")
        print("  3. Train and Save Model (3-5 minutes)")
        print("  4. Load Saved Model (2 seconds)")
        print("  5. Compare Training vs Loading Speed")
        print("  6. Make Predictions with Loaded Model")
        print("  7. Run All Demos (Full Walkthrough)")
        print("  0. Exit")
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == '1':
            demo_check_configuration()
        elif choice == '2':
            demo_check_existing_model()
        elif choice == '3':
            demo_train_and_save()
        elif choice == '4':
            demo_load_model()
        elif choice == '5':
            demo_compare_speed()
        elif choice == '6':
            demo_make_prediction()
        elif choice == '7':
            demo_check_configuration()
            demo_check_existing_model()
            if not os.path.exists('models/fraud_model.pkl'):
                demo_train_and_save()
            demo_load_model()
            demo_compare_speed()
            demo_make_prediction()
            print_header("All Demos Complete! 🎉")
            wait_for_user()
        elif choice == '0':
            print("\n👋 Thanks for trying the pickle demo!")
            break
        else:
            print("\n⚠️ Invalid choice. Please try again.")

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     PICKLE MODEL PERSISTENCE - INTERACTIVE DEMO                   ║
║     Fraud Management System                                       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

This demo shows how pickle enables fast model loading.

Key Features:
  ✓ Save trained models to disk
  ✓ Load models in ~2 seconds (vs 5 minutes training)
  ✓ Deploy pre-trained models to production
  ✓ Share models across sessions

""")
    
    demo_menu()
