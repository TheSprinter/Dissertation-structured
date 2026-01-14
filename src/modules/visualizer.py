"""
Visualizer Module
=================

Handles data visualization and reporting.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from config import OUTPUT_DIR


class AMLVisualizer:
    """Handles data visualization and reporting"""
    
    def __init__(self, df):
        self.df = df
        
    def create_comprehensive_dashboard(self, customer_profiles=None, anomalies=None):
        """Create comprehensive visualization dashboard"""
        print("\n" + "="*60)
        print("CREATING COMPREHENSIVE VISUALIZATION DASHBOARD")
        print("="*60)
        
        # Set up the plotting area
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('AML Compliance System - Comprehensive Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Transaction Volume Distribution
        self._plot_transaction_distribution(axes[0, 0])
        
        # 2. Risk Assessment Overview
        if customer_profiles is not None:
            self._plot_risk_distribution(axes[0, 1], customer_profiles)
        
        # 3. Geographic Analysis
        self._plot_geographic_analysis(axes[0, 2])
        
        # 4. Temporal Patterns
        self._plot_temporal_patterns(axes[1, 0])
        
        # 5. Anomaly Analysis
        if anomalies is not None:
            self._plot_anomaly_analysis(axes[1, 1], anomalies)
        
        # 6. Compliance Overview
        self._plot_compliance_overview(axes[1, 2])
        
        plt.tight_layout()
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        plt.savefig(os.path.join(OUTPUT_DIR, 'dashboard.png'), dpi=300, bbox_inches='tight')
        plt.show()
        
        # Additional detailed plots
        self._create_detailed_analysis_plots(customer_profiles, anomalies)
    
    def _plot_transaction_distribution(self, ax):
        """Plot transaction amount distribution"""
        ax.hist(self.df['Amount'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_title('Transaction Amount Distribution')
        ax.set_xlabel('Transaction Amount')
        ax.set_ylabel('Frequency')
        ax.set_yscale('log')
    
    def _plot_risk_distribution(self, ax, profiles):
        """Plot customer risk distribution"""
        risk_counts = profiles['risk_classification'].value_counts()
        colors = ['green', 'orange', 'red']
        ax.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', colors=colors)
        ax.set_title('Customer Risk Distribution')
    
    def _plot_geographic_analysis(self, ax):
        """Plot geographic transaction patterns"""
        location_data = pd.concat([
            self.df['Sender_bank_location'],
            self.df['Receiver_bank_location']
        ]).value_counts().head(10)
        
        location_data.plot(kind='bar', ax=ax, color='coral')
        ax.set_title('Top 10 Bank Locations')
        ax.set_xlabel('Location')
        ax.set_ylabel('Transaction Count')
        ax.tick_params(axis='x', rotation=45)
    
    def _plot_temporal_patterns(self, ax):
        """Plot temporal transaction patterns"""
        # Extract hour from time
        hours = pd.to_datetime(self.df['Time'], format='%H:%M:%S').dt.hour
        hour_counts = hours.value_counts().sort_index()
        
        ax.plot(hour_counts.index, hour_counts.values, marker='o', linewidth=2, markersize=4)
        ax.set_title('Hourly Transaction Patterns')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Transaction Count')
        ax.grid(True, alpha=0.3)
    
    def _plot_anomaly_analysis(self, ax, anomalies):
        """Plot anomaly detection results"""
        if 'composite_anomaly' in anomalies.columns:
            anomaly_counts = anomalies['composite_anomaly'].value_counts()
            labels = ['Normal', 'Anomaly']
            colors = ['lightgreen', 'red']
            ax.pie(anomaly_counts.values, labels=labels, autopct='%1.1f%%', colors=colors)
            ax.set_title('Anomaly Detection Results')
    
    def _plot_compliance_overview(self, ax):
        """Plot overall compliance metrics"""
        compliance_data = {
            'Legitimate': len(self.df[self.df['Is_laundering'] == 0]),
            'Suspicious': len(self.df[self.df['Is_laundering'] == 1])
        }
        
        ax.bar(compliance_data.keys(), compliance_data.values(), 
               color=['green', 'red'], alpha=0.7)
        ax.set_title('Transaction Compliance Overview')
        ax.set_ylabel('Transaction Count')
        
        # Add percentage labels
        total = sum(compliance_data.values())
        for i, (key, value) in enumerate(compliance_data.items()):
            percentage = value / total * 100
            ax.text(i, value, f'{percentage:.1f}%', ha='center', va='bottom')
    
    def _create_detailed_analysis_plots(self, customer_profiles, anomalies):
        """Create additional detailed analysis plots"""
        
        # Plot 1: Laundering Type Distribution
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 3, 1)
        laundering_types = self.df[self.df['Is_laundering'] == 1]['Laundering_type'].value_counts()
        plt.pie(laundering_types.values, labels=laundering_types.index, autopct='%1.1f%%')
        plt.title('Laundering Type Distribution')
        
        # Plot 2: Payment Type vs Risk
        plt.subplot(1, 3, 2)
        payment_risk = self.df.groupby('Payment_type')['Is_laundering'].mean().sort_values(ascending=False)
        payment_risk.plot(kind='bar', color='orange', alpha=0.7)
        plt.title('Risk by Payment Type')
        plt.ylabel('Laundering Rate')
        plt.xticks(rotation=45)
        
        # Plot 3: Cross-border vs Domestic Risk
        plt.subplot(1, 3, 3)
        self.df['is_cross_border'] = (self.df['Sender_bank_location'] != self.df['Receiver_bank_location'])
        cross_border_risk = self.df.groupby('is_cross_border')['Is_laundering'].mean()
        cross_border_risk.plot(kind='bar', color='purple', alpha=0.7)
        plt.title('Cross-border vs Domestic Risk')
        plt.ylabel('Laundering Rate')
        plt.xticks([0, 1], ['Domestic', 'Cross-border'], rotation=0)
        
        plt.tight_layout()
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        plt.savefig(os.path.join(OUTPUT_DIR, 'detailed_analysis.png'), dpi=300, bbox_inches='tight')
        plt.show()
        
        # Customer profile visualization
        if customer_profiles is not None:
            self._plot_customer_profiles(customer_profiles)
    
    def _plot_customer_profiles(self, profiles):
        """Create customer profile visualizations"""
        plt.figure(figsize=(15, 10))
        
        # Risk score distribution
        plt.subplot(2, 3, 1)
        plt.hist(profiles['risk_score'], bins=20, alpha=0.7, color='lightblue', edgecolor='black')
        plt.title('Risk Score Distribution')
        plt.xlabel('Risk Score')
        plt.ylabel('Customer Count')
        
        # Transaction volume vs risk
        plt.subplot(2, 3, 2)
        plt.scatter(profiles['total_volume'], profiles['risk_score'], alpha=0.6, color='red')
        plt.title('Transaction Volume vs Risk Score')
        plt.xlabel('Total Volume')
        plt.ylabel('Risk Score')
        plt.xscale('log')
        
        # Suspicious transaction ratio
        plt.subplot(2, 3, 3)
        profiles['susp_ratio'] = profiles['suspicious_transactions'] / profiles['total_transactions']
        plt.hist(profiles['susp_ratio'], bins=20, alpha=0.7, color='orange', edgecolor='black')
        plt.title('Suspicious Transaction Ratio')
        plt.xlabel('Ratio')
        plt.ylabel('Customer Count')
        
        # Cross-border activity
        plt.subplot(2, 3, 4)
        risk_classes = profiles.groupby('risk_classification')['cross_border_count'].mean()
        risk_classes.plot(kind='bar', color='green', alpha=0.7)
        plt.title('Cross-border Activity by Risk Class')
        plt.ylabel('Average Cross-border Count')
        plt.xticks(rotation=0)
        
        # High-risk countries involvement
        plt.subplot(2, 3, 5)
        high_risk_dist = profiles['high_risk_countries'].value_counts().head(10)
        high_risk_dist.plot(kind='bar', color='purple', alpha=0.7)
        plt.title('High-risk Country Involvement')
        plt.xlabel('Number of High-risk Transactions')
        plt.ylabel('Customer Count')
        
        # Structuring patterns
        plt.subplot(2, 3, 6)
        structuring_dist = profiles['structuring_indicators'].value_counts().head(10)
        structuring_dist.plot(kind='bar', color='red', alpha=0.7)
        plt.title('Structuring Pattern Distribution')
        plt.xlabel('Structuring Indicators')
        plt.ylabel('Customer Count')
        
        plt.suptitle('Customer Profile Analysis', fontsize=14, fontweight='bold')
        plt.tight_layout()
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        plt.savefig(os.path.join(OUTPUT_DIR, 'customer_profiles.png'), dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_compliance_report(self, customer_profiles=None, anomalies=None, ml_metrics=None):
        """Generate comprehensive compliance report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE AML COMPLIANCE REPORT")
        print("="*80)
        
        # Basic statistics
        total_transactions = len(self.df)
        suspicious_transactions = self.df['Is_laundering'].sum()
        suspicion_rate = suspicious_transactions / total_transactions * 100
        
        print(f"\n📊 TRANSACTION OVERVIEW:")
        print(f"   Total Transactions Analyzed: {total_transactions:,}")
        print(f"   Suspicious Transactions: {suspicious_transactions:,}")
        print(f"   Overall Suspicion Rate: {suspicion_rate:.2f}%")
        print(f"   Date Range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        
        # Customer risk summary
        if customer_profiles is not None:
            risk_summary = customer_profiles['risk_classification'].value_counts()
            print(f"\n🎯 CUSTOMER RISK ASSESSMENT:")
            for risk_level, count in risk_summary.items():
                percentage = count / len(customer_profiles) * 100
                print(f"   {risk_level} Risk Customers: {count} ({percentage:.1f}%)")
        
        # Anomaly detection summary
        if anomalies is not None and 'composite_anomaly' in anomalies.columns:
            anomaly_count = anomalies['composite_anomaly'].sum()
            anomaly_rate = anomaly_count / len(anomalies) * 100
            print(f"\n🔍 ANOMALY DETECTION RESULTS:")
            print(f"   Anomalous Transactions: {anomaly_count:,}")
            print(f"   Anomaly Detection Rate: {anomaly_rate:.2f}%")
        
        # ML model performance
        if ml_metrics:
            print(f"\n🤖 MACHINE LEARNING MODEL PERFORMANCE:")
            for model_name, metrics in ml_metrics.items():
                print(f"   {model_name.upper()}:")
                for metric_name, value in metrics.items():
                    print(f"     {metric_name}: {value:.3f}")
        
        print("\n" + "="*80)
        print("REPORT GENERATION COMPLETE")
        print("="*80)
