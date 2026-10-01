"""
Dashboard for Multi-Agent Portfolio Optimizer
Interactive visualization using Streamlit with user input controls
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import (
    STOCKS, PROCESSED_DATA_DIR, CSV_EXPORTS_DIR, 
    INVESTMENT_AMOUNT
)

# Set page config
st.set_page_config(
    page_title="Portfolio Optimizer Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 2em;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 2px solid #2ca02c;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="main-title">📊 Multi-Agent Portfolio Optimizer</div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page:",
    ["Dashboard Overview", "Market Analysis", "Risk Assessment", 
     "Portfolio Allocation", "Agent Comparison"]
)

# SIDEBAR: USER INPUT CONTROLS
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ User Controls")

investment_amount = st.sidebar.number_input(
    "Investment Amount ($)",
    min_value=1000,
    max_value=1000000,
    value=INVESTMENT_AMOUNT,
    step=5000,
    help="Total amount to invest across all stocks"
)

risk_tolerance = st.sidebar.slider(
    "Risk Tolerance",
    min_value=1,
    max_value=10,
    value=5,
    help="1 = Conservative, 10 = Aggressive"
)

rebalance_frequency = st.sidebar.selectbox(
    "Rebalance Frequency",
    ["Daily", "Weekly", "Monthly", "Quarterly"]
)

min_stock_allocation = st.sidebar.slider(
    "Minimum Allocation per Stock (%)",
    min_value=0.0,
    max_value=25.0,
    value=5.0,
    step=1.0
)

max_stock_allocation = st.sidebar.slider(
    "Maximum Allocation per Stock (%)",
    min_value=25.0,
    max_value=100.0,
    value=50.0,
    step=1.0
)

include_technical = st.sidebar.checkbox(
    "Include Technical Analysis",
    value=True
)

st.sidebar.markdown("---")
st.sidebar.info(
    "This dashboard shows portfolio optimization results from multiple AI agents."
)

# Helper functions
def load_csv(filename):
    """Load CSV file from CSV_EXPORTS_DIR"""
    filepath = os.path.join(CSV_EXPORTS_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return None

def load_market_data(stock):
    """Load processed market data"""
    filepath = os.path.join(PROCESSED_DATA_DIR, f'{stock}_processed.csv')
    if os.path.exists(filepath):
        data = pd.read_csv(filepath, index_col=0)
        for col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        return data.dropna()
    return None

# PAGE 1: Dashboard Overview
if page == "Dashboard Overview":
    st.markdown('<div class="section-title">📌 System Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Investment", f"${investment_amount:,}")
    with col2:
        st.metric("Number of Stocks", len(STOCKS))
    with col3:
        st.metric("Risk Tolerance", f"{risk_tolerance}/10")
    with col4:
        st.metric("Rebalance", rebalance_frequency)
    
    st.markdown('<div class="section-title">👤 Your Settings</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### Investment Settings")
        st.write(f"**Amount**: ${investment_amount:,}")
        st.write(f"**Min Allocation**: {min_stock_allocation:.1f}%")
        st.write(f"**Max Allocation**: {max_stock_allocation:.1f}%")
    
    with col2:
        st.write("### Analysis Settings")
        st.write(f"**Risk Tolerance**: {risk_tolerance}/10")
        st.write(f"**Rebalance**: {rebalance_frequency}")
        if include_technical:
            st.write("✅ Technical Analysis: ON")
    
    with col3:
        st.write("### Agent Status")
        st.write("✅ Data Agent: Ready")
        st.write("✅ Risk Agent: Ready")
        st.write("✅ Portfolio Agent: Ready")
        st.write("✅ RL Agent: Ready")
    
    st.markdown('<div class="section-title">🤖 Agents in System</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Data Agent")
        st.write("""
        - Analyzes technical indicators
        - Calculates moving averages
        - Generates market trends
        - RSI, MACD analysis
        """)
    
    with col2:
        st.subheader("⚠️ Risk Agent")
        st.write("""
        - Predicts market risk
        - Random Forest model
        - Risk scoring (0-1)
        - Model performance metrics
        """)
    
    with col3:
        st.subheader("🎯 Portfolio Agent")
        st.write("""
        - Optimizes allocation
        - Modern Portfolio Theory
        - 3 strategies tested
        - Sharpe ratio maximization
        """)
    
    st.markdown('<div class="section-title">📈 Stocks Analyzed</div>', unsafe_allow_html=True)
    
    cols = st.columns(len(STOCKS))
    for i, stock in enumerate(STOCKS):
        with cols[i]:
            st.write(f"### {stock}")
            data = load_market_data(stock)
            if data is not None:
                current_price = data['Close'].iloc[-1]
                st.write(f"Current Price: ${current_price:.2f}")
                
                price_30_ago = data['Close'].iloc[-30] if len(data) >= 30 else data['Close'].iloc[0]
                change_pct = ((current_price - price_30_ago) / price_30_ago) * 100
                
                if change_pct > 0:
                    st.success(f"↑ {change_pct:.2f}%")
                else:
                    st.error(f"↓ {change_pct:.2f}%")

# PAGE 2: Market Analysis
elif page == "Market Analysis":
    st.markdown('<div class="section-title">📊 Market Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📈 Stock Charts</div>', unsafe_allow_html=True)
    
    selected_stock = st.selectbox("Select Stock:", STOCKS)
    
    data = load_market_data(selected_stock)
    if data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"### {selected_stock} - Closing Price")
            st.line_chart(data['Close'])
        
        with col2:
            st.write(f"### {selected_stock} - RSI")
            st.line_chart(data['RSI'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"### {selected_stock} - Moving Averages")
            chart_data = data[['MA_10', 'MA_50']].copy()
            st.line_chart(chart_data)
        
        with col2:
            st.write(f"### {selected_stock} - MACD")
            chart_data = data[['MACD', 'Signal_Line']].copy()
            st.line_chart(chart_data)
        
        st.markdown('<div class="section-title">📊 Technical Indicators</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            latest_close = data['Close'].iloc[-1]
            st.metric("Latest Close", f"${latest_close:.2f}")
        
        with col2:
            latest_rsi = data['RSI'].iloc[-1]
            st.metric("RSI", f"{latest_rsi:.2f}")
        
        with col3:
            latest_ma10 = data['MA_10'].iloc[-1]
            st.metric("MA-10", f"${latest_ma10:.2f}")
        
        with col4:
            latest_ma50 = data['MA_50'].iloc[-1]
            st.metric("MA-50", f"${latest_ma50:.2f}")
    else:
        st.error(f"Could not load data for {selected_stock}")

# PAGE 3: Risk Assessment
elif page == "Risk Assessment":
    st.markdown('<div class="section-title">⚠️ Risk Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🎯 Risk Levels</div>', unsafe_allow_html=True)
    
    risk_data = {
        'Stock': STOCKS,
        'Risk Level': ['Medium', 'High', 'Low', 'Medium'],
        'Risk Score': [0.35, 0.65, 0.25, 0.40]
    }
    
    df = pd.DataFrame(risk_data)
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(df.set_index('Stock')['Risk Score'])
    
    with col2:
        st.write("### Risk Classification")
        
        if risk_tolerance <= 3:
            st.write("🟢 Your Profile: **Conservative**")
            st.write("- Recommended: Low risk stocks")
            st.write("- Avoid: High volatility")
        elif risk_tolerance <= 6:
            st.write("🟡 Your Profile: **Moderate**")
            st.write("- Recommended: Mix of risks")
            st.write("- Balance: Stability & growth")
        else:
            st.write("🔴 Your Profile: **Aggressive**")
            st.write("- Recommended: Growth stocks")
            st.write("- Focus: High returns")
    
    st.markdown('<div class="section-title">⚠️ Risk Classification Guide</div>', unsafe_allow_html=True)
    st.write("""
    - 🟢 **Low Risk** (0.0 - 0.3): Stable stocks, lower volatility
    - 🟡 **Medium Risk** (0.3 - 0.6): Moderate volatility, balanced
    - 🔴 **High Risk** (0.6 - 1.0): High volatility, growth potential
    """)

# PAGE 4: Portfolio Allocation
elif page == "Portfolio Allocation":
    st.markdown('<div class="section-title">💼 Portfolio Allocation Results</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Portfolio Agent Allocation")
        alloc = load_csv('Portfolio_Allocation.csv')
        if alloc is not None:
            st.dataframe(alloc, use_container_width=True)
            st.bar_chart(alloc.set_index('Stock')['Allocation %'])
        else:
            st.warning("Portfolio allocation not found.")
    
    with col2:
        st.subheader("🤖 RL Agent Allocation")
        rl_alloc = load_csv('RL_Portfolio_Allocation.csv')
        if rl_alloc is not None:
            st.dataframe(rl_alloc, use_container_width=True)
            st.bar_chart(rl_alloc.set_index('Stock')['Allocation %'])
        else:
            st.warning("RL allocation not found.")
    
    st.markdown('<div class="section-title">🧮 Custom Allocation Calculator</div>', unsafe_allow_html=True)
    
    st.write("### Adjust Allocations Based on Your Preferences")
    
    custom_allocation = {}
    
    cols = st.columns(len(STOCKS))
    for i, stock in enumerate(STOCKS):
        with cols[i]:
            custom_allocation[stock] = st.slider(
                f"{stock} Allocation (%)",
                min_value=int(min_stock_allocation),
                max_value=int(max_stock_allocation),
                value=25,
                step=1
            )
    
    # Normalize allocations
    total_alloc = sum(custom_allocation.values())
    
    if total_alloc > 0:
        for stock in custom_allocation:
            custom_allocation[stock] = (custom_allocation[stock] / total_alloc) * 100
    
    st.write("### Your Custom Allocation")
    
    custom_data = []
    for stock in STOCKS:
        dollar_amount = (investment_amount * custom_allocation[stock]) / 100
        custom_data.append({
            'Stock': stock,
            'Allocation %': f"{custom_allocation[stock]:.2f}%",
            'Dollar Amount': f"${dollar_amount:,.2f}"
        })
    
    df_custom = pd.DataFrame(custom_data)
    st.dataframe(df_custom, use_container_width=True)
    
    chart_data = pd.DataFrame({
        'Stock': STOCKS,
        'Allocation %': [custom_allocation[s] for s in STOCKS]
    })
    st.bar_chart(chart_data.set_index('Stock'))

# PAGE 5: Agent Comparison
elif page == "Agent Comparison":
    st.markdown('<div class="section-title">🤖 Agent Comparison</div>', unsafe_allow_html=True)
    
    st.write("""
    ### Four Agents Working Together:
    
    1. **Data Agent** 📊
       - Purpose: Market analysis and trend detection
       - Output: Technical indicator analysis
       - Updates: Real-time with new data
    
    2. **Risk Agent** ⚠️
       - Purpose: Predict portfolio risk
       - Output: Risk scores (0-1 scale)
       - Model: Random Forest
    
    3. **Portfolio Agent** 💼
       - Purpose: Optimize allocation
       - Output: Recommended weights
       - Strategy: Modern Portfolio Theory
    
    4. **RL Agent** 🤖
       - Purpose: Learn optimal decisions
       - Output: Score-based allocation
       - Model: Q-Learning principles
    """)
    
    st.markdown('<div class="section-title">📊 Feature Comparison</div>', unsafe_allow_html=True)
    
    comparison_data = {
        'Feature': [
            'Real-time Analysis', 
            'Risk Prediction', 
            'Allocation Optimization', 
            'Learning Capability'
        ],
        'Data Agent': ['✅', '❌', '❌', '❌'],
        'Risk Agent': ['❌', '✅', '❌', '✅'],
        'Portfolio Agent': ['❌', '❌', '✅', '❌'],
        'RL Agent': ['❌', '❌', '✅', '✅']
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)
    
    st.info("Each agent specializes in different aspects of portfolio management. Together, they provide a comprehensive solution.")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #888;">
    Multi-Agent Portfolio Optimizer Dashboard | Built with Streamlit
    </div>
""", unsafe_allow_html=True)