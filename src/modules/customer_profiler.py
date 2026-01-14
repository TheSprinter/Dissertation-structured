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
        all_accounts = set(self.df['Sender_account'].unique()) | set(self.df['Receiver_account'].unique())
        
        for account in all_accounts:
            profile = self._create_customer_profile(account)
            if profile:
                profiles[account] = profile
        
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
            print(f"💾 Customer profiles saved to {out_path}")
        
        return self.profiles
    
    def _create_customer_profile(self, account):
        """Create detailed profile for a single customer"""
        sent_txns = self.df[self.df['Sender_account'] == account]
        recv_txns = self.df[self.df['Receiver_account'] == account]
        all_txns = pd.concat([sent_txns, recv_txns])
        
        if len(all_txns) == 0:
            return None
            
        return {
            'account': account,
            'total_transactions': len(all_txns),
            'sent_transactions': len(sent_txns),
            'received_transactions': len(recv_txns),
            'total_volume': all_txns['Amount'].sum(),
            'sent_volume': sent_txns['Amount'].sum(),
            'received_volume': recv_txns['Amount'].sum(),
            'avg_transaction': all_txns['Amount'].mean(),
            'max_transaction': all_txns['Amount'].max(),
            'min_transaction': all_txns['Amount'].min(),
            'suspicious_transactions': all_txns['Is_laundering'].sum(),
            'cross_border_count': self._count_cross_border_transactions(sent_txns, recv_txns),
            'high_risk_countries': self._count_high_risk_locations(all_txns),
            'structuring_indicators': self._count_structuring(all_txns),
            'rapid_transactions': self._count_rapid_transactions(all_txns),
            'currencies_used': all_txns['Payment_currency'].nunique(),
            'payment_types_used': all_txns['Payment_type'].nunique(),
            'unique_counterparties': self._count_unique_counterparties(sent_txns, recv_txns)
        }
    
    def _count_cross_border_transactions(self, sent_txns, recv_txns):
        """Count cross-border transactions"""
        cross_border_sent = (sent_txns['Sender_bank_location'] != sent_txns['Receiver_bank_location']).sum()
        cross_border_recv = (recv_txns['Sender_bank_location'] != recv_txns['Receiver_bank_location']).sum()
        return cross_border_sent + cross_border_recv
    
    def _count_high_risk_locations(self, transactions):
        """Count transactions involving high-risk countries"""
        high_risk = ['AE-DXB', 'HK-HKG']  # Example high-risk locations
        return ((transactions['Sender_bank_location'].isin(high_risk)) | 
                (transactions['Receiver_bank_location'].isin(high_risk))).sum()
    
    def _count_structuring(self, transactions):
        """Identify potential structuring patterns"""
        return ((transactions['Amount'] >= 9000) & (transactions['Amount'] < 10000)).sum()
    
    def _count_rapid_transactions(self, transactions):
        """Count rapid succession transactions (same day)"""
        if len(transactions) < 2:
            return 0
        return transactions.groupby('Date').size().max() - 1
    
    def _count_unique_counterparties(self, sent_txns, recv_txns):
        """Count unique counterparties"""
        sent_counterparties = set(sent_txns['Receiver_account'].unique())
        recv_counterparties = set(recv_txns['Sender_account'].unique())
        return len(sent_counterparties | recv_counterparties)
    
    def _calculate_risk_scores(self, profiles):
        """Calculate risk scores for all customer profiles"""
        profile_list = []
        
        for account, profile in profiles.items():
            # Calculate normalized risk score (0-100)
            risk_factors = []
            
            # Suspicious transaction ratio
            susp_ratio = profile['suspicious_transactions'] / max(profile['total_transactions'], 1)
            risk_factors.append(susp_ratio * 30)
            
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
        print(f"✓ Customer profiling completed for {len(self.profiles)} accounts")
        
        # Risk distribution
        risk_dist = self.profiles['risk_classification'].value_counts()
        print(f"\n📊 Risk Distribution:")
        for risk, count in risk_dist.items():
            percentage = count / len(self.profiles) * 100
            print(f"   {risk}: {count} ({percentage:.1f}%)")
        
        # Top 5 highest risk customers
        print(f"\n🚨 Top 5 Highest Risk Customers:")
        top_risk = self.profiles.nlargest(5, 'risk_score')[['account', 'risk_score', 'risk_classification', 'suspicious_transactions']]
        print(top_risk.to_string(index=False))
