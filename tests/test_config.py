"""
Tests for config module
"""
import os
import sys
import warnings
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))


class TestConfig:
    def test_config_loads(self):
        from config import cfg
        assert cfg is not None
        assert isinstance(cfg.RPC_URL, str)
        assert isinstance(cfg.BATCH_SIZE, int)

    def test_rpc_candidates_returns_list(self):
        from config import cfg
        candidates = cfg.rpc_candidates
        assert isinstance(candidates, list)
        assert len(candidates) > 0

    def test_default_db_url_warns(self):
        """Default DB URL should emit a warning"""
        # Only test if DATABASE_URL not explicitly set
        if not os.getenv('DATABASE_URL'):
            from config import _Config
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                c = _Config()
                c._check_db_credentials()
                assert len(w) >= 1
                assert "default" in str(w[0].message).lower()
