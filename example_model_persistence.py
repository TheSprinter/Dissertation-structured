"""
Example: Model Persistence with Pickle/Joblib
==============================================

Demonstrates how to save and load ML models using the integrated pickle functionality.
"""

from src.aml_system import AMLComplianceSystem

def example_save_model():
    """Example: Train and save a model"""
    print("="*80)
    print("EXAMPLE 1: Training and Saving a Model")
    print("="*80)
    
    # Initialize system
    system = AMLComplianceSystem()
    
    # Load data
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    system.load_data(data_path)
    
    # Train and automatically save model
    print("\n🤖 Training model (will auto-save)...")
    system.ml_predictor.train_compliance_model(save_model=True)
    
    print("\n✅ Model saved successfully!")
    print("   Location: models/fraud_model.pkl")


def example_load_model():
    """Example: Load a pre-trained model"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Loading a Pre-trained Model")
    print("="*80)
    
    # Initialize system
    system = AMLComplianceSystem()
    
    # Load data
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    system.load_data(data_path)
    
    # Load pre-trained model
    print("\n📂 Loading pre-trained model...")
    if system.ml_predictor.load_model_from_disk():
        print("✅ Model loaded successfully!")
        
        # You can now use the model for predictions without retraining
        print("\n🎯 Model ready for predictions!")
    else:
        print("❌ No saved model found. Train one first.")


def example_check_and_load():
    """Example: Check if model exists before loading"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Smart Model Loading")
    print("="*80)
    
    # Initialize system
    system = AMLComplianceSystem()
    
    # Load data
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    system.load_data(data_path)
    
    # Check if model exists
    if system.ml_predictor.model_exists():
        print("\n✅ Saved model found! Loading...")
        system.ml_predictor.load_model_from_disk()
    else:
        print("\n⚠ No saved model found. Training new model...")
        system.ml_predictor.train_compliance_model(save_model=True)


def example_run_analysis_with_saved_model():
    """Example: Run complete analysis using saved model"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Complete Analysis with Model Persistence")
    print("="*80)
    
    # Initialize system
    system = AMLComplianceSystem()
    
    # Load data
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    system.load_data(data_path)
    
    # Run complete analysis (will use saved model if available)
    results = system.run_complete_analysis(save_results=True)
    
    print("\n✅ Analysis complete!")
    print(f"   - Customer profiles: {len(results['customer_profiles'])}")
    print(f"   - Anomalies detected: {len(results['anomalies'])}")
    print(f"   - Model metrics available: {bool(results['metrics'])}")


def example_model_management():
    """Example: Advanced model management"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Model Management")
    print("="*80)
    
    # Initialize system
    system = AMLComplianceSystem()
    
    # Load data
    data_path = 'fraud_management_dataset-1.5L (1).csv'
    system.load_data(data_path)
    
    # Check model status
    if system.ml_predictor.model_exists():
        print("\n📊 Existing model found")
        
        # Load existing model
        system.load_saved_model()
        
        # Option to train a new model if needed
        retrain = input("\nTrain a new model? (y/n): ").lower()
        if retrain == 'y':
            print("\n🔄 Training new model...")
            system.train_new_model(save=True)
    else:
        print("\n⚠ No existing model found")
        print("🤖 Training new model...")
        system.train_new_model(save=True)


if __name__ == '__main__':
    print("Model Persistence Examples")
    print("="*80)
    print("\nChoose an example to run:")
    print("1. Train and save a model")
    print("2. Load a pre-trained model")
    print("3. Smart model loading (check then load or train)")
    print("4. Run complete analysis with model persistence")
    print("5. Advanced model management")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == '1':
        example_save_model()
    elif choice == '2':
        example_load_model()
    elif choice == '3':
        example_check_and_load()
    elif choice == '4':
        example_run_analysis_with_saved_model()
    elif choice == '5':
        example_model_management()
    else:
        print("\n⚠ Invalid choice. Running Example 3 by default...")
        example_check_and_load()
