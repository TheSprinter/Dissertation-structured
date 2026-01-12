"""
Setup Script for AML Compliance System
=======================================

Quick setup and verification script.
"""

import os
import sys


def create_output_directory():
    """Create output directory if it doesn't exist"""
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ Created {output_dir}/ directory")
    else:
        print(f"✓ {output_dir}/ directory already exists")


def verify_dependencies():
    """Verify all required dependencies are installed"""
    print("\n📦 Verifying dependencies...")
    
    required_packages = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('sklearn', 'sklearn'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'sns')
    ]
    
    missing_packages = []
    
    for package, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        print("Install them using: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True


def check_project_structure():
    """Verify project structure is correct"""
    print("\n📁 Checking project structure...")
    
    required_dirs = ['src', 'src/modules', 'data', 'output', 'tests']
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'src/__init__.py',
        'src/config.py',
        'src/aml_system.py',
        'src/modules/__init__.py',
        'src/modules/data_manager.py',
        'src/modules/customer_profiler.py',
        'src/modules/anomaly_detector.py',
        'src/modules/ml_predictor.py',
        'src/modules/visualizer.py'
    ]
    
    all_good = True
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"   ✓ {directory}/")
        else:
            print(f"   ✗ {directory}/ - MISSING")
            all_good = False
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} - MISSING")
            all_good = False
    
    if all_good:
        print("\n✅ Project structure is correct!")
    else:
        print("\n⚠ Some files/directories are missing!")
    
    return all_good


def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("\n📝 Next Steps:")
    print("   1. Activate virtual environment (if using one)")
    print("   2. Install dependencies: pip install -r requirements.txt")
    print("   3. Run the system: python main.py")
    print("\n📚 Quick Commands:")
    print("   • Run tests: python -m pytest tests/")
    print("   • Check help: python main.py --help")
    print("\n📖 For more information, see README.md")
    print("="*60)


def main():
    """Main setup function"""
    print("="*60)
    print("AML COMPLIANCE SYSTEM - SETUP")
    print("="*60)
    
    # Create necessary directories
    create_output_directory()
    
    # Verify dependencies
    deps_ok = verify_dependencies()
    
    # Check project structure
    structure_ok = check_project_structure()
    
    # Display next steps
    display_next_steps()
    
    if deps_ok and structure_ok:
        print("\n✅ System is ready to use!")
        return 0
    else:
        print("\n⚠ Please fix the issues above before running the system.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
