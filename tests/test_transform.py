"""
Tests for ETL Transform Phase
"""
import pytest
import pandas as pd
from datetime import datetime, timezone


# Add src/backend to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from etl.transform import transform_data, validate_data


def _make_raw_rows(n=3):
    """Create sample raw transaction rows matching extract output format."""
    rows = []
    for i in range(n):
        rows.append({
            'block_number': 19000000 + i,
            'block_hash': f'0x{"ab" * 32}',
            'timestamp': 1700000000 + i * 12,
            'tx_hash': f'0x{"0" * 63}{i}',
            'transaction_index': i,
            'from_address': f'0x{"aa" * 20}',
            'to_address': f'0x{"bb" * 20}',
            'value_eth': 1.5 + i,
            'gas': 21000,
            'gas_price_gwei': 50.0,
            'gas_used': 21000,
            'cumulative_gas_used': 21000 * (i + 1),
            'status': 1,
            'contract_address': None,
            'effective_gas_price': 50000000000,
        })
    return rows


class TestTransformData:
    """Tests for transform_data()"""

    def test_returns_dataframe(self):
        rows = _make_raw_rows()
        df = transform_data(rows)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3

    def test_empty_input_returns_empty_df(self):
        df = transform_data([])
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_columns_renamed(self):
        rows = _make_raw_rows(1)
        df = transform_data(rows)
        # After transform, columns should be renamed for DB compatibility
        assert 'tx_hash' in df.columns
        assert 'from_addr' in df.columns
        assert 'to_addr' in df.columns
        assert 'block_timestamp' in df.columns

    def test_dtype_conversions(self):
        rows = _make_raw_rows(1)
        df = transform_data(rows)
        assert df['block_number'].dtype == 'int64'
        assert df['status'].dtype == 'int8'

    def test_processed_at_added(self):
        rows = _make_raw_rows(1)
        df = transform_data(rows)
        assert 'processed_at' in df.columns

    def test_missing_to_address_filled(self):
        rows = _make_raw_rows(1)
        rows[0]['to_address'] = None
        df = transform_data(rows)
        assert df['to_addr'].iloc[0] == ''


class TestValidateData:
    """Tests for validate_data()"""

    def test_valid_data_passes(self):
        rows = _make_raw_rows(3)
        df = transform_data(rows)
        assert validate_data(df) is True

    def test_empty_df_fails(self):
        assert validate_data(pd.DataFrame()) is False

    def test_missing_required_columns_fails(self):
        df = pd.DataFrame({'foo': [1, 2], 'bar': [3, 4]})
        assert validate_data(df) is False
