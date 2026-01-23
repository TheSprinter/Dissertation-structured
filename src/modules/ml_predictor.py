"""
ML Predictor Module
===================

Handles machine learning model training and predictions.
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score)
try:
    from joblib import dump, load
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False


class MLPredictor:
    """Handles machine learning model training and predictions"""
    
    def __init__(self, df, model_dir='models'):
        self.df = df
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.model_metrics = {}
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, 'fraud_model.pkl')
        self.package_path = os.path.join(model_dir, 'ml_package.pkl')
        
        # Create models directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        
    def train_compliance_model(self, test_size=0.3):
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
        categorical_features = ['Payment_type', 'Sender_bank_location', 'Receiver_bank_location',
                               'Payment_currency', 'Received_currency']
        
        for feature in categorical_features:
            if feature in features.columns:
                le = LabelEncoder()
                features[f'{feature}_encoded'] = le.fit_transform(features[feature].astype(str))
                self.label_encoders[feature] = le
                features = features.drop(feature, axis=1)
        
        # Keep only numeric features (exclude any string/object columns)
        numeric_features = features.select_dtypes(include=[np.number]).copy()
        if 'Is_laundering' not in numeric_features.columns and 'Is_laundering' in features.columns:
            numeric_features['Is_laundering'] = features['Is_laundering']

        # Store feature names (exclude target)
        self.feature_names = [col for col in numeric_features.columns if col != 'Is_laundering']
        
        # Prepare X and y
        X = numeric_features[self.feature_names]
        y = numeric_features['Is_laundering'] if 'Is_laundering' in numeric_features.columns else features['Is_laundering']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        print(f"✓ Feature preparation complete: {len(self.feature_names)} numeric features")
        return X, y
    
    def _engineer_features(self, df):
        """Engineer additional features for better prediction"""
        # Time-based features
        df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
        df['is_weekend'] = pd.to_datetime(df['Date']).dt.weekday >= 5
        df['is_night_transaction'] = ((df['hour'] >= 22) | (df['hour'] <= 5)).astype(int)
        
        # Amount-based features
        df['log_amount'] = np.log1p(df['Amount'])
        df['is_round_amount'] = (df['Amount'] % 1000 == 0).astype(int)
        df['is_structuring_amount'] = ((df['Amount'] >= 9000) & (df['Amount'] < 10000)).astype(int)
        
        # Geographic features
        df['is_cross_border'] = (df['Sender_bank_location'] != df['Receiver_bank_location']).astype(int)
        df['is_currency_mismatch'] = (df['Payment_currency'] != df['Received_currency']).astype(int)
        
        # Account pattern features
        df['sender_frequency'] = df.groupby('Sender_account')['Sender_account'].transform('count')
        df['receiver_frequency'] = df.groupby('Receiver_account')['Receiver_account'].transform('count')
        
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
    
    def save_model(self, filename=None):
        """Save trained model and all components to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        filepath = filename if filename else self.model_path
        
        print(f"\n💾 Saving trained model to {filepath}...")
        
        try:
            if JOBLIB_AVAILABLE:
                # Use joblib for better performance with sklearn models
                dump(self.model, filepath)
                print("✓ Model saved using joblib")
            else:
                # Fallback to pickle
                with open(filepath, 'wb') as f:
                    pickle.dump(self.model, f)
                print("✓ Model saved using pickle")
            return True
        except Exception as e:
            print(f"✗ Error saving model: {e}")
            return False
    
    def load_model(self, filename=None):
        """Load pre-trained model from disk"""
        filepath = filename if filename else self.model_path
        
        if not os.path.exists(filepath):
            print(f"⚠ No saved model found at {filepath}")
            return False
        
        print(f"📂 Loading model from {filepath}...")
        
        try:
            if JOBLIB_AVAILABLE:
                self.model = load(filepath)
                print("✓ Model loaded using joblib")
            else:
                with open(filepath, 'rb') as f:
                    self.model = pickle.load(f)
                print("✓ Model loaded using pickle")
            return True
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            return False
    
    def save_complete_package(self, filename=None):
        """Save model with all preprocessing components and metadata"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        filepath = filename if filename else self.package_path
        
        print(f"\n💾 Saving complete ML package to {filepath}...")
        
        # Package all components
        ml_package = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'model_metrics': self.model_metrics,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'n_features': len(self.feature_names)
        }
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(ml_package, f, protocol=pickle.HIGHEST_PROTOCOL)
            print("✓ Complete ML package saved successfully")
            print(f"  - Model: {type(self.model).__name__}")
            print(f"  - Features: {len(self.feature_names)}")
            print(f"  - Encoders: {len(self.label_encoders)}")
            print(f"  - Timestamp: {ml_package['timestamp']}")
            return True
        except Exception as e:
            print(f"✗ Error saving ML package: {e}")
            return False
    
    def load_complete_package(self, filename=None):
        """Load model with all preprocessing components"""
        filepath = filename if filename else self.package_path
        
        if not os.path.exists(filepath):
            print(f"⚠ No saved package found at {filepath}")
            return False
        
        print(f"📂 Loading complete ML package from {filepath}...")
        
        try:
            with open(filepath, 'rb') as f:
                ml_package = pickle.load(f)
            
            # Restore all components
            self.model = ml_package['model']
            self.scaler = ml_package['scaler']
            self.label_encoders = ml_package['label_encoders']
            self.feature_names = ml_package['feature_names']
            self.model_metrics = ml_package.get('model_metrics', {})
            
            print("✓ Complete ML package loaded successfully")
            print(f"  - Model: {type(self.model).__name__}")
            print(f"  - Features: {len(self.feature_names)}")
            print(f"  - Encoders: {len(self.label_encoders)}")
            print(f"  - Saved on: {ml_package.get('timestamp', 'Unknown')}")
            return True
        except Exception as e:
            print(f"✗ Error loading ML package: {e}")
            return False
    
    def list_saved_models(self):
        """List all saved models in the models directory"""
        if not os.path.exists(self.model_dir):
            print(f"⚠ Models directory not found: {self.model_dir}")
            return []
        
        models = [f for f in os.listdir(self.model_dir) if f.endswith(('.pkl', '.joblib'))]
        
        if models:
            print(f"\n📋 Found {len(models)} saved model(s):")
            for i, model in enumerate(models, 1):
                filepath = os.path.join(self.model_dir, model)
                size = os.path.getsize(filepath) / 1024  # KB
                modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                print(f"  {i}. {model} ({size:.1f} KB) - Modified: {modified.strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"⚠ No saved models found in {self.model_dir}")
        
        return models
    
    def _analyze_feature_importance(self):
        """Analyze and display feature importance"""
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n🔍 Top 10 Most Important Features:")
            print(feature_importance.head(10).to_string(index=False))
    
    def predict_risk(self, transaction_data):
        """Predict compliance risk for a new transaction"""
        if self.model is None:
            raise ValueError("Model not trained yet. Please run train_compliance_model() first.")
        
        # Convert single transaction to dataframe if needed
        if isinstance(transaction_data, dict):
            transaction_df = pd.DataFrame([transaction_data])
        else:
            transaction_df = transaction_data.copy()
        
        # Engineer features
        features = self._engineer_features(transaction_df)
        
        # Encode categorical variables
        categorical_features = ['Payment_type', 'Sender_bank_location', 'Receiver_bank_location',
                               'Payment_currency', 'Received_currency']
        
        for feature in categorical_features:
            if feature in features.columns and feature in self.label_encoders:
                try:
                    features[f'{feature}_encoded'] = self.label_encoders[feature].transform(features[feature].astype(str))
                    features = features.drop(feature, axis=1)
                except ValueError:
                    # Handle unseen categories
                    features[f'{feature}_encoded'] = 0
                    features = features.drop(feature, axis=1)
        
        # Select and scale features
        X = features[self.feature_names]
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        risk_probability = self.model.predict_proba(X_scaled)[0][1]
        risk_label = self.model.predict(X_scaled)[0]
        
        return {
            'risk_probability': risk_probability,
            'risk_label': 'High Risk' if risk_label == 1 else 'Low Risk',
            'risk_score': risk_probability * 100
        }
