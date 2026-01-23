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
    
    def run_complete_analysis(self, save_results=True, save_model=True):
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
        model = self.ml_predictor.train_compliance_model()
        
        # Save the trained model if requested
        if save_model:
            self.ml_predictor.save_complete_package()
        
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
    
    def load_pretrained_model(self, model_path=None):
        """Load a pre-trained model from disk"""
        if self.ml_predictor is None:
            raise ValueError("Data not loaded. Please run load_data() first.")
        
        success = self.ml_predictor.load_complete_package(model_path)
        if success:
            print("✓ Pre-trained model loaded successfully. Ready for predictions!")
        return success
    
    def save_trained_model(self, model_path=None):
        """Save the currently trained model"""
        if self.ml_predictor is None or self.ml_predictor.model is None:
            raise ValueError("No trained model to save.")
        
        return self.ml_predictor.save_complete_package(model_path)
    
    def list_available_models(self):
        """List all saved models"""
        if self.ml_predictor is None:
            # Create temporary predictor to access list method
            from modules.ml_predictor import MLPredictor
            temp_predictor = MLPredictor(pd.DataFrame())
            return temp_predictor.list_saved_models()
        return self.ml_predictor.list_saved_models()
    
    def get_customer_risk_profile(self, account_id):
        """Get detailed risk profile for specific customer"""
        if self.customer_profiler is None or self.customer_profiler.profiles is None:
            raise ValueError("Customer profiling not completed. Please run run_complete_analysis() first.")
        
        profile = self.customer_profiler.profiles[
            self.customer_profiler.profiles['account'] == account_id
        ]
        
        if len(profile) == 0:
            return f"No profile found for account: {account_id}"
        
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
        
        summary = {
            'total_transactions': len(self.df),
            'suspicious_transactions': self.df['Is_laundering'].sum(),
            'suspicion_rate': self.df['Is_laundering'].mean() * 100,
            'date_range': f"{self.df['Date'].min()} to {self.df['Date'].max()}",
            'unique_accounts': len(set(self.df['Sender_account']) | set(self.df['Receiver_account'])),
            'total_volume': self.df['Amount'].sum(),
            'avg_transaction_amount': self.df['Amount'].mean()
        }
        
        if hasattr(self, 'customer_profiler') and self.customer_profiler.profiles is not None:
            profiles = self.customer_profiler.profiles
            summary.update({
                'high_risk_customers': len(profiles[profiles['risk_classification'] == 'HIGH']),
                'medium_risk_customers': len(profiles[profiles['risk_classification'] == 'MEDIUM']),
                'low_risk_customers': len(profiles[profiles['risk_classification'] == 'LOW'])
            })
        
        return summary
