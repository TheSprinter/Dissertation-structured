"""
Customer Profiler Module
========================

Handles customer risk profiling and classification.
"""

import pandas as pd
import os
from config import OUTPUT_DIR


class CustomerProfiler:
    """Handles customer risk profiling and classification"""
    
    def __init__(self, df):
        self.df = df
        self.profiles = None
        
    def analyze_customers(self, save_results=True):
        """Perform comprehensive customer risk profiling"""
        print("\n" + "="*60)
        print("CUSTOMER PROFILING AND RISK ASSESSMENT")
        print("="*60)
        
        profiles = {}
        all_customers = self.df['customer_id'].unique()
        
        for customer in all_customers:
            profile = self._create_customer_profile(customer)
            if profile:
                profiles[customer] = profile
        
        # Calculate risk scores and classifications
        profile_list = self._calculate_risk_scores(profiles)
        
        # Store results
        self.profiles = pd.DataFrame(profile_list)
        
        # Display results
        self._display_profiling_results()
        
        if save_results:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            out_path = os.path.join(OUTPUT_DIR, 'customer_profiles.csv')
            self.profiles.to_csv(out_path, index=False)
            print(f" Customer profiles saved to {out_path}")
        
        return self.profiles
    
    def _create_customer_profile(self, customer):
        """Create detailed profile for a single customer"""
        customer_txns = self.df[self.df['customer_id'] == customer]
        
        if len(customer_txns) == 0:
            return None
            
        return {
            'customer_id': customer,
            'total_transactions': len(customer_txns),
            'total_volume': customer_txns['transaction_amount'].sum(),
            'avg_transaction': customer_txns['transaction_amount'].mean(),
            'max_transaction': customer_txns['transaction_amount'].max(),
            'min_transaction': customer_txns['transaction_amount'].min(),
            'fraudulent_transactions': customer_txns['is_fraud'].sum(),
            'cross_border_count': (customer_txns['billing_country'] != customer_txns['shipping_country']).sum(),
            'high_risk_countries': self._count_high_risk_locations(customer_txns),
            'structuring_indicators': ((customer_txns['transaction_amount'] >= 9000) & 
                                     (customer_txns['transaction_amount'] < 10000)).sum(),
            'rapid_transactions': self._count_rapid_transactions(customer_txns),
            'currencies_used': customer_txns['transaction_currency'].nunique(),
            'payment_methods_used': customer_txns['payment_method'].nunique(),
            'unique_merchants': customer_txns['merchant_id'].nunique(),
            'customer_age': customer_txns['customer_age'].iloc[0] if 'customer_age' in customer_txns.columns else 0,
            'account_age_days': customer_txns['account_age_days'].iloc[0] if 'account_age_days' in customer_txns.columns else 0,
            'unverified_transactions': ((customer_txns['email_verified'] == 0) | 
                                       (customer_txns['phone_verified'] == 0)).sum()
        }
    
    def _count_high_risk_locations(self, transactions):
        """Count transactions involving high-risk countries"""
        high_risk = ['AE', 'CN', 'RU'] # Example high-risk countries
        return ((transactions['billing_country'].isin(high_risk)) | 
                (transactions['shipping_country'].isin(high_risk))).sum()
    
    def _count_rapid_transactions(self, transactions):
        """Count rapid succession transactions (same day)"""
        if len(transactions) < 2:
            return 0
        return transactions.groupby('transaction_date').size().max() - 1
    
    def _calculate_risk_scores(self, profiles):
        """Calculate risk scores for all customer profiles"""
        profile_list = []
        
        for customer_id, profile in profiles.items():
            # Calculate normalized risk score (0-100)
            risk_factors = []
            
            # Fraudulent transaction ratio
            fraud_ratio = profile['fraudulent_transactions'] / max(profile['total_transactions'], 1)
            risk_factors.append(fraud_ratio * 30)
            
            # High amount transactions
            if profile['avg_transaction'] > 50000:
                risk_factors.append(20)
            elif profile['avg_transaction'] > 20000:
                risk_factors.append(10)
                
            # Cross-border activity
            cross_border_ratio = profile['cross_border_count'] / max(profile['total_transactions'], 1)
            risk_factors.append(cross_border_ratio * 20)
            
            # High-risk countries
            risk_factors.append(min(profile['high_risk_countries'] * 5, 15))
            
            # Structuring indicators
            risk_factors.append(min(profile['structuring_indicators'] * 10, 15))
            
            # Unverified transactions
            unverified_ratio = profile['unverified_transactions'] / max(profile['total_transactions'], 1)
            risk_factors.append(unverified_ratio * 10)
            
            # Calculate final risk score
            risk_score = min(sum(risk_factors), 100)
            
            # Risk classification
            if risk_score >= 70:
                risk_class = 'HIGH'
            elif risk_score >= 40:
                risk_class = 'MEDIUM'
            else:
                risk_class = 'LOW'
            
            profile['risk_score'] = risk_score
            profile['risk_classification'] = risk_class
            profile_list.append(profile)
        
        return profile_list
    
    def _display_profiling_results(self):
        """Display customer profiling analysis results"""
        print(f" Customer profiling completed for {len(self.profiles)} customers")
        
        # Risk distribution
        risk_dist = self.profiles['risk_classification'].value_counts()
        print(f"\n Risk Distribution:")
        for risk, count in risk_dist.items():
            percentage = count / len(self.profiles) * 100
            print(f" {risk}: {count} ({percentage:.1f}%)")
        
        # Top 5 highest risk customers
        print(f"\n Top 5 Highest Risk Customers:")
        top_risk = self.profiles.nlargest(5, 'risk_score')[['customer_id', 'risk_score', 'risk_classification', 'fraudulent_transactions']]
        print(top_risk.to_string(index=False))
