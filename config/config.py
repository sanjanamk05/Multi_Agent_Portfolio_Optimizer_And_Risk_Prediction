"""
Configuration file for Multi-Agent Portfolio Optimization System
All system parameters and settings defined here
"""

# ==================== STOCK SELECTION ====================
STOCKS = ['AAPL', 'TSLA', 'AMZN', 'GOOGL']
INVESTMENT_AMOUNT = 100000  # $100,000 initial investment

# ==================== DATA PARAMETERS ====================
DATA_START_DATE = '2022-01-01'  # Start date for historical data
DATA_END_DATE = '2024-12-31'     # End date for historical data
DATA_INTERVAL = '1d'              # Daily data
LOOKBACK_WINDOW = 60              # 60 days for feature engineering

# ==================== TECHNICAL INDICATORS ====================
MA_PERIODS = [10, 50]
EMA_PERIOD = 12
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD_DEV = 2
ATR_PERIOD = 14

# ==================== RISK PREDICTION ====================
TRAIN_TEST_SPLIT = 0.8  # 80% train, 20% test
RISK_MODEL_TYPE = 'random_forest'  # Options: 'random_forest', 'linear_regression'
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH = 15
RF_MIN_SAMPLES_LEAF = 2

# Risk score thresholds
RISK_THRESHOLDS = {
    'low': (0.0, 0.3),
    'medium': (0.3, 0.7),
    'high': (0.7, 1.0)
}

# ==================== PORTFOLIO OPTIMIZATION ====================
MIN_ALLOCATION = 0.10  # Minimum 10% per stock
MAX_ALLOCATION = 0.40  # Maximum 40% per stock
RISK_FREE_RATE = 0.02  # 2% risk-free rate

# ==================== REINFORCEMENT LEARNING ====================
RL_ALGORITHM = 'PPO'  # Options: 'PPO', 'DQN'
PPO_LEARNING_RATE = 0.0003
PPO_BATCH_SIZE = 64
PPO_N_EPOCHS = 10
PPO_TIMESTEPS = 50000

DQN_LEARNING_RATE = 0.0001
DQN_BUFFER_SIZE = 50000
DQN_TIMESTEPS = 50000

EPISODE_LENGTH = 252  # Trading days per episode
TRANSACTION_COST = 0.001  # 0.1% transaction cost

# ==================== FILE PATHS ====================
DATA_DIR = 'data'
RAW_DATA_DIR = f'{DATA_DIR}/raw'
PROCESSED_DATA_DIR = f'{DATA_DIR}/processed'
MODELS_DIR = 'models/trained_models'
DATASETS_DIR = 'datasets/saved_datasets'
CSV_EXPORTS_DIR = 'datasets/csv_exports'
REPORTS_DIR = 'reports'
DEMO_RESULTS_DIR = 'demo_results'
VISUALIZATIONS_DIR = f'{DEMO_RESULTS_DIR}/visualizations'

# ==================== SYSTEM SETTINGS ====================
RANDOM_SEED = 42
VERBOSE = True
SAVE_MODELS = True
SAVE_PLOTS = True
USE_CACHED_DATA = True