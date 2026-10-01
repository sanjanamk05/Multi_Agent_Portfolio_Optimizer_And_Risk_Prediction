"""
Portfolio Optimization Agent
Optimizes portfolio allocation using Modern Portfolio Theory
"""

import os
import pandas as pd
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    STOCKS, PROCESSED_DATA_DIR, INVESTMENT_AMOUNT,
    MIN_ALLOCATION, MAX_ALLOCATION, RISK_FREE_RATE,
    CSV_EXPORTS_DIR
)

class PortfolioAgent:
    """Optimizes portfolio allocation"""
    
    def __init__(self):
        self.stocks = STOCKS
        self.investment_amount = INVESTMENT_AMOUNT
        self.data = {}
        self.returns_data = {}
        self.portfolio_allocation = {}
        self.portfolio_performance = {}
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
    
    def optimize_equal_weight(self):
        """Equal weight portfolio (1/N allocation)"""
        equal_weight = 1.0 / len(self.stocks)
        for stock in self.stocks:
            self.portfolio_allocation[stock] = equal_weight
    
    def optimize_portfolio(self):
        """Run portfolio optimization"""
        
        print("=" * 60)
        print("PORTFOLIO OPTIMIZATION")
        print("=" * 60 + "\n")
        
        # Equal Weight Strategy
        print("📊 Strategy: Equal Weight Portfolio")
        print("-" * 60)
        self.optimize_equal_weight()
        
        total_allocation = sum(self.portfolio_allocation.values())
        
        for stock in self.stocks:
            weight = self.portfolio_allocation[stock]
            dollar_amount = self.investment_amount * weight
            print(f"   {stock}: {weight:.2%} → ${dollar_amount:,.2f}")
        
        print()
        print("=" * 60)
        print("✅ RECOMMENDATION")
        print("=" * 60)
        print("\nRecommended Allocation:")
        for stock in self.stocks:
            weight = self.portfolio_allocation[stock]
            dollar_amount = self.investment_amount * weight
            print(f"   {stock}: {weight:.2%} (${dollar_amount:,.2f})")
        print()
    
    def save_portfolio_allocation(self):
        """Save portfolio allocation to CSV"""
        print("💾 Saving portfolio allocation...\n")
        
        os.makedirs(CSV_EXPORTS_DIR, exist_ok=True)
        
        allocation_data = {
            'Stock': [],
            'Allocation %': [],
            'Dollar Amount': []
        }
        
        for stock in self.stocks:
            allocation_data['Stock'].append(stock)
            allocation_data['Allocation %'].append(self.portfolio_allocation[stock] * 100)
            allocation_data['Dollar Amount'].append(
                self.investment_amount * self.portfolio_allocation[stock]
            )
        
        df = pd.DataFrame(allocation_data)
        filepath = os.path.join(CSV_EXPORTS_DIR, 'Portfolio_Allocation.csv')
        df.to_csv(filepath, index=False)
        
        print(f"✅ Portfolio allocation saved to: {filepath}\n")

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("PORTFOLIO OPTIMIZATION AGENT")
    print("=" * 60 + "\n")
    
    agent = PortfolioAgent()
    agent.optimize_portfolio()
    agent.save_portfolio_allocation()
    
    print("=" * 60)
    print("✅ PORTFOLIO AGENT COMPLETE!")
    print("=" * 60)
    """
Portfolio Optimization Agent
Optimizes portfolio allocation using Modern Portfolio Theory
"""

import os
import pandas as pd
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    STOCKS, PROCESSED_DATA_DIR, INVESTMENT_AMOUNT,
    MIN_ALLOCATION, MAX_ALLOCATION, RISK_FREE_RATE,
    CSV_EXPORTS_DIR
)

class PortfolioAgent:
    """Optimizes portfolio allocation"""
    
    def __init__(self):
        self.stocks = STOCKS
        self.investment_amount = INVESTMENT_AMOUNT
        self.data = {}
        self.returns_data = {}
        self.portfolio_allocation = {}
        self.portfolio_performance = {}
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
    
    def optimize_equal_weight(self):
        """Equal weight portfolio (1/N allocation)"""
        equal_weight = 1.0 / len(self.stocks)
        for stock in self.stocks:
            self.portfolio_allocation[stock] = equal_weight
    
    def optimize_portfolio(self):
        """Run portfolio optimization"""
        
        print("=" * 60)
        print("PORTFOLIO OPTIMIZATION")
        print("=" * 60 + "\n")
        
        # Equal Weight Strategy
        print("📊 Strategy: Equal Weight Portfolio")
        print("-" * 60)
        self.optimize_equal_weight()
        
        total_allocation = sum(self.portfolio_allocation.values())
        
        for stock in self.stocks:
            weight = self.portfolio_allocation[stock]
            dollar_amount = self.investment_amount * weight
            print(f"   {stock}: {weight:.2%} → ${dollar_amount:,.2f}")
        
        print()
        print("=" * 60)
        print("✅ RECOMMENDATION")
        print("=" * 60)
        print("\nRecommended Allocation:")
        for stock in self.stocks:
            weight = self.portfolio_allocation[stock]
            dollar_amount = self.investment_amount * weight
            print(f"   {stock}: {weight:.2%} (${dollar_amount:,.2f})")
        print()
    
    def save_portfolio_allocation(self):
        """Save portfolio allocation to CSV"""
        print("💾 Saving portfolio allocation...\n")
        
        os.makedirs(CSV_EXPORTS_DIR, exist_ok=True)
        
        allocation_data = {
            'Stock': [],
            'Allocation %': [],
            'Dollar Amount': []
        }
        
        for stock in self.stocks:
            allocation_data['Stock'].append(stock)
            allocation_data['Allocation %'].append(self.portfolio_allocation[stock] * 100)
            allocation_data['Dollar Amount'].append(
                self.investment_amount * self.portfolio_allocation[stock]
            )
        
        df = pd.DataFrame(allocation_data)
        filepath = os.path.join(CSV_EXPORTS_DIR, 'Portfolio_Allocation.csv')
        df.to_csv(filepath, index=False)
        
        print(f"✅ Portfolio allocation saved to: {filepath}\n")

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("PORTFOLIO OPTIMIZATION AGENT")
    print("=" * 60 + "\n")
    
    agent = PortfolioAgent()
    agent.optimize_portfolio()
    agent.save_portfolio_allocation()
    
    print("=" * 60)
    print("✅ PORTFOLIO AGENT COMPLETE!")
    print("=" * 60)