"""
Fraud Management System
=======================

Main orchestration class for the Fraud Management System.
"""

from modules.data_manager import DataManager
from modules.customer_profiler import CustomerProfiler
from modules.anomaly_detector import AnomalyDetector
from modules.ml_predictor import MLPredictor
from modules.visualizer import AMLVisualizer


class AMLComplianceSystem:
    """
    Main AML Compliance System that orchestrates all modules
    
    Integrates:
    - Data Management
    - Customer Profiling  
    - Anomaly Detection
    - Machine Learning Prediction
    - Visualization & Reporting
    """
    
    def __init__(self, data_path=None):
        """Initialize the complete AML Compliance System"""
        self.data_path = data_path
        self.data_manager = None
        self.customer_profiler = None
        self.anomaly_detector = None
        self.ml_predictor = None
        self.visualizer = None
        self.df = None
        
        print("="*80)
        print("FRAUD MANAGEMENT AI SYSTEM INITIALIZED")
        print("="*80)
        print("🔧 System Components:")
        print("   • Data Management Module")
        print("   • Customer Profiling Module") 
        print("   • Anomaly Detection Module")
        print("   • Machine Learning Module")
        print("   • Visualization & Reporting Module")
        print("="*80)
        print("System Ready. Use load_data() to begin analysis.")
    
    def load_data(self, data_path=None):
        """Load and initialize data across all modules"""
        if data_path:
            self.data_path = data_path
        
        # Initialize data manager and load data
        self.data_manager = DataManager()
        self.df = self.data_manager.load_data(self.data_path)
        
        # Initialize other modules with the loaded data
        self.customer_profiler = CustomerProfiler(self.df)
        self.anomaly_detector = AnomalyDetector(self.df)
        self.ml_predictor = MLPredictor(self.df)
        self.visualizer = AMLVisualizer(self.df)
        
        print("\n✓ All modules initialized with loaded data")
        return self.df
    
    def run_complete_analysis(self, save_results=True):
        """Run the complete AML compliance analysis pipeline"""
        print("\n" + "="*80)
        print("RUNNING COMPLETE FRAUD ANALYSIS")
        print("="*80)
        
        if self.df is None:
            raise ValueError("Data not loaded. Please run load_data() first.")
        
        # Step 1: Customer Profiling
        print("\n🔍 Step 1: Customer Risk Profiling...")
        customer_profiles = self.customer_profiler.analyze_customers(save_results)
        
        # Step 2: Anomaly Detection  
        print("\n🚨 Step 2: Transaction Anomaly Detection...")
        anomalies = self.anomaly_detector.detect_anomalies(save_results)
        
        # Step 3: Machine Learning Model Training
        print("\n🤖 Step 3: ML Model Training...")
        # Try to load existing model, otherwise train new one
        if not self.ml_predictor.load_model_from_disk():
            model = self.ml_predictor.train_compliance_model()
        else:
            model = self.ml_predictor.model
            print("   Using pre-trained model from disk")
        
        # Step 4: Comprehensive Visualization
        print("\n📊 Step 4: Generating Visualizations...")
        self.visualizer.create_comprehensive_dashboard(customer_profiles, anomalies)
        
        # Step 5: Generate Final Report
        print("\n📄 Step 5: Generating Compliance Report...")
        self.visualizer.generate_compliance_report(
            customer_profiles, 
            anomalies, 
            self.ml_predictor.model_metrics
        )
        
        print("\n" + "="*80)
        print("✅ COMPLETE ANALYSIS FINISHED SUCCESSFULLY")
        print("="*80)
        
        return {
            'customer_profiles': customer_profiles,
            'anomalies': anomalies,
            'model': model,
            'metrics': self.ml_predictor.model_metrics
        }
    
    def predict_compliance_risk(self, transaction_data):
        """Predict compliance risk for new transaction(s)"""
        if self.ml_predictor is None or self.ml_predictor.model is None:
            raise ValueError("ML model not trained. Please run run_complete_analysis() first.")
        
        return self.ml_predictor.predict_risk(transaction_data)
    
    def train_new_model(self, save=True):
        """Force training of a new ML model"""
        if self.ml_predictor is None:
            raise ValueError("ML predictor not initialized. Please run load_data() first.")
        
        print("\n🔄 Training new model...")
        return self.ml_predictor.train_compliance_model(save_model=save)
    
    def load_saved_model(self, model_dir='models'):
        """Load a previously saved model"""
        if self.ml_predictor is None:
            raise ValueError("ML predictor not initialized. Please run load_data() first.")
        
        return self.ml_predictor.load_model_from_disk(model_dir)
    
    def save_current_model(self, model_dir='models'):
        """Save the current trained model to disk"""
        if self.ml_predictor is None or self.ml_predictor.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        self.ml_predictor.save_model_to_disk(model_dir)
    
    def get_customer_risk_profile(self, customer_id):
        """Get detailed risk profile for specific customer"""
        if self.customer_profiler is None or self.customer_profiler.profiles is None:
            raise ValueError("Customer profiling not completed. Please run run_complete_analysis() first.")
        
        profile = self.customer_profiler.profiles[
            self.customer_profiler.profiles['customer_id'] == customer_id
        ]
        
        if len(profile) == 0:
            return f"No profile found for customer: {customer_id}"
        
        return profile.iloc[0].to_dict()
    
    def detect_transaction_anomalies(self, transaction_data):
        """Detect anomalies in new transaction data"""
        if self.anomaly_detector is None:
            raise ValueError("Anomaly detector not initialized. Please run load_data() first.")
        
        # For new transactions, we'd need to implement real-time anomaly detection
        # This is a placeholder for the concept
        print("Real-time anomaly detection would be implemented here")
        return {"status": "Feature under development"}
    
    def generate_summary_report(self):
        """Generate executive summary report"""
        if self.df is None:
            raise ValueError("No data loaded for analysis")
        
        fraud_count = self.df['is_fraud'].sum() if 'is_fraud' in self.df.columns else 0
        summary = {
            'total_transactions': len(self.df),
            'suspicious_transactions': fraud_count,
            'suspicion_rate': fraud_count / len(self.df) * 100 if len(self.df) > 0 else 0,
            'date_range': f"{self.df['transaction_date'].min()} to {self.df['transaction_date'].max()}",
            'unique_accounts': self.df['customer_id'].nunique(),
            'total_volume': self.df['transaction_amount'].sum(),
            'avg_transaction_amount': self.df['transaction_amount'].mean()
        }
        
        if hasattr(self, 'customer_profiler') and self.customer_profiler.profiles is not None:
            profiles = self.customer_profiler.profiles
            summary.update({
                'high_risk_customers': len(profiles[profiles['risk_classification'] == 'HIGH']),
                'medium_risk_customers': len(profiles[profiles['risk_classification'] == 'MEDIUM']),
                'low_risk_customers': len(profiles[profiles['risk_classification'] == 'LOW'])
            })
        
        return summary
