"""
Reinforcement Learning Agent
Simplified version for portfolio optimization
"""

import os
import pandas as pd
import numpy as np
import sys
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    STOCKS, PROCESSED_DATA_DIR, MODELS_DIR, INVESTMENT_AMOUNT
)

class RLAgent:
    """Simplified RL Agent using Q-Learning principles"""
    
    def __init__(self):
        self.stocks = STOCKS
        self.data = {}
        self.q_table = {}
        self.load_processed_data()
    
    def load_processed_data(self):
        """Load processed data from CSV files"""
        print("📂 Loading processed data...")
        
        for stock in self.stocks:
            filepath = os.path.join(PROCESSED_DATA_DIR, f'{stock}_processed.csv')
            try:
                data = pd.read_csv(filepath, index_col=0)
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
    
    def calculate_stock_scores(self):
        """Calculate performance scores for each stock"""
        print("📊 Calculating Stock Performance Scores...")
        print("-" * 60)
        
        scores = {}
        
        for stock in self.stocks:
            data = self.data[stock]
            
            # Score 1: Recent price trend (last 30 days)
            recent_return = (data['Close'].iloc[-1] - data['Close'].iloc[-30]) / data['Close'].iloc[-30]
            trend_score = min(max(recent_return, -1), 1)  # Clip to [-1, 1]
            
            # Score 2: RSI signal (0-1 scale)
            rsi = data['RSI'].iloc[-1]
            if rsi < 30:
                rsi_score = 1.0  # Oversold (buy signal)
            elif rsi > 70:
                rsi_score = 0.0  # Overbought (sell signal)
            else:
                rsi_score = 0.5  # Neutral
            
            # Score 3: Moving Average trend
            ma_10 = data['MA_10'].iloc[-1]
            ma_50 = data['MA_50'].iloc[-1]
            if ma_10 > ma_50:
                ma_score = 1.0
            elif ma_10 < ma_50:
                ma_score = 0.0
            else:
                ma_score = 0.5
            
            # Combined score (weighted average)
            combined_score = (trend_score * 0.3 + rsi_score * 0.3 + ma_score * 0.4)
            combined_score = (combined_score + 1) / 2  # Normalize to [0, 1]
            
            scores[stock] = {
                'trend': trend_score,
                'rsi': rsi_score,
                'ma': ma_score,
                'combined': combined_score
            }
            
            print(f"{stock}:")
            print(f"   Trend Score: {trend_score:.2f}")
            print(f"   RSI Score: {rsi_score:.2f}")
            print(f"   MA Score: {ma_score:.2f}")
            print(f"   Combined Score: {combined_score:.2f}")
            print()
        
        return scores
    
    def optimize_allocation(self, scores):
        """Optimize portfolio allocation based on scores"""
        print("🎯 Optimizing Portfolio Allocation...")
        print("-" * 60)
        
        # Allocate based on scores
        total_score = sum(scores[stock]['combined'] for stock in self.stocks)
        
        allocation = {}
        for stock in self.stocks:
            if total_score > 0:
                weight = scores[stock]['combined'] / total_score
            else:
                weight = 1.0 / len(self.stocks)
            
            allocation[stock] = weight
        
        print("Recommended Allocation:")
        for stock in self.stocks:
            dollar_amount = INVESTMENT_AMOUNT * allocation[stock]
            print(f"   {stock}: {allocation[stock]:.2%} → ${dollar_amount:,.2f}")
        print()
        
        return allocation
    
    def save_allocation(self, allocation):
        """Save allocation to CSV"""
        print("💾 Saving allocation...")
        
        from config.config import CSV_EXPORTS_DIR
        os.makedirs(CSV_EXPORTS_DIR, exist_ok=True)
        
        allocation_data = {
            'Stock': [],
            'Allocation %': [],
            'Dollar Amount': []
        }
        
        for stock in self.stocks:
            allocation_data['Stock'].append(stock)
            allocation_data['Allocation %'].append(allocation[stock] * 100)
            allocation_data['Dollar Amount'].append(INVESTMENT_AMOUNT * allocation[stock])
        
        df = pd.DataFrame(allocation_data)
        filepath = os.path.join(CSV_EXPORTS_DIR, 'RL_Portfolio_Allocation.csv')
        df.to_csv(filepath, index=False)
        
        print(f"✅ RL allocation saved to: {filepath}\n")
    
    def run_full_pipeline(self):
        """Run complete RL pipeline"""
        
        print("=" * 60)
        print("REINFORCEMENT LEARNING AGENT")
        print("=" * 60 + "\n")
        
        scores = self.calculate_stock_scores()
        allocation = self.optimize_allocation(scores)
        self.save_allocation(allocation)
        
        print("=" * 60)
        print("✅ RL AGENT COMPLETE!")
        print("=" * 60)

# Main execution
if __name__ == "__main__":
    agent = RLAgent()
    agent.run_full_pipeline()