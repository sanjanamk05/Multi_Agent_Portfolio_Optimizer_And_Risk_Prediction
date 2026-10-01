"""
Risk Prediction Agent
Predicts market risk using Random Forest model
"""

import os
import pandas as pd
import numpy as np
import sys
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    STOCKS, PROCESSED_DATA_DIR, MODELS_DIR, TRAIN_TEST_SPLIT,
    RF_N_ESTIMATORS, RF_MAX_DEPTH, RF_MIN_SAMPLES_LEAF,
    RISK_THRESHOLDS
)

class RiskAgent:
    """Predicts market risk using machine learning"""
    
    def __init__(self):
        self.stocks = STOCKS
        self.data = {}
        self.models = {}
        self.risk_scores = {}
        self.load_processed_data()
    
    def load_processed_data(self):
        """Load processed data from CSV files"""
        print("📂 Loading processed data...")
        
        for stock in self.stocks:
            filepath = os.path.join(PROCESSED_DATA_DIR, f'{stock}_processed.csv')
            try:
                data = pd.read_csv(filepath, index_col=0)
                # Convert all columns to numeric
                for col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
                data = data.dropna()
                self.data[stock] = data
                print(f"   ✅ Loaded {stock}: {len(data)} records")
            except FileNotFoundError:
                print(f"   ❌ File not found: {filepath}")
                return False
        
        print("✅ Data loading complete!\n")
        return True
    
    def prepare_features_and_target(self, stock):
        """Prepare features (X) and target (y) for model training"""
        
        data = self.data[stock].copy()
        
        # Target: Next day's return (volatility proxy)
        data['Target'] = data['Returns'].shift(-1).abs()
        
        # Features: Technical indicators
        feature_cols = [
            'MA_10', 'MA_50', 'EMA_12', 'RSI', 
            'MACD', 'Signal_Line', 'MACD_Histogram',
            'BB_Upper', 'BB_Lower', 'BB_Middle', 'ATR'
        ]
        
        # Keep only available features
        available_features = [col for col in feature_cols if col in data.columns]
        
        # Remove rows with NaN
        data = data[available_features + ['Target']].dropna()
        
        # Remove infinity values
        data = data.replace([np.inf, -np.inf], np.nan).dropna()
        
        X = data[available_features]
        y = data['Target']
        
        # Ensure y has values and is not empty
        if len(y) < 10:
            print(f"   ⚠️ Warning: Only {len(y)} valid samples for {stock}")
        
        return X, y, available_features
        
        
    
    def train_risk_model(self, stock):
        """Train Random Forest model for risk prediction"""
        
        print(f"🤖 Training risk model for {stock}...")
        
        # Prepare data
        X, y, feature_cols = self.prepare_features_and_target(stock)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=1 - TRAIN_TEST_SPLIT,
            random_state=42
        )
        
        # Create and train model
        model = RandomForestRegressor(
            n_estimators=RF_N_ESTIMATORS,
            max_depth=RF_MAX_DEPTH,
            min_samples_leaf=RF_MIN_SAMPLES_LEAF,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        print(f"   RMSE: {rmse:.6f}")
        print(f"   R² Score: {r2:.4f}")
        
        # Store model
        self.models[stock] = {
            'model': model,
            'features': feature_cols,
            'rmse': rmse,
            'r2': r2,
            'X_test': X_test,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        print(f"   ✅ Model trained for {stock}\n")
    
    def save_models(self):
        """Save trained models to disk"""
        print("💾 Saving trained models...")
        
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        for stock, model_data in self.models.items():
            filepath = os.path.join(MODELS_DIR, f'{stock}_risk_model.pkl')
            joblib.dump(model_data['model'], filepath)
            print(f"   ✅ Saved {stock} model")
        
        print("✅ Models saved!\n")
    
    def predict_risk(self, stock):
        """Predict risk score for a stock"""
        
        data = self.data[stock].copy()
        model_data = self.models[stock]
        model = model_data['model']
        feature_cols = model_data['features']
        
        # Get latest features
        latest_features = data[feature_cols].iloc[-1:].dropna()
        
        if len(latest_features) == 0:
            return None
        
        # Predict risk
        risk_prediction = model.predict(latest_features)[0]
        
        # Normalize to 0-1 scale
        # Higher prediction = higher risk
        risk_score = min(risk_prediction * 10, 1.0)  # Scale and cap at 1.0
        
        return risk_score
    
    def categorize_risk(self, risk_score):
        """Categorize risk score into levels"""
        
        if risk_score < RISK_THRESHOLDS['low'][1]:
            return "LOW RISK 🟢"
        elif risk_score < RISK_THRESHOLDS['medium'][1]:
            return "MEDIUM RISK 🟡"
        else:
            return "HIGH RISK 🔴"
    
    def analyze_all_stocks(self):
        """Analyze risk for all stocks"""
        print("=" * 60)
        print("TRAINING RISK PREDICTION MODELS")
        print("=" * 60 + "\n")
        
        # Train models
        for stock in self.stocks:
            self.train_risk_model(stock)
        
        # Save models
        self.save_models()
        
        # Predict risks
        print("=" * 60)
        print("RISK PREDICTION RESULTS")
        print("=" * 60 + "\n")
        
        for stock in self.stocks:
            risk_score = self.predict_risk(stock)
            risk_category = self.categorize_risk(risk_score)
            
            self.risk_scores[stock] = {
                'score': risk_score,
                'category': risk_category
            }
            
            print(f"📊 {stock} Risk Analysis:")
            print(f"   Risk Score: {risk_score:.4f} / 1.00")
            print(f"   Category: {risk_category}")
            print()
    
    def generate_risk_report(self):
        """Generate risk analysis report"""
        print("📝 Generating risk report...\n")
        
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        report_filename = os.path.join(MODELS_DIR, 'Risk_Analysis_Report.txt')
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("RISK PREDICTION REPORT\n")
            f.write("="*60 + "\n\n")
            
            for stock in self.stocks:
                model_data = self.models[stock]
                risk_data = self.risk_scores[stock]
                
                f.write(f"{'='*60}\n")
                f.write(f"{stock} - {risk_data['category']}\n")
                f.write(f"{'='*60}\n")
                f.write(f"Risk Score: {risk_data['score']:.4f}/1.00\n\n")
                
                f.write(f"Model Performance:\n")
                f.write(f"  RMSE: {model_data['rmse']:.6f}\n")
                f.write(f"  R2 Score: {model_data['r2']:.4f}\n\n")
        
        print(f"✅ Report saved to: {report_filename}\n")
    
    def get_risk_score(self, stock):
        """Get risk score for a specific stock"""
        return self.risk_scores.get(stock, None)
    
    def get_all_risk_scores(self):
        """Get all risk scores"""
        return self.risk_scores

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("RISK PREDICTION AGENT")
    print("=" * 60 + "\n")
    
    agent = RiskAgent()
    agent.analyze_all_stocks()
    agent.generate_risk_report()
    
    print("=" * 60)
    print("✅ RISK AGENT COMPLETE!")
    print("=" * 60)