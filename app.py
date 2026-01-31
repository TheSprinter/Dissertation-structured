"""
Streamlit Web Application for Fraud Management System
======================================================

A comprehensive web interface for fraud detection and management.
"""

import streamlit as st
import pandas as pd
import sys
import os
from io import StringIO
import base64

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aml_system import AMLComplianceSystem

# Page configuration
st.set_page_config(
    page_title="Fraud Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
    .risk-high {
        color: #DC2626;
        font-weight: bold;
    }
    .risk-medium {
        color: #F59E0B;
        font-weight: bold;
    }
    .risk-low {
        color: #10B981;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #3B82F6;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'aml_system' not in st.session_state:
    st.session_state.aml_system = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

def initialize_system():
    """Initialize the AML system"""
    if st.session_state.aml_system is None:
        st.session_state.aml_system = AMLComplianceSystem()
    return st.session_state.aml_system

def load_data(data_source):
    """Load data into the system"""
    aml_system = initialize_system()
    with st.spinner("Loading and processing data..."):
        df = aml_system.load_data(data_source)
        st.session_state.data_loaded = True
        return df

def run_analysis():
    """Run complete AML analysis"""
    aml_system = st.session_state.aml_system
    with st.spinner("Running comprehensive AML analysis... This may take a few moments."):
        results = aml_system.run_complete_analysis(save_results=True)
        st.session_state.analysis_complete = True
        st.session_state.analysis_results = results
        return results

def get_image_download_link(img_path, filename):
    """Generate download link for image"""
    if os.path.exists(img_path):
        with open(img_path, "rb") as file:
            img_bytes = file.read()
        b64 = base64.b64encode(img_bytes).decode()
        return f'<a href="data:image/png;base64,{b64}" download="{filename}">Download {filename}</a>'
    return ""

def main():
    # Header
    st.markdown('<div class="main-header">🛡️ Fraud Management System</div>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Fraud Detection & Risk Management Platform")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "🏠 Home",
        "📊 Data Upload & Analysis",
        "🔍 Transaction Risk Prediction",
        "👥 Customer Risk Profiles",
        "📈 Dashboard & Reports",
        "💾 Model Management",
        "ℹ️ About"
    ])
    
    # Home Page
    if page == "🏠 Home":
        #st.header("Welcome to the Fraud Management System")
        
        # Project Information
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 10px; 
                    color: white; 
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0 0 1rem 0; color: white;">🎓 Academic Project Information</h3>
            <p style="margin: 0.5rem 0; font-size: 1.1rem;">
                <strong>Project:</strong> Final Semester Dissertation Project<br>
                <strong>Institution:</strong> BITS Pilani<br>
                <strong>Program:</strong> MTech in Artificial Intelligence and Machine Learning (AIML)<br>
                <strong>Submitted by:</strong> Simit Das<br>
                <strong>BITS ID:</strong> 2023AA05807
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 Features</h3>
                <ul>
                    <li>Real-time risk assessment</li>
                    <li>ML-powered predictions</li>
                    <li>Anomaly detection</li>
                    <li>Customer profiling</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🔧 Capabilities</h3>
                <ul>
                    <li>Multi-algorithm detection</li>
                    <li>Interactive dashboards</li>
                    <li>Compliance reporting</li>
                    <li>Risk classification</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Analytics</h3>
                <ul>
                    <li>Transaction patterns</li>
                    <li>Risk scoring</li>
                    <li>Behavioral analysis</li>
                    <li>Trend visualization</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("👈 Use the sidebar to navigate to different sections of the application.")
        
        # Quick Start Guide
        with st.expander("📚 Quick Start Guide"):
            st.markdown("""
            1. **Data Upload & Analysis**: Upload your transaction data (CSV) or use sample data
            2. **Run Analysis**: Process the data through our ML pipeline
            3. **View Results**: Explore dashboards, reports, and risk assessments
            4. **Predict Risk**: Test individual transactions for compliance risk
            5. **Customer Profiles**: View detailed risk profiles for accounts
            """)
    
    # Data Upload & Analysis Page
    elif page == "📊 Data Upload & Analysis":
        st.header("Data Upload & Analysis")
        
        st.markdown("### Upload Transaction Data")
        
        # Data source selection
        data_option = st.radio(
            "Choose data source:",
            ["Upload CSV File", "Use Sample Data", "Enter Data URL"]
        )
        
        data_source = None
        
        if data_option == "Upload CSV File":
            uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
            if uploaded_file is not None:
                # Save uploaded file temporarily
                temp_path = "temp_uploaded_data.csv"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                data_source = temp_path
                st.success("✅ File uploaded successfully!")
                
                # Show preview
                df_preview = pd.read_csv(temp_path)
                st.markdown("#### Data Preview")
                st.dataframe(df_preview.head(10))
                st.write(f"**Shape:** {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")
        
        elif data_option == "Use Sample Data":
            st.info("Sample data will be generated automatically")
            data_source = None  # Will trigger synthetic data generation
        
        elif data_option == "Enter Data URL":
            data_url = st.text_input("Enter data URL:")
            if data_url:
                data_source = data_url
        
        # Load Data Button
        if st.button("🔄 Load Data", key="load_data_btn"):
            if data_option == "Upload CSV File" and data_source is None:
                st.error("Please upload a CSV file first")
            else:
                try:
                    df = load_data(data_source)
                    st.success("✅ Data loaded successfully!")
                    
                    # Display data statistics
                    st.markdown("### Data Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Transactions", f"{len(df):,}")
                    with col2:
                        st.metric("Unique Customers", f"{df['customer_id'].nunique():,}")
                    with col3:
                        st.metric("Total Volume", f"${df['transaction_amount'].sum():,.2f}")
                    with col4:
                        st.metric("Avg Transaction", f"${df['transaction_amount'].mean():,.2f}")
                    
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
        
        # Run Analysis Button
        st.markdown("---")
        if st.session_state.data_loaded:
            st.markdown("### Run Complete AML Analysis")
            st.info("This will perform customer profiling, anomaly detection, ML model training, and generate visualizations.")
            
            if st.button("🚀 Run Complete Analysis", key="run_analysis_btn"):
                try:
                    results = run_analysis()
                    st.success("✅ Analysis completed successfully!")
                    
                    # Display summary metrics
                    summary = st.session_state.aml_system.generate_summary_report()
                    
                    st.markdown("### Analysis Summary")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Suspicious Transactions", 
                                f"{summary.get('suspicious_transactions', 0):,}")
                        st.metric("Suspicion Rate", 
                                f"{summary.get('suspicion_rate', 0):.2f}%")
                    
                    with col2:
                        st.metric("High Risk Customers", 
                                summary.get('high_risk_customers', 'N/A'))
                        st.metric("Medium Risk Customers", 
                                summary.get('medium_risk_customers', 'N/A'))
                    
                    with col3:
                        st.metric("Low Risk Customers", 
                                summary.get('low_risk_customers', 'N/A'))
                        st.metric("Total Volume", 
                                f"${summary.get('total_volume', 0):,.2f}")
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
        else:
            st.warning("⚠️ Please load data first before running analysis.")
    
    # Transaction Risk Prediction Page
    elif page == "🔍 Transaction Risk Prediction":
        st.header("Transaction Risk Prediction")
        
        if not st.session_state.analysis_complete:
            st.warning("⚠️ Please complete the data analysis first (Data Upload & Analysis page)")
        else:
            st.markdown("### Enter Transaction Details")
            
            # Create tabs for better organization
            basic_tab, location_tab, verification_tab = st.tabs(["Basic Info", "Location & Currency", "Verification"])
            
            with basic_tab:
                col1, col2 = st.columns(2)
                
                with col1:
                    transaction_time = st.text_input("Transaction Time (HH:MM:SS)", "14:30:00")
                    transaction_date = st.date_input("Transaction Date")
                    customer_id = st.text_input("Customer ID", "CUST00001")
                    transaction_amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=500.0, step=50.0)
                    merchant_id = st.text_input("Merchant ID", "MERCH0001")
                    merchant_category = st.selectbox("Merchant Category", 
                        ["Electronics", "Grocery", "Restaurant", "Travel", "Healthcare",
                         "Entertainment", "Utilities", "Fashion", "Home", "Sports"])
                
                with col2:
                    payment_method = st.selectbox("Payment Method", 
                        ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer", "Cryptocurrency"])
                    transaction_type = st.selectbox("Transaction Type",
                        ["Purchase", "Cash Withdrawal", "Transfer", "Payment"])
                    device_type = st.selectbox("Device Type",
                        ["Mobile", "Desktop", "Tablet"])
                    card_type = st.selectbox("Card Type",
                        ["Visa", "Mastercard", "American Express", "Discover"])
                    cvv_match = st.selectbox("CVV Match", [1, 0], help="1=Match, 0=No match")
                    card_present = st.selectbox("Card Present", [1, 0], help="1=Yes, 0=No")
            
            with location_tab:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Geographic Information")
                    location = st.selectbox("Transaction Location", 
                        ["US", "UK", "IN", "AE", "CN", "SG", "JP", "DE", "FR", "AU"])
                    billing_country = st.selectbox("Billing Country", 
                        ["US", "UK", "IN", "AE", "CN", "SG", "JP", "DE", "FR", "AU"], index=0)
                    shipping_country = st.selectbox("Shipping Country", 
                        ["US", "UK", "IN", "AE", "CN", "SG", "JP", "DE", "FR", "AU"], index=0)
                    ip_country = st.selectbox("IP Country", 
                        ["US", "UK", "IN", "AE", "CN", "SG", "JP", "DE", "FR", "AU"], index=0)
                
                with col2:
                    st.markdown("#### Currency Information")
                    transaction_currency = st.selectbox("Transaction Currency", 
                        ["USD", "EUR", "GBP", "INR", "AED", "CNY", "SGD", "JPY"], index=0)
                    billing_currency = st.selectbox("Billing Currency", 
                        ["USD", "EUR", "GBP", "INR", "AED", "CNY", "SGD", "JPY"], index=0)
                    
                    st.markdown("#### Additional Info")
                    merchant_reputation = st.selectbox("Merchant Reputation", 
                        ["High", "Medium", "Low"], index=0)
            
            with verification_tab:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Account Verification")
                    email_verified = st.selectbox("Email Verified", [1, 0], help="1=Yes, 0=No")
                    phone_verified = st.selectbox("Phone Verified", [1, 0], help="1=Yes, 0=No")
                    shipping_address_verified = st.selectbox("Shipping Address Verified", [1, 0], help="1=Yes, 0=No")
                
                with col2:
                    st.markdown("#### Security Metrics")
                    failed_login_attempts = st.number_input("Failed Login Attempts", min_value=0, max_value=10, value=0)
                    velocity_score = st.slider("Velocity Score", 0, 100, 50, 
                                              help="Transaction velocity indicator")
                    distance_from_last_transaction_km = st.number_input("Distance from Last Transaction (km)", 
                                                                        min_value=0.0, value=50.0, step=10.0)
            
            if st.button("🎯 Predict Risk", key="predict_btn"):
                transaction = {
                    'transaction_time': transaction_time,
                    'transaction_date': str(transaction_date),
                    'customer_id': customer_id,
                    'transaction_amount': transaction_amount,
                    'merchant_id': merchant_id,
                    'merchant_category': merchant_category,
                    'payment_method': payment_method,
                    'transaction_type': transaction_type,
                    'device_type': device_type,
                    'location': location,
                    'card_type': card_type,
                    'cvv_match': cvv_match,
                    'card_present': card_present,
                    'billing_country': billing_country,
                    'shipping_country': shipping_country,
                    'ip_country': ip_country,
                    'transaction_currency': transaction_currency,
                    'billing_currency': billing_currency,
                    'merchant_reputation': merchant_reputation,
                    'email_verified': email_verified,
                    'phone_verified': phone_verified,
                    'shipping_address_verified': shipping_address_verified,
                    'failed_login_attempts': failed_login_attempts,
                    'velocity_score': velocity_score,
                    'distance_from_last_transaction_km': distance_from_last_transaction_km
                }
                
                try:
                    with st.spinner("Analyzing transaction..."):
                        prediction = st.session_state.aml_system.predict_compliance_risk(transaction)
                    
                    st.markdown("### Risk Assessment Results")
                    
                    # Display results in a nice format
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Transaction Details")
                        for key, value in transaction.items():
                            st.text(f"{key}: {value}")
                    
                    with col2:
                        st.markdown("#### Risk Prediction")
                        for key, value in prediction.items():
                            if isinstance(value, float):
                                st.text(f"{key}: {value:.4f}")
                            else:
                                # Color code risk levels
                                if value == "HIGH":
                                    st.markdown(f'**{key}:** <span class="risk-high">{value}</span>', 
                                              unsafe_allow_html=True)
                                elif value == "MEDIUM":
                                    st.markdown(f'**{key}:** <span class="risk-medium">{value}</span>', 
                                              unsafe_allow_html=True)
                                elif value == "LOW":
                                    st.markdown(f'**{key}:** <span class="risk-low">{value}</span>', 
                                              unsafe_allow_html=True)
                                else:
                                    st.text(f"{key}: {value}")
                    
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")
    
    # Customer Risk Profiles Page
    elif page == "👥 Customer Risk Profiles":
        st.header("Customer Risk Profiles")
        
        if not st.session_state.analysis_complete:
            st.warning("⚠️ Please complete the data analysis first (Data Upload & Analysis page)")
        else:
            # Load customer profiles
            if os.path.exists('output/customer_profiles.csv'):
                profiles_df = pd.read_csv('output/customer_profiles.csv')
                
                st.markdown("### All Customer Profiles")
                
                # Filter options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    risk_filter = st.multiselect(
                        "Filter by Risk Level",
                        options=['HIGH', 'MEDIUM', 'LOW'],
                        default=['HIGH', 'MEDIUM', 'LOW']
                    )
                
                with col2:
                    sort_by = st.selectbox(
                        "Sort by",
                        ['risk_score', 'total_transactions', 'total_volume', 'customer_id']
                    )
                
                with col3:
                    ascending = st.checkbox("Ascending Order", value=False)
                
                # Apply filters
                filtered_df = profiles_df[profiles_df['risk_classification'].isin(risk_filter)]
                filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
                
                # Display statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Profiles", len(profiles_df))
                with col2:
                    st.metric("High Risk", len(profiles_df[profiles_df['risk_classification'] == 'HIGH']))
                with col3:
                    st.metric("Medium Risk", len(profiles_df[profiles_df['risk_classification'] == 'MEDIUM']))
                with col4:
                    st.metric("Low Risk", len(profiles_df[profiles_df['risk_classification'] == 'LOW']))
                
                # Display table
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    height=400
                )
                
                # Download button
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Customer Profiles CSV",
                    data=csv,
                    file_name="customer_profiles.csv",
                    mime="text/csv"
                )
                
                # Individual customer lookup
                st.markdown("---")
                st.markdown("### Lookup Individual Customer")
                
                account_id = st.text_input("Enter Account ID:")
                if st.button("🔍 Search", key="search_customer_btn"):
                    try:
                        profile = st.session_state.aml_system.get_customer_risk_profile(account_id)
                        
                        if isinstance(profile, dict):
                            st.success(f"Profile found for account: {account_id}")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("#### Account Information")
                                st.json(profile)
                            
                            with col2:
                                st.markdown("#### Risk Assessment")
                                risk_class = profile.get('risk_classification', 'UNKNOWN')
                                risk_score = profile.get('risk_score', 0)
                                
                                if risk_class == "HIGH":
                                    st.error(f"⚠️ HIGH RISK (Score: {risk_score:.2f})")
                                elif risk_class == "MEDIUM":
                                    st.warning(f"⚠️ MEDIUM RISK (Score: {risk_score:.2f})")
                                else:
                                    st.success(f"✅ LOW RISK (Score: {risk_score:.2f})")
                        else:
                            st.error(profile)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.error("Customer profiles not found. Please run the analysis first.")
    
    # Dashboard & Reports Page
    elif page == "📈 Dashboard & Reports":
        st.header("Dashboard & Reports")
        
        if not st.session_state.analysis_complete:
            st.warning("⚠️ Please complete the data analysis first (Data Upload & Analysis page)")
        else:
            st.markdown("### Executive Summary")
            
            # Generate and display summary
            summary = st.session_state.aml_system.generate_summary_report()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Transactions", f"{summary.get('total_transactions', 0):,}")
                st.metric("Suspicious Transactions", f"{summary.get('suspicious_transactions', 0):,}")
                st.metric("Suspicion Rate", f"{summary.get('suspicion_rate', 0):.2f}%")
            
            with col2:
                st.metric("Unique Accounts", f"{summary.get('unique_accounts', 0):,}")
                st.metric("High Risk Customers", summary.get('high_risk_customers', 'N/A'))
                st.metric("Medium Risk Customers", summary.get('medium_risk_customers', 'N/A'))
            
            with col3:
                st.metric("Low Risk Customers", summary.get('low_risk_customers', 'N/A'))
                st.metric("Total Volume", f"${summary.get('total_volume', 0):,.2f}")
                st.metric("Avg Transaction", f"${summary.get('avg_transaction_amount', 0):,.2f}")
            
            st.markdown("---")
            st.markdown("### Visualizations")
            
            # Display generated visualizations
            viz_files = [
                ('output/dashboard.png', 'Comprehensive Dashboard'),
                ('output/detailed_analysis.png', 'Detailed Analysis'),
                ('output/customer_profiles.png', 'Customer Profiles Analysis')
            ]
            
            for file_path, title in viz_files:
                if os.path.exists(file_path):
                    st.markdown(f"#### {title}")
                    st.image(file_path, use_container_width=True)
                    
                    # Download link
                    st.markdown(get_image_download_link(file_path, f"{title.replace(' ', '_')}.png"), 
                              unsafe_allow_html=True)
                    st.markdown("---")
                else:
                    st.info(f"{title} not available yet.")
            
            # Download reports
            st.markdown("### Download Reports")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if os.path.exists('output/customer_profiles.csv'):
                    with open('output/customer_profiles.csv', 'r') as f:
                        st.download_button(
                            label="📥 Download Customer Profiles CSV",
                            data=f,
                            file_name="customer_profiles.csv",
                            mime="text/csv"
                        )
            
            with col2:
                if os.path.exists('output/detected_anomalies.csv'):
                    with open('output/detected_anomalies.csv', 'r') as f:
                        st.download_button(
                            label="📥 Download Detected Anomalies CSV",
                            data=f,
                            file_name="detected_anomalies.csv",
                            mime="text/csv"
                        )
    
    # Model Management Page
    elif page == "💾 Model Management":
        st.header("Model Management")
        
        st.markdown("""
        Manage your trained machine learning models, view model information, 
        and perform model operations like training, saving, and loading.
        """)
        
        # Check if system is initialized
        if not st.session_state.data_loaded:
            st.warning("⚠️ Please load data first (Data Upload & Analysis page)")
        else:
            aml_system = st.session_state.aml_system
            
            # Model Status Section
            st.markdown("### 📊 Model Status")
            
            model_exists = os.path.exists('models/fraud_model.pkl')
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if model_exists:
                    st.success("✅ Model Available")
                else:
                    st.error("❌ No Model Found")
            
            with col2:
                if model_exists:
                    try:
                        # Load metadata
                        import joblib
                        metadata = joblib.load('models/model_metadata.pkl')
                        st.info(f"📅 Trained: {metadata.get('timestamp', 'Unknown')}")
                    except:
                        st.info("📅 Trained: Unknown")
                else:
                    st.info("📅 Not Trained")
            
            with col3:
                if model_exists:
                    try:
                        metadata = joblib.load('models/model_metadata.pkl')
                        st.info(f"🔢 Features: {metadata.get('feature_count', 'N/A')}")
                    except:
                        st.info("🔢 Features: N/A")
                else:
                    st.info("🔢 Features: N/A")
            
            # Model Information
            if model_exists:
                st.markdown("---")
                st.markdown("### 📋 Model Information")
                
                try:
                    import joblib
                    metadata = joblib.load('models/model_metadata.pkl')
                    metrics = metadata.get('model_metrics', {})
                    
                    if metrics:
                        st.markdown("#### Performance Metrics")
                        
                        # Display metrics for each model
                        for model_name, model_metrics in metrics.items():
                            with st.expander(f"📊 {model_name.replace('_', ' ').title()}"):
                                metric_cols = st.columns(4)
                                
                                with metric_cols[0]:
                                    st.metric("Accuracy", f"{model_metrics.get('accuracy', 0):.3f}")
                                with metric_cols[1]:
                                    st.metric("Precision", f"{model_metrics.get('precision', 0):.3f}")
                                with metric_cols[2]:
                                    st.metric("Recall", f"{model_metrics.get('recall', 0):.3f}")
                                with metric_cols[3]:
                                    st.metric("F1-Score", f"{model_metrics.get('f1_score', 0):.3f}")
                    
                    # Model Files
                    st.markdown("#### 📁 Model Files")
                    model_files = [
                        ('fraud_model.pkl', 'Trained ML Model'),
                        ('scaler.pkl', 'Feature Scaler'),
                        ('label_encoders.pkl', 'Categorical Encoders'),
                        ('feature_names.pkl', 'Feature Names'),
                        ('model_metadata.pkl', 'Model Metadata')
                    ]
                    
                    for filename, description in model_files:
                        filepath = os.path.join('models', filename)
                        if os.path.exists(filepath):
                            size = os.path.getsize(filepath) / 1024  # KB
                            st.text(f"✅ {filename} ({size:.2f} KB) - {description}")
                        else:
                            st.text(f"❌ {filename} - {description}")
                
                except Exception as e:
                    st.error(f"Error loading model information: {str(e)}")
            
            # Model Operations
            st.markdown("---")
            st.markdown("### 🔧 Model Operations")
            
            operation_tabs = st.tabs(["Train New Model", "Load Model", "Model Info", "Delete Model"])
            
            # Train New Model Tab
            with operation_tabs[0]:
                st.markdown("#### Train a New Model")
                st.info("Training will create a new model using the loaded transaction data.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    test_size = st.slider("Test Set Size", 0.1, 0.5, 0.3, 0.05)
                
                with col2:
                    save_model = st.checkbox("Save Model After Training", value=True)
                
                if st.button("🚀 Train Model", key="train_model_btn"):
                    try:
                        with st.spinner("Training model... This may take a few minutes."):
                            # Train the model
                            model = aml_system.ml_predictor.train_compliance_model(
                                test_size=test_size,
                                save_model=save_model
                            )
                        
                        st.success("✅ Model trained successfully!")
                        
                        # Display metrics
                        if aml_system.ml_predictor.model_metrics:
                            st.markdown("#### Training Results")
                            metrics = aml_system.ml_predictor.model_metrics
                            
                            for model_name, model_metrics in metrics.items():
                                st.markdown(f"**{model_name.replace('_', ' ').title()}**")
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("Accuracy", f"{model_metrics.get('accuracy', 0):.3f}")
                                with col2:
                                    st.metric("Precision", f"{model_metrics.get('precision', 0):.3f}")
                                with col3:
                                    st.metric("Recall", f"{model_metrics.get('recall', 0):.3f}")
                                with col4:
                                    st.metric("F1-Score", f"{model_metrics.get('f1_score', 0):.3f}")
                        
                        st.balloons()
                    
                    except Exception as e:
                        st.error(f"Error training model: {str(e)}")
            
            # Load Model Tab
            with operation_tabs[1]:
                st.markdown("#### Load Existing Model")
                st.info("Load a previously trained model from disk.")
                
                if not model_exists:
                    st.warning("⚠️ No saved model found in the models/ directory.")
                else:
                    if st.button("📂 Load Model from Disk", key="load_model_btn"):
                        try:
                            with st.spinner("Loading model..."):
                                success = aml_system.ml_predictor.load_model_from_disk()
                            
                            if success:
                                st.success("✅ Model loaded successfully!")
                                st.info("The system is now ready for predictions.")
                            else:
                                st.error("Failed to load model.")
                        
                        except Exception as e:
                            st.error(f"Error loading model: {str(e)}")
            
            # Model Info Tab
            with operation_tabs[2]:
                st.markdown("#### Detailed Model Information")
                
                if not model_exists:
                    st.warning("⚠️ No model available. Train a model first.")
                else:
                    try:
                        import joblib
                        
                        # Load all model artifacts
                        st.markdown("**Model Architecture:**")
                        model = joblib.load('models/fraud_model.pkl')
                        st.code(str(type(model).__name__))
                        
                        st.markdown("**Feature Names:**")
                        feature_names = joblib.load('models/feature_names.pkl')
                        st.write(f"Total Features: {len(feature_names)}")
                        
                        with st.expander("View All Features"):
                            for i, feat in enumerate(feature_names, 1):
                                st.text(f"{i}. {feat}")
                        
                        st.markdown("**Label Encoders:**")
                        encoders = joblib.load('models/label_encoders.pkl')
                        st.write(f"Total Encoders: {len(encoders)}")
                        
                        with st.expander("View Encoded Features"):
                            for feature, encoder in encoders.items():
                                st.text(f"• {feature}: {len(encoder.classes_)} classes")
                        
                        st.markdown("**Model Metadata:**")
                        metadata = joblib.load('models/model_metadata.pkl')
                        st.json(metadata)
                    
                    except Exception as e:
                        st.error(f"Error loading model details: {str(e)}")
            
            # Delete Model Tab
            with operation_tabs[3]:
                st.markdown("#### Delete Model")
                st.warning("⚠️ This will permanently delete all model files. This action cannot be undone.")
                
                if not model_exists:
                    st.info("No model to delete.")
                else:
                    confirm_delete = st.checkbox("I understand this will delete all model files")
                    
                    if confirm_delete:
                        if st.button("🗑️ Delete Model", key="delete_model_btn", type="primary"):
                            try:
                                import shutil
                                
                                # Delete all model files
                                if os.path.exists('models'):
                                    for file in os.listdir('models'):
                                        file_path = os.path.join('models', file)
                                        if os.path.isfile(file_path):
                                            os.remove(file_path)
                                
                                st.success("✅ Model files deleted successfully!")
                                st.info("You can train a new model in the 'Train New Model' tab.")
                                
                                # Reset the page
                                st.rerun()
                            
                            except Exception as e:
                                st.error(f"Error deleting model: {str(e)}")
            
            # Model Performance Monitoring
            if model_exists:
                st.markdown("---")
                st.markdown("### 📈 Model Performance Monitoring")
                
                st.info("💡 Tip: Retrain your model periodically with new data to maintain accuracy.")
                
                try:
                    import joblib
                    metadata = joblib.load('models/model_metadata.pkl')
                    timestamp_str = metadata.get('timestamp', '')
                    
                    if timestamp_str:
                        from datetime import datetime
                        training_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                        days_since_training = (datetime.now() - training_date).days
                        
                        if days_since_training > 30:
                            st.warning(f"⚠️ Model was trained {days_since_training} days ago. Consider retraining with recent data.")
                        elif days_since_training > 7:
                            st.info(f"ℹ️ Model was trained {days_since_training} days ago.")
                        else:
                            st.success(f"✅ Model is recent ({days_since_training} days old).")
                
                except Exception as e:
                    st.error(f"Error checking model age: {str(e)}")
    
    # About Page
    elif page == "ℹ️ About":
        st.header("About the Fraud Management System")
        
        st.markdown("""
        ### 🛡️ Overview
        
        The Fraud Management System is a comprehensive AI-powered platform designed to help financial 
        institutions detect and prevent fraudulent activities. It combines machine learning, 
        anomaly detection, and risk profiling to provide real-time fraud monitoring.
        
        ### 🎯 Key Features
        
        - **Customer Risk Profiling**: Comprehensive risk assessment based on transaction patterns
        - **Anomaly Detection**: Multi-algorithm approach using Isolation Forest and statistical methods
        - **Machine Learning**: Predictive models for compliance risk forecasting
        - **Interactive Dashboards**: Real-time visualization and comprehensive reports
        - **Real-time Prediction**: Risk assessment for new transactions
        
        ### 🔧 Technology Stack
        
        **Model Persistence & Serialization:**
        - **Joblib** (v1.3.0+) - Optimized model serialization for scikit-learn, better compression, recommended for production
        - **Python pickle** - Built-in object serialization (fallback), standard Python protocol
        
        **Frontend & Web Framework:**
        - **Streamlit** (v1.30.0+) - Interactive web application framework with model management UI
        
        **Data Processing & Analysis:**
        - **Pandas** (v2.0.0+) - Data manipulation and analysis
        - **NumPy** (v1.24.0+) - Numerical computing
        - **Python-dateutil** (v2.8.0+) - Date/time utilities
        
        **Machine Learning & AI:**
        - **Scikit-learn** (v1.3.0+) - ML algorithms (Random Forest, Isolation Forest, GradientBoosting, etc.)
        
        **Data Visualization:**
        - **Matplotlib** (v3.7.0+) - Static plotting library
        - **Seaborn** (v0.12.0+) - Statistical data visualization
        - **Pillow** (v10.0.0+) - Image processing
        
        **Runtime & Deployment:**
        - **Python** (v3.8+) - Programming language
        - **Docker** - Containerization with persistent model volumes
        
        **Optional Deep Learning (Available):**
        - **TensorFlow** (v2.13.0+) - Deep learning framework with SavedModel format
        - **Keras** (v2.13.0+) - Neural network API with h5 format support
        
        **Performance:**
        - Save Time: < 2 seconds | Load Time: < 1 second | File Size: 5-50 MB
        
        ### 📊 Modules
        
        1. **Data Manager**: Handles data loading and preprocessing
        2. **Customer Profiler**: Analyzes customer behavior and risk patterns
        3. **Anomaly Detector**: Identifies suspicious transactions
        4. **ML Predictor**: Trains and deploys predictive models
        5. **Visualizer**: Creates comprehensive reports and dashboards
        
        ### 📖 How to Use
        
        1. Navigate to **Data Upload & Analysis** to load your transaction data
        2. Run the complete analysis to process the data
        3. View the **Dashboard & Reports** for comprehensive insights
        4. Use **Transaction Risk Prediction** to assess new transactions
        5. Check **Customer Risk Profiles** for detailed customer analysis
        
        ###  Academic Project
        
        This project is submitted as part of the **Final Semester Dissertation Project** for the **Master of Technology (MTech) in Artificial Intelligence and Machine Learning (AIML)** degree at **Birla Institute of Technology and Science (BITS), Pilani**.
        
        **Institution**: BITS Pilani  
        **Program**: MTech in AIML  
        **Project Type**: Dissertation Project  
        **Academic Year**: 2025-2026
        
        ---
        
        **Version**: 1.0.0  
        **Last Updated**: January 2026
        """)

if __name__ == "__main__":
    main()
