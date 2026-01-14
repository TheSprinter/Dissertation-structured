"""
Anomaly Detector Module
=======================

Handles transaction anomaly detection using multiple algorithms.
"""

import pandas as pd
import numpy as np
import os
from config import OUTPUT_DIR
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder


class AnomalyDetector:
    """Handles transaction anomaly detection using multiple algorithms"""
    
    def __init__(self, df):
        self.df = df
        self.anomalies = None
        self.anomaly_scores = None
        
    def detect_anomalies(self, save_results=True):
        """Detect anomalies using multiple methods"""
        print("\n" + "="*60)
        print("TRANSACTION ANOMALY DETECTION")
        print("="*60)
        
        # Prepare data for anomaly detection
        features = self._prepare_features()
        
        # Apply multiple anomaly detection algorithms
        isolation_anomalies = self._isolation_forest_detection(features)
        statistical_anomalies = self._statistical_detection(features)
        
        # Combine results
        combined_anomalies = self._combine_anomaly_results(isolation_anomalies, statistical_anomalies)
        
        # Store results
        self.anomalies = combined_anomalies
        
        # Display results
        self._display_anomaly_results()
        
        if save_results:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            out_path = os.path.join(OUTPUT_DIR, 'detected_anomalies.csv')
            self.anomalies.to_csv(out_path, index=False)
            print(f"💾 Anomaly results saved to {out_path}")
        
        return self.anomalies
    
    def _prepare_features(self):
        """Prepare numerical features for anomaly detection"""
        # Create feature matrix
        feature_df = self.df.copy()
        
        # Convert time to minutes since midnight
        feature_df['time_minutes'] = pd.to_datetime(feature_df['Time'], format='%H:%M:%S').dt.hour * 60 + \
                                    pd.to_datetime(feature_df['Time'], format='%H:%M:%S').dt.minute
        
        # Encode categorical variables
        le_payment = LabelEncoder()
        le_sender_loc = LabelEncoder()
        le_receiver_loc = LabelEncoder()
        
        feature_df['payment_type_encoded'] = le_payment.fit_transform(feature_df['Payment_type'])
        feature_df['sender_loc_encoded'] = le_sender_loc.fit_transform(feature_df['Sender_bank_location'])
        feature_df['receiver_loc_encoded'] = le_receiver_loc.fit_transform(feature_df['Receiver_bank_location'])
        
        # Cross-border indicator
        feature_df['is_cross_border'] = (feature_df['Sender_bank_location'] != feature_df['Receiver_bank_location']).astype(int)
        
        # Currency mismatch
        feature_df['currency_mismatch'] = (feature_df['Payment_currency'] != feature_df['Received_currency']).astype(int)
        
        # Select numerical features
        features = feature_df[['Amount', 'time_minutes', 'payment_type_encoded', 
                              'sender_loc_encoded', 'receiver_loc_encoded', 
                              'is_cross_border', 'currency_mismatch']]
        
        return features
    
    def _isolation_forest_detection(self, features):
        """Use Isolation Forest for anomaly detection"""
        print("🔍 Running Isolation Forest anomaly detection...")
        
        # Normalize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Apply Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(features_scaled)
        anomaly_scores = iso_forest.score_samples(features_scaled)
        
        # Create results dataframe
        results = self.df.copy()
        results['isolation_anomaly'] = (anomaly_labels == -1).astype(int)
        results['isolation_score'] = anomaly_scores
        
        print(f"✓ Isolation Forest detected {(anomaly_labels == -1).sum()} anomalies")
        return results
    
    def _statistical_detection(self, features):
        """Use statistical methods for anomaly detection"""
        print("📊 Running statistical anomaly detection...")
        
        results = self.df.copy()
        
        # Z-score based anomaly detection for amount
        amount_zscore = np.abs((self.df['Amount'] - self.df['Amount'].mean()) / self.df['Amount'].std())
        amount_anomalies = amount_zscore > 3
        
        # Time-based anomalies (unusual hours)
        time_minutes = pd.to_datetime(self.df['Time'], format='%H:%M:%S').dt.hour * 60 + \
                      pd.to_datetime(self.df['Time'], format='%H:%M:%S').dt.minute
        # Anomalies for very early (0-5 AM) or very late (10 PM - midnight) transactions
        time_anomalies = (time_minutes < 300) | (time_minutes > 1320)
        
        # Combine statistical anomalies
        statistical_anomalies = amount_anomalies | time_anomalies
        
        results['statistical_anomaly'] = statistical_anomalies.astype(int)
        results['amount_zscore'] = amount_zscore
        
        print(f"✓ Statistical detection found {statistical_anomalies.sum()} anomalies")
        return results
    
    def _combine_anomaly_results(self, isolation_results, statistical_results):
        """Combine results from multiple anomaly detection methods"""
        combined = isolation_results.copy()
        combined['statistical_anomaly'] = statistical_results['statistical_anomaly']
        combined['amount_zscore'] = statistical_results['amount_zscore']
        
        # Create composite anomaly score
        combined['composite_anomaly'] = ((combined['isolation_anomaly'] == 1) | 
                                        (combined['statistical_anomaly'] == 1)).astype(int)
        
        # Risk score (0-100)
        combined['anomaly_risk_score'] = (
            (combined['isolation_anomaly'] * 50) +
            (combined['statistical_anomaly'] * 30) + 
            (np.clip(-combined['isolation_score'] * 100, 0, 20))
        )
        
        return combined
    
    def _display_anomaly_results(self):
        """Display anomaly detection results summary"""
        total_anomalies = self.anomalies['composite_anomaly'].sum()
        isolation_anomalies = self.anomalies['isolation_anomaly'].sum()
        statistical_anomalies = self.anomalies['statistical_anomaly'].sum()
        
        print(f"\n📊 Anomaly Detection Summary:")
        print(f"   Total Transactions: {len(self.anomalies):,}")
        print(f"   Isolation Forest Anomalies: {isolation_anomalies:,}")
        print(f"   Statistical Anomalies: {statistical_anomalies:,}")
        print(f"   Combined Anomalies: {total_anomalies:,}")
        print(f"   Anomaly Rate: {total_anomalies/len(self.anomalies)*100:.2f}%")
        
        # Show top anomalies
        top_anomalies = self.anomalies.nlargest(5, 'anomaly_risk_score')[
            ['Sender_account', 'Receiver_account', 'Amount', 'anomaly_risk_score', 'Is_laundering']
        ]
        print(f"\n🚨 Top 5 Highest Risk Anomalies:")
        print(top_anomalies.to_string(index=False))
