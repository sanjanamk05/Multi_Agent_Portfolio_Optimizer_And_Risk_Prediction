"""
Data loader module for fetching and preprocessing stock data
Downloads data from Yahoo Finance and prepares it for analysis
"""

import os
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    STOCKS, DATA_START_DATE, DATA_END_DATE, DATA_INTERVAL,
    RAW_DATA_DIR, PROCESSED_DATA_DIR, VERBOSE
)

class DataLoader:
    """Load and preprocess financial data"""
    
    def __init__(self):
        self.stocks = STOCKS
        self.start_date = DATA_START_DATE
        self.end_date = DATA_END_DATE
        self.interval = DATA_INTERVAL
        self.raw_data = {}
        self.processed_data = {}
    
    def download_data(self):
        """Download historical stock data from Yahoo Finance"""
        print("📥 Downloading historical stock data...")
        
        for stock in self.stocks:
            try:
                data = yf.download(
                    stock,
                    start=self.start_date,
                    end=self.end_date,
                    interval=self.interval,
                    progress=False
                )
                self.raw_data[stock] = data
                print(f"   ✅ {stock}: {len(data)} trading days")
            except Exception as e:
                print(f"   ❌ Error downloading {stock}: {e}")
                return False
        
        print("✅ Data download complete!\n")
        return True
    
    def save_raw_data(self):
        """Save raw data to CSV files"""
        print("💾 Saving raw data...")
        
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        
        for stock, data in self.raw_data.items():
            filepath = os.path.join(RAW_DATA_DIR, f'{stock}_raw.csv')
            data.to_csv(filepath)
            print(f"   ✅ Saved {stock}")
        
        print("✅ Raw data saved!\n")
    
    def clean_data(self):
        """Clean data: remove NaN, outliers, duplicates"""
        print("🧹 Cleaning data...")
        
        for stock, data in self.raw_data.items():
            # Remove duplicates
            data = data[~data.index.duplicated(keep='first')]
            
            # Remove NaN values
            data = data.dropna()
            
            # Remove outliers using IQR method
            for col in data.select_dtypes(include=[np.number]).columns:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                data[col] = data[col].clip(lower_bound, upper_bound)
            
            self.raw_data[stock] = data
            print(f"   ✅ {stock}: {len(data)} records after cleaning")
        
        print("✅ Data cleaning complete!\n")
    
    def normalize_data(self):
        """Normalize data to 0-1 range"""
        print("📊 Normalizing data...")
        
        for stock, data in self.raw_data.items():
            # MinMax normalization for price columns
            price_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close']
            for col in price_cols:
                if col in data.columns:
                    min_val = data[col].min()
                    max_val = data[col].max()
                    data[col] = (data[col] - min_val) / (max_val - min_val)
            
            # Volume normalization
            if 'Volume' in data.columns:
                min_vol = data['Volume'].min()
                max_vol = data['Volume'].max()
                data['Volume'] = (data['Volume'] - min_vol) / (max_vol - min_vol)
            
            self.raw_data[stock] = data
            print(f"   ✅ {stock}: normalized")
        
        print("✅ Data normalization complete!\n")
    
    def compute_technical_indicators(self):
        """Compute 10+ technical indicators"""
        print("📈 Computing technical indicators...")
        
        for stock, data in self.raw_data.items():
            # Moving Averages
            data['MA_10'] = data['Close'].rolling(window=10).mean()
            data['MA_50'] = data['Close'].rolling(window=50).mean()
            data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
            
            # Daily returns
            data['Returns'] = data['Close'].pct_change()
            
            # RSI (Relative Strength Index)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD
            ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = ema_12 - ema_26
            data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
            data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
            
            # Bollinger Bands
            sma_20 = data['Close'].rolling(window=20).mean()
            std_20 = data['Close'].rolling(window=20).std()
            data['BB_Upper'] = sma_20 + (2 * std_20)
            data['BB_Lower'] = sma_20 - (2 * std_20)
            data['BB_Middle'] = sma_20
            
            # ATR (Average True Range)
            high_low = data['High'] - data['Low']
            high_close = abs(data['High'] - data['Close'].shift())
            low_close = abs(data['Low'] - data['Close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = ranges.max(axis=1)
            data['ATR'] = true_range.rolling(14).mean()
            
            # Remove NaN from indicators
            data = data.dropna()
            
            self.processed_data[stock] = data
            print(f"   ✅ {stock}: {len(data.columns)} features computed")
        
        print("✅ Technical indicators computed!\n")
    
    def save_processed_data(self):
        """Save processed data to CSV"""
        print("💾 Saving processed data...")
        
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
        
        for stock, data in self.processed_data.items():
            filepath = os.path.join(PROCESSED_DATA_DIR, f'{stock}_processed.csv')
            data.to_csv(filepath)
            print(f"   ✅ {stock}: {len(data)} records with {len(data.columns)} features")
        
        print("✅ Processed data saved!\n")
    
    def get_data(self, stock):
        """Get processed data for a specific stock"""
        return self.processed_data.get(stock, None)
    
    def get_all_data(self):
        """Get all processed data"""
        return self.processed_data

# Main execution
if __name__ == "__main__":
    loader = DataLoader()
    
    # Execute pipeline
    print("=" * 60)
    print("MULTI-AGENT PORTFOLIO OPTIMIZER - DATA LOADING PIPELINE")
    print("=" * 60 + "\n")
    
    loader.download_data()
    loader.save_raw_data()
    loader.clean_data()
    loader.normalize_data()
    loader.compute_technical_indicators()
    loader.save_processed_data()
    
    print("=" * 60)
    print("✅ DATA PIPELINE COMPLETE!")
    print("=" * 60)