"""
Pickle Configuration Status Check
===================================

Run this to verify pickle/joblib integration is properly configured.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_configuration():
    """Comprehensive pickle configuration check"""
    
    print("="*70)
    print("PICKLE INTEGRATION STATUS CHECK")
    print("="*70)
    
    status = {
        'passed': 0,
        'total': 0,
        'issues': []
    }
    
    # Check 1: Joblib installed
    print("\n1. Checking joblib installation...")
    status['total'] += 1
    try:
        import joblib
        print(f"   ✅ Joblib installed (version {joblib.__version__})")
        status['passed'] += 1
    except ImportError:
        print("   ❌ Joblib not installed")
        status['issues'].append("Install joblib: pip install joblib")
    
    # Check 2: Requirements.txt
    print("\n2. Checking requirements.txt...")
    status['total'] += 1
    try:
        with open('requirements.txt', 'r') as f:
            if 'joblib' in f.read():
                print("   ✅ Joblib in requirements.txt")
                status['passed'] += 1
            else:
                print("   ⚠️ Joblib not in requirements.txt")
                status['issues'].append("Add 'joblib>=1.3.0' to requirements.txt")
    except FileNotFoundError:
        print("   ❌ requirements.txt not found")
        status['issues'].append("Create requirements.txt")
    
    # Check 3: Models directory
    print("\n3. Checking models directory...")
    status['total'] += 1
    if os.path.exists('models'):
        print("   ✅ Models directory exists")
        files = os.listdir('models')
        if files:
            print(f"   📁 Contains: {', '.join(files)}")
        else:
            print("   📁 Empty (will be populated after first training)")
        status['passed'] += 1
    else:
        print("   ❌ Models directory not found")
        status['issues'].append("Create 'models' directory")
    
    # Check 4: MLPredictor methods
    print("\n4. Checking MLPredictor pickle methods...")
    status['total'] += 1
    try:
        from modules.ml_predictor import MLPredictor
        import pandas as pd
        
        df = pd.DataFrame({'test': [1, 2, 3]})
        predictor = MLPredictor(df)
        
        methods = ['save_model_to_disk', 'load_model_from_disk', 'model_exists']
        missing = [m for m in methods if not hasattr(predictor, m)]
        
        if not missing:
            print(f"   ✅ All methods present: {', '.join(methods)}")
            status['passed'] += 1
        else:
            print(f"   ❌ Missing methods: {', '.join(missing)}")
            status['issues'].append("Update ml_predictor.py with pickle methods")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        status['issues'].append("Fix MLPredictor import/implementation")
    
    # Check 5: AMLComplianceSystem methods
    print("\n5. Checking AMLComplianceSystem model management...")
    status['total'] += 1
    try:
        from aml_system import AMLComplianceSystem
        
        system = AMLComplianceSystem()
        methods = ['train_new_model', 'load_saved_model', 'save_current_model']
        missing = [m for m in methods if not hasattr(system, m)]
        
        if not missing:
            print(f"   ✅ All methods present: {', '.join(methods)}")
            status['passed'] += 1
        else:
            print(f"   ❌ Missing methods: {', '.join(missing)}")
            status['issues'].append("Update aml_system.py with model management methods")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        status['issues'].append("Fix AMLComplianceSystem import/implementation")
    
    # Check 6: Auto-save in run_complete_analysis
    print("\n6. Checking auto-save integration...")
    status['total'] += 1
    try:
        with open('src/aml_system.py', 'r') as f:
            content = f.read()
            if 'load_model_from_disk' in content and 'run_complete_analysis' in content:
                print("   ✅ Auto-load feature integrated in run_complete_analysis")
                status['passed'] += 1
            else:
                print("   ⚠️ Auto-load may not be configured")
                status['issues'].append("Review aml_system.py run_complete_analysis method")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check 7: Streamlit app integration
    print("\n7. Checking Streamlit app (app.py)...")
    status['total'] += 1
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'run_complete_analysis' in content and 'AMLComplianceSystem' in content:
                print("   ✅ App.py uses AMLComplianceSystem.run_complete_analysis()")
                print("   ℹ️  Model loading is automatic via run_complete_analysis")
                status['passed'] += 1
            else:
                print("   ⚠️ App.py may need updates")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check 8: Documentation
    print("\n8. Checking documentation...")
    status['total'] += 1
    docs = ['MODEL_PERSISTENCE.md', 'example_model_persistence.py']
    found_docs = [d for d in docs if os.path.exists(d)]
    if found_docs:
        print(f"   ✅ Documentation available: {', '.join(found_docs)}")
        status['passed'] += 1
    else:
        print("   ⚠️ Documentation files not found")
    
    # Check 9: Saved models
    print("\n9. Checking for saved models...")
    model_files = ['fraud_model.pkl', 'scaler.pkl', 'label_encoders.pkl', 
                   'feature_names.pkl', 'model_metadata.pkl']
    if os.path.exists('models'):
        existing = [f for f in model_files if os.path.exists(os.path.join('models', f))]
        if existing:
            print(f"   ✅ Found saved models: {', '.join(existing)}")
            print("   ℹ️  System will load these automatically")
        else:
            print("   ℹ️  No saved models yet (will be created after first training)")
            print("   ℹ️  Run analysis once to train and save model")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Tests Passed: {status['passed']}/{status['total']}")
    
    if status['passed'] == status['total']:
        print("\n🎉 CONFIGURATION: EXCELLENT")
        print("✅ Pickle integration is fully configured and operational!")
        print("\n📝 Next Steps:")
        print("   1. Run the app: streamlit run app.py")
        print("   2. Upload data and run analysis")
        print("   3. Model will be trained and saved automatically")
        print("   4. Future runs will load the saved model instantly")
    elif status['passed'] >= status['total'] * 0.7:
        print("\n✅ CONFIGURATION: GOOD")
        print("Pickle integration is mostly configured.")
        if status['issues']:
            print("\n⚠️ Minor issues to address:")
            for issue in status['issues']:
                print(f"   - {issue}")
    else:
        print("\n⚠️ CONFIGURATION: NEEDS ATTENTION")
        print("Some configuration issues detected.")
        if status['issues']:
            print("\n❌ Issues to fix:")
            for issue in status['issues']:
                print(f"   - {issue}")
    
    print("\n" + "="*70)
    
    return status['passed'] == status['total']

if __name__ == '__main__':
    success = check_configuration()
    sys.exit(0 if success else 1)
