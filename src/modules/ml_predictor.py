"""
ML Predictor Module
===================

Handles machine learning model training and predictions.
"""

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score)


class MLPredictor:
    """Handles machine learning model training and predictions"""
    
    def __init__(self, df):
        self.df = df
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.model_metrics = {}
        
    def train_compliance_model(self, test_size=0.3, save_model=True):
        """Train machine learning model for compliance risk prediction"""
        print("\n" + "="*60)
        print("MACHINE LEARNING MODEL TRAINING")
        print("="*60)
        
        # Prepare features and target
        X, y = self._prepare_ml_features()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, 
                                                            random_state=42, stratify=y)
        
        # Train multiple models and select best
        models = self._train_multiple_models(X_train, y_train)
        
        # Evaluate models
        best_model = self._evaluate_models(models, X_test, y_test)
        
        # Store best model
        self.model = best_model
        
        # Feature importance analysis
        self._analyze_feature_importance()
        
        # Save model to disk
        if save_model:
            self.save_model_to_disk()
        
        print("✓ Model training completed successfully!")
        return self.model
    
    def _prepare_ml_features(self):
        """Prepare features for machine learning"""
        print("🔧 Preparing features for ML model...")
        
        # Copy dataframe
        ml_df = self.df.copy()
        
        # Feature engineering
        features = self._engineer_features(ml_df)
        
        # Encode categorical variables
        categorical_features = ['merchant_category', 'payment_method', 'transaction_type',
                               'location', 'device_type', 'ip_country', 'card_type',
                               'billing_country', 'shipping_country', 'transaction_currency',
                               'billing_currency', 'merchant_reputation']
        
        for feature in categorical_features:
            if feature in features.columns:
                le = LabelEncoder()
                features[f'{feature}_encoded'] = le.fit_transform(features[feature].astype(str))
                self.label_encoders[feature] = le
                features = features.drop(feature, axis=1)
        
        # Keep only numeric features (exclude any string/object columns)
        numeric_features = features.select_dtypes(include=[np.number]).copy()
        if 'is_fraud' not in numeric_features.columns and 'is_fraud' in features.columns:
            numeric_features['is_fraud'] = features['is_fraud']

        # Store feature names (exclude target)
        self.feature_names = [col for col in numeric_features.columns if col != 'is_fraud']
        
        # Prepare X and y
        X = numeric_features[self.feature_names]
        y = numeric_features['is_fraud'] if 'is_fraud' in numeric_features.columns else features['is_fraud']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        print(f"✓ Feature preparation complete: {len(self.feature_names)} numeric features")
        return X, y
    
    def _engineer_features(self, df):
        """Engineer additional features for better prediction"""
        # Time-based features
        df['transaction_hour'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S').dt.hour if 'transaction_time' in df.columns else df.get('transaction_hour', 0)
        df['is_night_transaction'] = ((df['transaction_hour'] >= 22) | (df['transaction_hour'] <= 5)).astype(int)
        
        # Amount-based features
        df['log_amount'] = np.log1p(df['transaction_amount'])
        df['is_round_amount'] = (df['transaction_amount'] % 1000 == 0).astype(int)
        df['is_structuring_amount'] = ((df['transaction_amount'] >= 9000) & (df['transaction_amount'] < 10000)).astype(int)
        
        # Geographic features
        df['is_cross_border'] = (df['billing_country'] != df['shipping_country']).astype(int)
        df['currency_mismatch'] = (df['transaction_currency'] != df['billing_currency']).astype(int)
        
        # Customer behavior features
        df['is_high_velocity'] = (df['velocity_score'] > 70).astype(int) if 'velocity_score' in df.columns else 0
        df['has_failed_logins'] = (df['failed_login_attempts'] > 0).astype(int)
        
        # Risk indicator features
        df['unverified_email'] = (df['email_verified'] == 0).astype(int)
        df['unverified_phone'] = (df['phone_verified'] == 0).astype(int)
        df['unverified_address'] = (df['shipping_address_verified'] == 0).astype(int)
        df['verification_gap'] = df['unverified_email'] + df['unverified_phone'] + df['unverified_address']
        
        return df
    
    def _train_multiple_models(self, X_train, y_train):
        """Train multiple ML models"""
        print("🤖 Training multiple ML models...")
        
        models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'isolation_forest_classifier': IsolationForest(contamination=0.15, random_state=42)
        }
        
        trained_models = {}
        
        for name, model in models.items():
            print(f"   Training {name}...")
            if name == 'isolation_forest_classifier':
                model.fit(X_train)
                trained_models[name] = model
            else:
                model.fit(X_train, y_train)
                # Cross-validation score
                cv_scores = cross_val_score(model, X_train, y_train, cv=5)
                print(f"     CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
                trained_models[name] = model
        
        return trained_models
    
    def _evaluate_models(self, models, X_test, y_test):
        """Evaluate all models and select the best one"""
        print("\n📊 Evaluating model performance...")
        
        best_model = None
        best_score = 0
        
        for name, model in models.items():
            if name == 'isolation_forest_classifier':
                # For isolation forest, use different evaluation
                y_pred = model.predict(X_test)
                y_pred_binary = (y_pred == -1).astype(int)
                accuracy = accuracy_score(y_test, y_pred_binary)
            else:
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, zero_division=0)
                recall = recall_score(y_test, y_pred, zero_division=0)
                f1 = f1_score(y_test, y_pred, zero_division=0)
                
                print(f"\n{name.upper()} Results:")
                print(f"   Accuracy: {accuracy:.3f}")
                print(f"   Precision: {precision:.3f}")
                print(f"   Recall: {recall:.3f}")
                print(f"   F1-Score: {f1:.3f}")
                
                # Store metrics
                self.model_metrics[name] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1
                }
                
                # Update best model based on F1 score
                if f1 > best_score:
                    best_score = f1
                    best_model = model
        
        print(f"\n✓ Best model selected with F1-score: {best_score:.3f}")
        return best_model
    
    def _analyze_feature_importance(self):
        """Analyze and display feature importance"""
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n🔍 Top 10 Most Important Features:")
            print(feature_importance.head(10).to_string(index=False))
    
    def save_model_to_disk(self, model_dir='models'):
        """Save trained model, scaler, encoders, and metadata to disk using joblib"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        # Create models directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        
        # Generate timestamp for versioning
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model
        model_path = os.path.join(model_dir, 'fraud_model.pkl')
        joblib.dump(self.model, model_path, compress=3)
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        joblib.dump(self.scaler, scaler_path, compress=3)
        
        # Save label encoders
        encoders_path = os.path.join(model_dir, 'label_encoders.pkl')
        joblib.dump(self.label_encoders, encoders_path, compress=3)
        
        # Save feature names
        features_path = os.path.join(model_dir, 'feature_names.pkl')
        joblib.dump(self.feature_names, features_path, compress=3)
        
        # Save model metrics and metadata
        metadata = {
            'model_metrics': self.model_metrics,
            'timestamp': timestamp,
            'feature_count': len(self.feature_names)
        }
        metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
        joblib.dump(metadata, metadata_path, compress=3)
        
        print(f"\n💾 Model saved successfully to '{model_dir}/' directory")
        print(f"   - Model: fraud_model.pkl")
        print(f"   - Scaler: scaler.pkl")
        print(f"   - Encoders: label_encoders.pkl")
        print(f"   - Features: feature_names.pkl")
        print(f"   - Metadata: model_metadata.pkl")
    
    def load_model_from_disk(self, model_dir='models'):
        """Load pre-trained model, scaler, and encoders from disk"""
        try:
            # Load model
            model_path = os.path.join(model_dir, 'fraud_model.pkl')
            self.model = joblib.load(model_path)
            
            # Load scaler
            scaler_path = os.path.join(model_dir, 'scaler.pkl')
            self.scaler = joblib.load(scaler_path)
            
            # Load label encoders
            encoders_path = os.path.join(model_dir, 'label_encoders.pkl')
            self.label_encoders = joblib.load(encoders_path)
            
            # Load feature names
            features_path = os.path.join(model_dir, 'feature_names.pkl')
            self.feature_names = joblib.load(features_path)
            
            # Load metadata
            metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
            metadata = joblib.load(metadata_path)
            self.model_metrics = metadata.get('model_metrics', {})
            
            print(f"\n✅ Model loaded successfully from '{model_dir}/' directory")
            print(f"   - Trained on: {metadata.get('timestamp', 'Unknown')}")
            print(f"   - Features: {metadata.get('feature_count', len(self.feature_names))}")
            if self.model_metrics:
                print(f"   - Performance metrics available")
            return True
            
        except FileNotFoundError as e:
            print(f"\n⚠ No saved model found in '{model_dir}/' directory")
            print("   Train a new model using train_compliance_model()")
            return False
        except Exception as e:
            print(f"\n❌ Error loading model: {str(e)}")
            return False
    
    def model_exists(self, model_dir='models'):
        """Check if a trained model exists on disk"""
        model_path = os.path.join(model_dir, 'fraud_model.pkl')
        return os.path.exists(model_path)
    
    def predict_risk(self, transaction_data):
        """Predict compliance risk for a new transaction"""
        if self.model is None:
            raise ValueError("Model not trained yet. Please run train_compliance_model() first.")
        
        # Convert single transaction to dataframe if needed
        if isinstance(transaction_data, dict):
            transaction_df = pd.DataFrame([transaction_data])
        else:
            transaction_df = transaction_data.copy()
        
        # Add default values for missing columns
        default_columns = {
            'customer_age': 35,
            'account_age_days': 365,
            'previous_transactions_24h': 2,
            'previous_transactions_7d': 10,
            'previous_transactions_30d': 50,
            'avg_transaction_amount': 500,
            'is_weekend': 0,
            'is_holiday': 0,
            'distance_from_home_km': 10,
            'distance_from_last_transaction_km': 50,
            'failed_login_attempts': 0,
            'session_duration_seconds': 600,
            'num_page_views': 5,
            'time_since_last_transaction_minutes': 1440,
            'same_merchant_last_30d': 1,
            'num_unique_merchants_30d': 5,
            'num_locations_7d': 1,
            'currency_mismatch': 0,
            'velocity_score': 50,
            'email_verified': 1,
            'phone_verified': 1,
            'shipping_address_verified': 1,
            'card_present': 0,
            'cvv_match': 1,
            'merchant_reputation': 'High',
            'is_fraud': 0
        }
        
        for col, default_val in default_columns.items():
            if col not in transaction_df.columns:
                transaction_df[col] = default_val
        
        # Engineer features
        features = self._engineer_features(transaction_df)
        
        # Encode categorical variables
        categorical_features = ['merchant_category', 'payment_method', 'transaction_type',
                               'location', 'device_type', 'ip_country', 'card_type',
                               'billing_country', 'shipping_country', 'transaction_currency',
                               'billing_currency', 'merchant_reputation']
        
        for feature in categorical_features:
            if feature in features.columns and feature in self.label_encoders:
                try:
                    features[f'{feature}_encoded'] = self.label_encoders[feature].transform(features[feature].astype(str))
                    features = features.drop(feature, axis=1)
                except ValueError:
                    # Handle unseen categories
                    features[f'{feature}_encoded'] = 0
                    features = features.drop(feature, axis=1)
        
        # Select and scale features - only use features that exist in both
        available_features = [f for f in self.feature_names if f in features.columns]
        X = features[available_features]
        
        # If we're missing some features, fill with zeros
        if len(available_features) < len(self.feature_names):
            missing_features = set(self.feature_names) - set(available_features)
            for missing_feat in missing_features:
                X[missing_feat] = 0
            X = X[self.feature_names]  # Reorder to match training order
        
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        risk_probability = self.model.predict_proba(X_scaled)[0][1]
        risk_label = self.model.predict(X_scaled)[0]
        
        return {
            'risk_probability': risk_probability,
            'risk_label': 'High Risk' if risk_label == 1 else 'Low Risk',
            'risk_score': risk_probability * 100
        }
