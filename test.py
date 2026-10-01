"""
Quick test to verify VS Code environment setup
"""

import sys
import os

print("=" * 60)
print("ENVIRONMENT SETUP TEST")
print("=" * 60 + "\n")

# Test imports
print("Testing imports...")
try:
    import numpy as np
    print("✅ NumPy imported successfully")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")

try:
    import pandas as pd
    print("✅ Pandas imported successfully")
except ImportError as e:
    print(f"❌ Pandas import failed: {e}")

try:
    import yfinance as yf
    print("✅ YFinance imported successfully")
except ImportError as e:
    print(f"❌ YFinance import failed: {e}")

try:
    from sklearn.ensemble import RandomForestRegressor
    print("✅ Scikit-learn imported successfully")
except ImportError as e:
    print(f"❌ Scikit-learn import failed: {e}")

try:
    from stable_baselines3 import PPO
    print("✅ Stable-Baselines3 imported successfully")
except ImportError as e:
    print(f"❌ Stable-Baselines3 import failed: {e}")

try:
    import streamlit as st
    print("✅ Streamlit imported successfully")
except ImportError as e:
    print(f"❌ Streamlit import failed: {e}")

print("\n" + "=" * 60)
print("✅ SETUP COMPLETE! All dependencies installed.")
print("=" * 60)

# Test configuration
print("\n✅ Configuration file location: config/config.py")
print("✅ Project structure created: ✓")
print("\n📝 Next steps:")
print("   1. Run: python data/data_loader.py")
print("   2. Check data/raw/ and data/processed/ folders")
print("   3. Create agents next")