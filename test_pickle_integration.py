"""
Quick Test: Verify Pickle Integration
======================================

This script tests the pickle/joblib model persistence functionality.
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        import joblib
        import pandas as pd
        import numpy as np
        
        # Change to src directory for imports
        src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        from aml_system import AMLComplianceSystem
        from modules.ml_predictor import MLPredictor
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def test_model_directory():
    """Test that models directory exists"""
    print("\nTesting models directory...")
    if os.path.exists('models'):
        print("✅ Models directory exists")
        return True
    else:
        print("⚠️ Models directory not found (will be created on first save)")
        return True


def test_pickle_functionality():
    """Test basic pickle save/load functionality"""
    print("\nTesting joblib functionality...")
    try:
        import joblib
        import tempfile
        
        # Test save
        test_data = {'key': 'value', 'number': 42}
        temp_file = os.path.join(tempfile.gettempdir(), 'test_pickle.pkl')
        joblib.dump(test_data, temp_file)
        
        # Test load
        loaded_data = joblib.load(temp_file)
        
        # Cleanup
        os.remove(temp_file)
        
        if loaded_data == test_data:
            print("✅ Joblib save/load working correctly")
            return True
        else:
            print("❌ Data mismatch after load")
            return False
            
    except Exception as e:
        print(f"❌ Joblib test failed: {e}")
        return False


def test_ml_predictor_methods():
    """Test that MLPredictor has required methods"""
    print("\nTesting MLPredictor methods...")
    try:
        # Change to src directory for imports
        src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
            
        from modules.ml_predictor import MLPredictor
        
        required_methods = [
            'save_model_to_disk',
            'load_model_from_disk',
            'model_exists',
            'train_compliance_model'
        ]
        
        missing_methods = []
        for method in required_methods:
            if not hasattr(MLPredictor, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Missing methods: {', '.join(missing_methods)}")
            return False
        else:
            print("✅ All required methods present")
            return True
            
    except Exception as e:
        print(f"❌ Method check failed: {e}")
        return False


def test_system_methods():
    """Test that AMLComplianceSystem has model management methods"""
    print("\nTesting AMLComplianceSystem methods...")
    try:
        # Change to src directory for imports
        src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
            
        from aml_system import AMLComplianceSystem
        
        required_methods = [
            'train_new_model',
            'load_saved_model',
            'save_current_model'
        ]
        
        missing_methods = []
        for method in required_methods:
            if not hasattr(AMLComplianceSystem, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Missing methods: {', '.join(missing_methods)}")
            return False
        else:
            print("✅ All required methods present")
            return True
            
    except Exception as e:
        print(f"❌ Method check failed: {e}")
        return False


def test_requirements():
    """Test that joblib is in requirements.txt"""
    print("\nChecking requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            if 'joblib' in content:
                print("✅ Joblib found in requirements.txt")
                return True
            else:
                print("⚠️ Joblib not in requirements.txt")
                return False
    except Exception as e:
        print(f"❌ Could not read requirements.txt: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("PICKLE INTEGRATION TEST SUITE")
    print("="*60)
    
    tests = [
        test_imports,
        test_model_directory,
        test_pickle_functionality,
        test_ml_predictor_methods,
        test_system_methods,
        test_requirements
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if all(results):
        print("\n🎉 All tests passed! Pickle integration is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
