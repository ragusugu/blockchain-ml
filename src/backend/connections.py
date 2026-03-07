"""
Shared Connection Factory
Provides cached Web3 and database connections with retry logic.
Import: from connections import get_web3, get_db_engine
"""
import logging
import time
from typing import Optional

from web3 import Web3
from sqlalchemy import create_engine, text

from config import cfg

logger = logging.getLogger(__name__)

# ── Cached singletons ────────────────────────────────────────────
_w3_instance: Optional[Web3] = None
_db_engine = None


def get_web3(force_reconnect: bool = False) -> Optional[Web3]:
    """
    Get a cached Web3 connection with automatic fallback and retry.

    Args:
        force_reconnect: Force a new connection even if one exists.

    Returns:
        Connected Web3 instance, or None if all candidates fail.
    """
    global _w3_instance

    if _w3_instance is not None and not force_reconnect:
        try:
            if _w3_instance.is_connected():
                return _w3_instance
        except Exception:
            pass
        _w3_instance = None  # Stale connection; reconnect

    for attempt in range(cfg.RPC_MAX_RETRIES):
        for url in cfg.rpc_candidates:
            try:
                logger.info(f"Connecting to RPC: {url} (attempt {attempt + 1}/{cfg.RPC_MAX_RETRIES})")
                candidate = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': cfg.RPC_TIMEOUT}))
                if candidate.is_connected():
                    _w3_instance = candidate
                    logger.info(f"✅ Web3 connected via {url} — block {_w3_instance.eth.block_number}")
                    return _w3_instance
                logger.warning(f"RPC not reachable: {url}")
            except Exception as e:
                logger.warning(f"RPC error for {url}: {e}")

        if attempt < cfg.RPC_MAX_RETRIES - 1:
            logger.info(f"⏳ Retrying in {cfg.RPC_RETRY_DELAY}s...")
            time.sleep(cfg.RPC_RETRY_DELAY)

    logger.error(f"❌ Web3 connection failed after {cfg.RPC_MAX_RETRIES} attempts")
    return None


def get_db_engine(echo: bool = False):
    """
    Get a cached SQLAlchemy engine.

    Args:
        echo: Enable SQL logging.

    Returns:
        SQLAlchemy engine.
    """
    global _db_engine

    if _db_engine is not None:
        return _db_engine

    try:
        _db_engine = create_engine(cfg.DATABASE_URL, echo=echo)
        with _db_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        logger.info("✅ Connected to PostgreSQL")
        return _db_engine
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


def reset_connections():
    """Reset cached connections (useful for testing)."""
    global _w3_instance, _db_engine
    _w3_instance = None
    _db_engine = None
