"""
Unit Tests for Fraud Management System
=====================================

Basic tests for the system modules.
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.data_manager import DataManager


class TestDataManager(unittest.TestCase):
    """Test cases for DataManager module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data_manager = DataManager()
    
    def test_initialization(self):
        """Test DataManager initialization"""
        self.assertIsNone(self.data_manager.df)
    
    def test_synthetic_data_generation(self):
        """Test synthetic data generation"""
        df = self.data_manager._generate_synthetic_data(n_transactions=100)
        
        # Check if dataframe is created
        self.assertIsNotNone(df)
        
        # Check number of rows
        self.assertEqual(len(df), 100)
        
        # Check required columns exist
        required_columns = ['Time', 'Date', 'Sender_account', 'Receiver_account',
                          'Amount', 'Payment_currency', 'Received_currency']
        for col in required_columns:
            self.assertIn(col, df.columns)
    
    def test_transaction_amount_generation(self):
        """Test transaction amount generation"""
        # Test legitimate transaction
        amount_legit = self.data_manager._generate_transaction_amount(is_laundering=False)
        self.assertGreater(amount_legit, 0)
        
        # Test suspicious transaction
        amount_suspicious = self.data_manager._generate_transaction_amount(is_laundering=True)
        self.assertGreater(amount_suspicious, 0)


class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_system_initialization(self):
        """Test if system can be initialized"""
        from aml_system import AMLComplianceSystem
        
        system = AMLComplianceSystem()
        self.assertIsNone(system.df)
        self.assertIsNone(system.data_manager)


if __name__ == '__main__':
    unittest.main()
