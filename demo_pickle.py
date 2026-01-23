"""
Quick Demo: Pickle Integration Test
====================================

Quick test to demonstrate pickle functionality.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aml_system import AMLComplianceSystem


def quick_demo():
    """Quick demonstration of pickle functionality"""
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         FRAUD MANAGEMENT SYSTEM                               ║
║         Pickle Integration - Quick Demo                       ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Initialize system
    print("\n📋 Step 1: Initializing system...")
    aml_system = AMLComplianceSystem()
    
    # Step 2: Load data
    print("\n📋 Step 2: Loading data...")
    aml_system.load_data()
    
    # Step 3: Check for existing models
    print("\n📋 Step 3: Checking for saved models...")
    models = aml_system.list_available_models()
    
    # Step 4: Try to load existing model or train new one
    print("\n📋 Step 4: Model loading/training...")
    
    model_loaded = False
    if len(models) > 0:
        print("🔍 Found existing model(s). Attempting to load...")
        model_loaded = aml_system.load_pretrained_model()
    
    if not model_loaded:
        print("🤖 No model found or load failed. Training new model...")
        print("⏳ This will take a few moments...")
        aml_system.run_complete_analysis(save_results=True, save_model=True)
        print("✅ Model trained and saved!")
    else:
        print("✅ Model loaded successfully!")
    
    # Step 5: Make a test prediction
    print("\n📋 Step 5: Testing prediction...")
    
    test_transaction = {
        'Time': '14:30:00',
        'Date': '2024-06-15',
        'Sender_account': 'ACC_TEST_001',
        'Receiver_account': 'ACC_TEST_002',
        'Amount': 15000,
        'Payment_currency': 'USD',
        'Received_currency': 'USD',
        'Sender_bank_location': 'US-NY',
        'Receiver_bank_location': 'UK-LDN',
        'Payment_type': 'Wire Transfer'
    }
    
    prediction = aml_system.predict_compliance_risk(test_transaction)
    
    print("\n" + "="*70)
    print("PREDICTION RESULTS")
    print("="*70)
    print(f"Transaction Amount: ${test_transaction['Amount']:,.2f}")
    print(f"From: {test_transaction['Sender_bank_location']}")
    print(f"To: {test_transaction['Receiver_bank_location']}")
    print("-"*70)
    print(f"🎯 Risk Label: {prediction['risk_label']}")
    print(f"📊 Risk Probability: {prediction['risk_probability']:.2%}")
    print(f"⚠️  Risk Score: {prediction['risk_score']:.2f}/100")
    print("="*70)
    
    # Summary
    print("\n" + "="*70)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\n📝 Summary:")
    print(f"   • Models saved in: models/")
    print(f"   • Total saved models: {len(aml_system.list_available_models())}")
    print(f"   • Model ready for predictions: ✓")
    print("\n💡 Next Steps:")
    print("   • Run 'streamlit run app.py' for web interface")
    print("   • Run 'python pickle_examples.py' for more examples")
    print("   • Check PICKLE_GUIDE.md for documentation")


if __name__ == "__main__":
    try:
        quick_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
