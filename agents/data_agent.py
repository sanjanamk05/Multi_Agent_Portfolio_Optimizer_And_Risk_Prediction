"""
Data & Market Analysis Agent
Analyzes technical indicators and identifies market trends
"""

import os
import pandas as pd
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    STOCKS, PROCESSED_DATA_DIR, REPORTS_DIR
)

class DataAgent:
    """Analyzes market data and generates trend signals"""
    
    def __init__(self):
        self.stocks = STOCKS
        self.data = {}
        self.analysis_results = {}
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
   
    
    def analyze_moving_averages(self, stock):
        """Analyze Moving Average trends"""
        data = self.data[stock]
        
        # Get latest values
        ma_10 = data['MA_10'].iloc[-1]
        ma_50 = data['MA_50'].iloc[-1]
        price = data['Close'].iloc[-1]
        
        # Determine trend
        if ma_10 > ma_50:
            ma_trend = "BULLISH ⬆️"
            ma_score = 1.0
        elif ma_10 < ma_50:
            ma_trend = "BEARISH ⬇️"
            ma_score = 0.0
        else:
            ma_trend = "NEUTRAL ➡️"
            ma_score = 0.5
        
        return {
            'ma_10': ma_10,
            'ma_50': ma_50,
            'price': price,
            'trend': ma_trend,
            'score': ma_score
        }
    
    def analyze_rsi(self, stock):
        """Analyze RSI (Relative Strength Index)"""
        data = self.data[stock]
        
        rsi = data['RSI'].iloc[-1]
        
        # RSI interpretation
        if rsi > 70:
            rsi_signal = "OVERBOUGHT 🔴"
            rsi_score = 0.0  # Sell signal
        elif rsi < 30:
            rsi_signal = "OVERSOLD 🟢"
            rsi_score = 1.0  # Buy signal
        else:
            rsi_signal = "NEUTRAL 🟡"
            rsi_score = 0.5
        
        return {
            'rsi_value': rsi,
            'signal': rsi_signal,
            'score': rsi_score
        }
    
    def analyze_macd(self, stock):
        """Analyze MACD (Moving Average Convergence Divergence)"""
        data = self.data[stock]
        
        macd = data['MACD'].iloc[-1]
        signal_line = data['Signal_Line'].iloc[-1]
        histogram = data['MACD_Histogram'].iloc[-1]
        
        # MACD interpretation
        if macd > signal_line:
            macd_trend = "BULLISH ⬆️"
            macd_score = 1.0
        elif macd < signal_line:
            macd_trend = "BEARISH ⬇️"
            macd_score = 0.0
        else:
            macd_trend = "NEUTRAL ➡️"
            macd_score = 0.5
        
        return {
            'macd_value': macd,
            'signal_line': signal_line,
            'histogram': histogram,
            'trend': macd_trend,
            'score': macd_score
        }
    
    def calculate_price_change(self, stock):
        """Calculate price change percentage"""
        data = self.data[stock]
        
        current_price = data['Close'].iloc[-1]
        price_30_days_ago = data['Close'].iloc[-30] if len(data) >= 30 else data['Close'].iloc[0]
        
        change_pct = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
        
        if change_pct > 0:
            change_direction = "UP ⬆️"
            change_score = 1.0
        elif change_pct < 0:
            change_direction = "DOWN ⬇️"
            change_score = 0.0
        else:
            change_direction = "FLAT ➡️"
            change_score = 0.5
        
        return {
            'current_price': current_price,
            'price_30_days_ago': price_30_days_ago,
            'change_pct': change_pct,
            'direction': change_direction,
            'score': change_score
        }
    
    def determine_overall_trend(self, stock):
        """Determine overall market trend for a stock"""
        
        # Get all analysis scores
        ma_analysis = self.analyze_moving_averages(stock)
        rsi_analysis = self.analyze_rsi(stock)
        macd_analysis = self.analyze_macd(stock)
        price_analysis = self.calculate_price_change(stock)
        
        # Calculate average score (weighted)
        overall_score = (
            ma_analysis['score'] * 0.30 +
            rsi_analysis['score'] * 0.25 +
            macd_analysis['score'] * 0.30 +
            price_analysis['score'] * 0.15
        )
        
        # Convert score to trend
        if overall_score > 0.65:
            overall_trend = "STRONG BULLISH 📈"
            trend_color = "🟢"
        elif overall_score > 0.55:
            overall_trend = "BULLISH 📊"
            trend_color = "🟢"
        elif overall_score > 0.45:
            overall_trend = "NEUTRAL ➡️"
            trend_color = "🟡"
        elif overall_score > 0.35:
            overall_trend = "BEARISH 📉"
            trend_color = "🔴"
        else:
            overall_trend = "STRONG BEARISH ⚠️"
            trend_color = "🔴"
        
        return {
            'trend': overall_trend,
            'score': overall_score,
            'color': trend_color,
            'ma': ma_analysis,
            'rsi': rsi_analysis,
            'macd': macd_analysis,
            'price': price_analysis
        }
    
    def analyze_all_stocks(self):
        """Analyze all stocks and generate report"""
        print("📊 Analyzing market data for all stocks...\n")
        
        for stock in self.stocks:
            analysis = self.determine_overall_trend(stock)
            self.analysis_results[stock] = analysis
            
            print(f"{'='*60}")
            print(f"📈 {stock} MARKET ANALYSIS")
            print(f"{'='*60}")
            print(f"Overall Trend: {analysis['trend']}")
            print(f"Trend Score: {analysis['score']:.2f} / 1.00")
            print()
            
            print(f"📊 Moving Average Analysis:")
            print(f"   MA-10: {analysis['ma']['ma_10']:.4f}")
            print(f"   MA-50: {analysis['ma']['ma_50']:.4f}")
            print(f"   Current Price: {analysis['ma']['price']:.4f}")
            print(f"   Signal: {analysis['ma']['trend']}")
            print()
            
            print(f"📈 RSI Analysis:")
            print(f"   RSI Value: {analysis['rsi']['rsi_value']:.2f}")
            print(f"   Signal: {analysis['rsi']['signal']}")
            print()
            
            print(f"📉 MACD Analysis:")
            print(f"   MACD: {analysis['macd']['macd_value']:.6f}")
            print(f"   Signal Line: {analysis['macd']['signal_line']:.6f}")
            print(f"   Histogram: {analysis['macd']['histogram']:.6f}")
            print(f"   Trend: {analysis['macd']['trend']}")
            print()
            
            print(f"💹 Price Change (30 days):")
            print(f"   Current: ${analysis['price']['current_price']:.2f}")
            print(f"   30 Days Ago: ${analysis['price']['price_30_days_ago']:.2f}")
            print(f"   Change: {analysis['price']['change_pct']:.2f}% {analysis['price']['direction']}")
            print()
        
        print("✅ Analysis complete!\n")
    
    def generate_report(self):
        """Generate a text report"""
        print("📝 Generating market analysis report...\n")
        
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        report_filename = os.path.join(REPORTS_DIR, 'Market_Analysis_Report.txt')
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("MARKET ANALYSIS REPORT\n")
            f.write("="*60 + "\n\n")
            
            for stock in self.stocks:
                analysis = self.analysis_results[stock]
                
                f.write(f"{'='*60}\n")
                f.write(f"{stock} - {analysis['trend']}\n")
                f.write(f"{'='*60}\n")
                f.write(f"Trend Score: {analysis['score']:.2f}/1.00\n\n")
                
                f.write(f"Moving Average: {analysis['ma']['trend']}\n")
                f.write(f"  MA-10: {analysis['ma']['ma_10']:.4f}\n")
                f.write(f"  MA-50: {analysis['ma']['ma_50']:.4f}\n\n")
                
                f.write(f"RSI: {analysis['rsi']['signal']}\n")
                f.write(f"  Value: {analysis['rsi']['rsi_value']:.2f}\n\n")
                
                f.write(f"MACD: {analysis['macd']['trend']}\n")
                f.write(f"  Value: {analysis['macd']['macd_value']:.6f}\n\n")
                
                f.write(f"Price Change (30 days): {analysis['price']['change_pct']:.2f}%\n\n")
        
        print(f"✅ Report saved to: {report_filename}\n")
        
                
              
    
    def get_analysis(self, stock):
        """Get analysis results for a specific stock"""
        return self.analysis_results.get(stock, None)
    
    def get_all_analysis(self):
        """Get all analysis results"""
        return self.analysis_results

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("DATA & MARKET ANALYSIS AGENT")
    print("=" * 60 + "\n")
    
    agent = DataAgent()
    agent.analyze_all_stocks()
    agent.generate_report()
    
    print("=" * 60)
    print("✅ DATA AGENT COMPLETE!")
    print("=" * 60)