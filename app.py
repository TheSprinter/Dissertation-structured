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
        "ℹ️ About"
    ])
    
    # Home Page
    if page == "🏠 Home":
        st.header("Welcome to the Fraud Management System")
        
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
        
        ### 📄 License
        
        This system is developed for educational and research purposes.
        
        ---
        
        **Version**: 1.0.0  
        **Last Updated**: January 2026
        """)

if __name__ == "__main__":
    main()
