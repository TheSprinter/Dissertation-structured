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

# Custom CSS for modern UI styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }
    
    /* Header with Glassmorphism */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        animation: fadeInDown 0.8s ease-in-out;
    }
    
    /* Modern Card Design with Glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 48px rgba(31, 38, 135, 0.25);
    }
    
    .metric-card h3 {
        color: #1a202c;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    .metric-card ul {
        list-style: none;
        padding: 0;
    }
    
    .metric-card li {
        padding: 0.6rem 0;
        color: #4a5568;
        font-size: 1rem;
        position: relative;
        padding-left: 1.5rem;
    }
    
    .metric-card li::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #667eea;
        font-weight: bold;
    }
    
    /* Risk Labels with Modern Design */
    .risk-high {
        color: #DC2626;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        background: rgba(220, 38, 38, 0.1);
        border-radius: 8px;
        display: inline-block;
    }
    
    .risk-medium {
        color: #F59E0B;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        background: rgba(245, 158, 11, 0.1);
        border-radius: 8px;
        display: inline-block;
    }
    
    .risk-low {
        color: #10B981;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 8px;
        display: inline-block;
    }
    
    /* Modern Button Styles */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 1rem;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
    }
    
    [data-testid="stSidebar"] .css-17eq0hr {
        color: white;
    }
    
    /* Metric Containers */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stNumberInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Data Tables */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Info/Warning/Success Boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 12px;
        font-weight: 600;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px dashed #cbd5e0;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Radio Buttons */
    .stRadio>div {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        background: rgba(255, 255, 255, 0.8);
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
    
    # Model Management Section in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Quick Actions")
    
    if st.session_state.data_loaded:
        if st.sidebar.button("📋 List Saved Models"):
            aml_system = st.session_state.aml_system
            with st.sidebar:
                aml_system.list_available_models()
    
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
                        st.metric("Unique Accounts", 
                                f"{len(set(df['Sender_account']) | set(df['Receiver_account'])):,}")
                    with col3:
                        st.metric("Total Volume", f"${df['Amount'].sum():,.2f}")
                    with col4:
                        st.metric("Avg Transaction", f"${df['Amount'].mean():,.2f}")
                    
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
            
            col1, col2 = st.columns(2)
            
            with col1:
                time = st.text_input("Time (HH:MM:SS)", "14:30:00")
                date = st.date_input("Date")
                sender_account = st.text_input("Sender Account", "ACC0001")
                receiver_account = st.text_input("Receiver Account", "ACC0002")
                amount = st.number_input("Amount ($)", min_value=0.0, value=5000.0, step=100.0)
            
            with col2:
                payment_currency = st.selectbox("Payment Currency", 
                    ["USD", "EUR", "GBP", "AED", "CHF", "JPY", "CNY"])
                received_currency = st.selectbox("Received Currency", 
                    ["USD", "EUR", "GBP", "AED", "CHF", "JPY", "CNY"])
                sender_location = st.text_input("Sender Bank Location", "US-NY")
                receiver_location = st.text_input("Receiver Bank Location", "AE-DXB")
                payment_type = st.selectbox("Payment Type", 
                    ["Wire", "ACH", "Check", "Card", "Cash", "Crypto"])
            
            if st.button("🎯 Predict Risk", key="predict_btn"):
                transaction = {
                    'Time': time,
                    'Date': str(date),
                    'Sender_account': sender_account,
                    'Receiver_account': receiver_account,
                    'Amount': amount,
                    'Payment_currency': payment_currency,
                    'Received_currency': received_currency,
                    'Sender_bank_location': sender_location,
                    'Receiver_bank_location': receiver_location,
                    'Payment_type': payment_type
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
                        ['risk_score', 'transaction_count', 'total_volume', 'account']
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
        Manage your trained machine learning models. Save, load, and track model versions 
        for easy deployment and reuse.
        """)
        
        if not st.session_state.data_loaded:
            st.warning("⚠️ Please load data first from the 'Data Upload & Analysis' page.")
        else:
            aml_system = st.session_state.aml_system
            
            # Create tabs for different model operations
            tab1, tab2, tab3 = st.tabs(["📋 View Models", "💾 Save Model", "📂 Load Model"])
            
            with tab1:
                st.subheader("Available Saved Models")
                
                if st.button("🔄 Refresh Model List"):
                    models = aml_system.list_available_models()
                    if models:
                        st.success(f"Found {len(models)} model(s)")
                    else:
                        st.info("No saved models found")
                
                st.markdown("""
                **Model Storage Location**: `models/` directory
                
                Models are saved with all preprocessing components including:
                - Trained model
                - Feature scaler
                - Label encoders
                - Feature names
                - Model metrics
                - Timestamp
                """)
            
            with tab2:
                st.subheader("Save Trained Model")
                
                if st.session_state.analysis_complete:
                    st.info("Current model is ready to be saved")
                    
                    model_name = st.text_input("Model Name (optional)", 
                                              value="ml_package.pkl",
                                              help="Enter a custom name or use default")
                    
                    if not model_name.endswith('.pkl'):
                        model_name += '.pkl'
                    
                    model_path = f"models/{model_name}"
                    
                    if st.button("💾 Save Model"):
                        with st.spinner("Saving model..."):
                            success = aml_system.save_trained_model(model_path)
                            if success:
                                st.success(f"✅ Model saved successfully to `{model_path}`")
                                st.balloons()
                            else:
                                st.error("❌ Failed to save model")
                else:
                    st.warning("⚠️ No trained model available. Please run the analysis first.")
                    if st.button("▶️ Run Analysis Now"):
                        st.experimental_rerun()
            
            with tab3:
                st.subheader("Load Pre-trained Model")
                
                st.markdown("""
                Load a previously trained model to make predictions without retraining.
                """)
                
                # Option to use default or custom path
                load_option = st.radio("Select loading option:", 
                                      ["Load default model", "Load custom model"])
                
                model_to_load = None
                
                if load_option == "Load default model":
                    model_to_load = "models/ml_package.pkl"
                    st.info(f"Will load: `{model_to_load}`")
                else:
                    custom_path = st.text_input("Enter model path:", 
                                               value="models/ml_package.pkl")
                    model_to_load = custom_path
                
                if st.button("📂 Load Model"):
                    with st.spinner(f"Loading model from {model_to_load}..."):
                        success = aml_system.load_pretrained_model(model_to_load)
                        if success:
                            st.success("✅ Model loaded successfully!")
                            st.session_state.analysis_complete = True
                            st.info("Model is now ready for predictions. Go to 'Transaction Risk Prediction' page.")
                        else:
                            st.error(f"❌ Failed to load model from `{model_to_load}`")
                            st.info("Make sure the model file exists in the specified path.")
    
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
        
        - **Frontend**: Streamlit
        - **ML/AI**: Scikit-learn, Pandas, NumPy
        - **Visualization**: Matplotlib, Seaborn
        - **Data Processing**: Python 3.8+
        
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
        
        ### 📞 Support
        
        For questions or support, please refer to the documentation or contact the development team.
        
        ### 📄 Academic Project
        
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
