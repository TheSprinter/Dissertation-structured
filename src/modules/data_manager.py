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
            
            # Data validation
            required_columns = ['Time', 'Date', 'Sender_account', 'Receiver_account',
                              'Amount', 'Payment_currency', 'Received_currency',
                              'Sender_bank_location', 'Receiver_bank_location',
                              'Payment_type', 'Is_laundering', 'Laundering_type']

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
        print(f"  • Columns: {list(self.df.columns)}")
        print(f"  • Date Range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        print(f"  • Suspicious Transactions: {self.df['Is_laundering'].sum():,} ({self.df['Is_laundering'].sum()/len(self.df)*100:.2f}%)")
        
        print(f"\n📊 Sample Data:")
        print(self.df.head())
    
    def _generate_synthetic_data(self, n_transactions=1000):
        """Generate synthetic transaction data for testing"""
        np.random.seed(42)
        
        print(f"🔄 Generating {n_transactions} synthetic transactions...")
        
        # Define data parameters
        customers = [f'ACC{str(i).zfill(4)}' for i in range(1, 21)]
        banks = ['US-NY', 'UK-LDN', 'SG-SGP', 'AE-DXB', 'CH-ZRH', 'HK-HKG',
                'JP-TYO', 'DE-BER', 'FR-PAR', 'AU-SYD']
        currencies = ['USD', 'EUR', 'GBP', 'AED', 'CHF', 'SGD', 'JPY', 'AUD']
        payment_types = ['Wire', 'ACH', 'Card', 'Crypto', 'Cash', 'Check']
        laundering_types = ['None', 'Structuring', 'Smurfing', 'Trade-based',
                          'Shell-company', 'Round-tripping']

        data = []
        for i in range(n_transactions):
            # 15% laundering probability
            is_laundering = np.random.random() < 0.15

            # Amount patterns based on laundering type
            amount = self._generate_transaction_amount(is_laundering)
            
            sender = np.random.choice(customers)
            receiver = np.random.choice([c for c in customers if c != sender])

            transaction = {
                'Time': f"{np.random.randint(0, 24):02d}:{np.random.randint(0, 60):02d}:{np.random.randint(0, 60):02d}",
                'Date': pd.Timestamp(2024, np.random.randint(1, 13), np.random.randint(1, 29)).strftime('%Y-%m-%d'),
                'Sender_account': sender,
                'Receiver_account': receiver,
                'Amount': amount,
                'Payment_currency': np.random.choice(currencies),
                'Received_currency': np.random.choice(currencies),
                'Sender_bank_location': np.random.choice(banks),
                'Receiver_bank_location': np.random.choice(banks),
                'Payment_type': np.random.choice(payment_types, p=[0.35, 0.25, 0.15, 0.10, 0.10, 0.05]),
                'Is_laundering': 1 if is_laundering else 0,
                'Laundering_type': np.random.choice(laundering_types[1:]) if is_laundering else 'None'
            }
            data.append(transaction)

        df = pd.DataFrame(data)
        print(f"✓ Synthetic data generated: {len(df)} transactions")
        return df
    
    def _generate_transaction_amount(self, is_laundering):
        """Generate realistic transaction amounts based on laundering patterns"""
        if is_laundering:
            if np.random.random() < 0.4:
                return np.random.randint(9000, 10000)  # Structuring
            elif np.random.random() < 0.3:
                return np.random.randint(50000, 200000)  # Large suspicious
            else:
                return np.random.randint(1000, 15000)  # Smurfing
        else:
            return np.random.choice([
                np.random.randint(100, 5000),    # Small
                np.random.randint(5000, 30000),  # Medium
                np.random.randint(30000, 100000) # Large legitimate
            ], p=[0.6, 0.3, 0.1])
