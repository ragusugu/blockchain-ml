"""
Transform Phase of ETL Pipeline
Cleans and normalizes extracted data using Pandas
"""
import logging
import pandas as pd
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def transform_data(rows):
    """
    Transform raw transaction rows into clean, normalized data.
    
    Args:
        rows: List of dictionaries from extract phase
    
    Returns:
        pandas.DataFrame with clean data
    """
    if not rows:
        logger.warning("No rows to transform")
        return pd.DataFrame()
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    logger.info(f"Created DataFrame with {len(df)} rows")
    
    # Data type conversions
    df['block_number'] = df['block_number'].astype('int64')
    df['transaction_index'] = df['transaction_index'].astype('int64')
    df['timestamp'] = df['timestamp'].astype('int64')
    df['value_eth'] = df['value_eth'].astype('float64')
    df['gas'] = df['gas'].astype('int64')
    df['gas_price_gwei'] = df['gas_price_gwei'].astype('float64')
    df['gas_used'] = df['gas_used'].astype('int64')
    df['cumulative_gas_used'] = df['cumulative_gas_used'].astype('int64')
    df['status'] = df['status'].astype('int8')
    
    # Handle missing values
    df['to_address'] = df['to_address'].fillna('')
    df['contract_address'] = df['contract_address'].fillna('')
    df['effective_gas_price'] = df['effective_gas_price'].fillna(0).astype('int64')
    
    # Add processing timestamp
    df['processed_at'] = datetime.now(timezone.utc)
    
    # Rename columns for database compatibility
    df.rename(columns={
        'block_number': 'block_number',
        'block_hash': 'block_hash',
        'timestamp': 'block_timestamp',
        'transaction_hash': 'tx_hash',
        'transaction_index': 'tx_index',
        'from_address': 'from_addr',
        'to_address': 'to_addr',
        'value_eth': 'value',
        'gas_price_gwei': 'gas_price',
        'contract_address': 'contract_addr',
        'effective_gas_price': 'effective_gas_price'
    }, inplace=True)
    
    logger.info(f"Transformed {len(df)} rows")
    return df


def validate_data(df):
    """
    Validate transformed data quality.
    
    Args:
        df: DataFrame to validate
    
    Returns:
        Boolean - True if valid, False otherwise
    """
    if df.empty:
        logger.warning("DataFrame is empty")
        return False
    
    # Check for required columns
    required_cols = ['tx_hash', 'block_number', 'from_addr', 'status']
    missing = [col for col in required_cols if col not in df.columns]
    
    if missing:
        logger.error(f"Missing required columns: {missing}")
        return False
    
    # Check for nulls in critical columns
    null_counts = df[required_cols].isnull().sum()
    if null_counts.any():
        logger.warning(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
    
    logger.info(f"Data validation passed for {len(df)} rows")
    return True
