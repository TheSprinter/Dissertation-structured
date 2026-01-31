"""
Data Manager Module
===================

Handles data loading, validation, and synthetic data generation.
"""

import pandas as pd
import numpy as np


class DataManager:
    """Handles data loading, validation, and synthetic data generation"""
    
    def __init__(self):
        self.df = None
        
    def load_data(self, data_path):
        """Load transaction data from CSV file or generate synthetic data"""
        print("\n" + "="*60)
        print("LOADING TRANSACTION DATA")
        print("="*60)
        
        try:
            # Handle Google Drive links
            if 'drive.google.com' in str(data_path):
                file_id = data_path.split('/d/')[1].split('/')[0]
                data_path = f'https://drive.google.com/uc?id={file_id}'

            self.df = pd.read_csv(data_path)
            
            # Data validation - New dataset columns
            required_columns = ['transaction_id', 'customer_id', 'transaction_amount', 
                              'transaction_date', 'merchant_id', 'merchant_category',
                              'payment_method', 'transaction_type', 'card_type',
                              'location', 'device_type', 'ip_country', 'is_fraud']

            missing_cols = set(required_columns) - set(self.df.columns)
            if missing_cols:
                print(f"⚠ Warning: Missing columns: {missing_cols}")

            self._display_data_summary()
            return self.df

        except Exception as e:
            print(f"⚠ Error loading data: {e}")
            print("📝 Generating synthetic data for demonstration...")
            self.df = self._generate_synthetic_data()
            return self.df
    
    def _display_data_summary(self):
        """Display comprehensive data summary"""
        print(f"✓ Dataset loaded successfully!")
        print(f"  • Total Transactions: {len(self.df):,}")
        print(f"  • Columns: {len(self.df.columns)} columns")
        print(f"  • Date Range: {self.df['transaction_date'].min()} to {self.df['transaction_date'].max()}")
        fraud_count = self.df['is_fraud'].sum() if 'is_fraud' in self.df.columns else 0
        print(f"  • Fraudulent Transactions: {fraud_count:,} ({fraud_count/len(self.df)*100:.2f}%)")
        
        print(f"\n📊 Sample Data:")
        print(self.df.head())
    
    def _generate_synthetic_data(self, n_transactions=1000):
        """Generate synthetic transaction data for testing - New Schema"""
        np.random.seed(42)
        
        print(f"🔄 Generating {n_transactions} synthetic transactions...")
        
        # Define data parameters
        merchants = [f'MERCH{str(i).zfill(4)}' for i in range(1, 101)]
        merchant_categories = ['Electronics', 'Grocery', 'Restaurant', 'Travel', 'Healthcare',
                             'Entertainment', 'Utilities', 'Fashion', 'Home', 'Sports']
        payment_methods = ['Credit Card', 'Debit Card', 'Digital Wallet', 'Bank Transfer', 'Cryptocurrency']
        transaction_types = ['Purchase', 'Cash Withdrawal', 'Transfer', 'Payment']
        card_types = ['Visa', 'Mastercard', 'American Express', 'Discover']
        device_types = ['Mobile', 'Desktop', 'Tablet']
        countries = ['US', 'UK', 'IN', 'AE', 'CN', 'SG', 'JP', 'DE', 'FR', 'AU']
        
        data = []
        base_date = pd.Timestamp(2024, 1, 1)
        
        for i in range(n_transactions):
            # 5% fraud probability
            is_fraud = np.random.random() < 0.05
            
            # Generate transaction data
            transaction_date = base_date + pd.Timedelta(days=np.random.randint(0, 365))
            transaction_hour = np.random.randint(0, 24)
            
            # Amount patterns based on fraud
            if is_fraud:
                amount = np.random.choice([
                    np.random.randint(9000, 10000),   # Structuring
                    np.random.randint(50000, 200000), # Large suspicious
                    np.random.randint(1000, 15000)    # Smurfing
                ], p=[0.4, 0.3, 0.3])
            else:
                amount = np.random.choice([
                    np.random.randint(10, 500),      # Small
                    np.random.randint(500, 5000),    # Medium
                    np.random.randint(5000, 50000)   # Large legitimate
                ], p=[0.6, 0.3, 0.1])
            
            transaction = {
                'transaction_id': f'TXN{str(i).zfill(7)}',
                'customer_id': f'CUST{str(np.random.randint(1, 10000)).zfill(5)}',
                'transaction_amount': round(amount, 2),
                'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                'transaction_time': f'{transaction_hour:02d}:{np.random.randint(0, 60):02d}:{np.random.randint(0, 60):02d}',
                'merchant_category': np.random.choice(merchant_categories),
                'merchant_id': np.random.choice(merchants),
                'merchant_reputation': np.random.choice(['High', 'Medium', 'Low'], p=[0.7, 0.2, 0.1]),
                'transaction_type': np.random.choice(transaction_types),
                'payment_method': np.random.choice(payment_methods),
                'location': np.random.choice(countries),
                'device_type': np.random.choice(device_types),
                'ip_address': f'{np.random.randint(0, 256)}.{np.random.randint(0, 256)}.{np.random.randint(0, 256)}.{np.random.randint(0, 256)}',
                'ip_country': np.random.choice(countries),
                'billing_country': np.random.choice(countries),
                'shipping_country': np.random.choice(countries),
                'card_type': np.random.choice(card_types),
                'card_present': np.random.choice([0, 1], p=[0.7, 0.3]),
                'cvv_match': np.random.choice([0, 1], p=[0.05 if is_fraud else 0.01, 0.95 if is_fraud else 0.99]),
                'customer_age': np.random.randint(18, 80),
                'account_age_days': np.random.randint(1, 7300),
                'previous_transactions_24h': np.random.randint(0, 20),
                'previous_transactions_7d': np.random.randint(0, 100),
                'previous_transactions_30d': np.random.randint(0, 300),
                'avg_transaction_amount': round(np.random.uniform(100, 5000), 2),
                'transaction_hour': transaction_hour,
                'is_weekend': 1 if transaction_date.weekday() >= 5 else 0,
                'is_holiday': np.random.choice([0, 1], p=[0.95, 0.05]),
                'distance_from_home_km': round(np.random.exponential(scale=50), 2),
                'distance_from_last_transaction_km': round(np.random.exponential(scale=30), 2),
                'failed_login_attempts': np.random.randint(0, 5 if is_fraud else 2),
                'session_id': f'SESS{str(np.random.randint(1, 100000)).zfill(6)}',
                'session_duration_seconds': np.random.randint(60, 3600),
                'num_page_views': np.random.randint(1, 50),
                'time_since_last_transaction_minutes': np.random.randint(1, 10080),
                'same_merchant_last_30d': np.random.randint(0, 50),
                'num_unique_merchants_30d': np.random.randint(1, 100),
                'num_locations_7d': np.random.randint(1, 10),
                'transaction_currency': np.random.choice(['USD', 'EUR', 'GBP', 'INR', 'AED', 'CNY', 'SGD']),
                'billing_currency': np.random.choice(['USD', 'EUR', 'GBP', 'INR', 'AED', 'CNY', 'SGD']),
                'currency_mismatch': np.random.choice([0, 1], p=[0.7, 0.3]),
                'velocity_score': round(np.random.uniform(0, 100), 2),
                'email_verified': np.random.choice([0, 1], p=[0.1 if is_fraud else 0.02, 0.9 if is_fraud else 0.98]),
                'phone_verified': np.random.choice([0, 1], p=[0.15 if is_fraud else 0.05, 0.85 if is_fraud else 0.95]),
                'shipping_address_verified': np.random.choice([0, 1], p=[0.2 if is_fraud else 0.05, 0.8 if is_fraud else 0.95]),
                'is_fraud': 1 if is_fraud else 0
            }
            data.append(transaction)
        
        df = pd.DataFrame(data)
        print(f"✓ Synthetic data generated: {len(df)} transactions")
        return df
