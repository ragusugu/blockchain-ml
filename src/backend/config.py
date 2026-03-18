"""
Centralized Configuration
Single source of truth for all environment variables and settings.
Import: from config import cfg
"""
import os


class _Config:
    """Application configuration loaded from environment variables."""

    # ── RPC Endpoints ──────────────────────────────────────────────
    RPC_URL: str = os.getenv('RPC_URL', 'https://ethereum.publicnode.com')
    ANKR_RPC_URL: str = os.getenv('ANKR_RPC_URL', 'https://rpc.ankr.com/eth')

    RPC_FALLBACK_URLS: list = [
        "https://ethereum.publicnode.com",
        "https://eth-mainnet.public.blastapi.io",
        "https://cloudflare-eth.com",
        "https://rpc.ankr.com/eth",
        "https://1rpc.io/eth",
    ]

    RPC_TIMEOUT: int = int(os.getenv('RPC_TIMEOUT', '20'))
    RPC_MAX_RETRIES: int = int(os.getenv('RPC_MAX_RETRIES', '5'))
    RPC_RETRY_DELAY: int = int(os.getenv('RPC_RETRY_DELAY', '5'))

    # ── Database ───────────────────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        'DATABASE_URL',
        'postgresql://blockchain_user:change-me-to-secure-password@postgres:5432/blockchain_db'
    )

    # ── ETL Pipeline ──────────────────────────────────────────────
    BATCH_SIZE: int = int(os.getenv('BATCH_SIZE', '10'))
    MAX_WORKERS: int = int(os.getenv('MAX_WORKERS', '5'))

    # ── Streaming ─────────────────────────────────────────────────
    POLLING_INTERVAL: int = int(os.getenv('POLLING_INTERVAL', '10'))
    ANKR_POLLING_INTERVAL: int = int(os.getenv('ANKR_POLLING_INTERVAL', '12'))
    ANKR_BATCH_SIZE: int = int(os.getenv('ANKR_BATCH_SIZE', '10'))
    STREAMING_ENABLED: bool = os.getenv('STREAMING_ENABLED', 'true').lower() == 'true'

    # ── ML / AI ───────────────────────────────────────────────────
    MODEL_ENABLED: bool = os.getenv('MODEL_ENABLED', 'true').lower() == 'true'
    MODEL_PATH: str = os.getenv('MODEL_PATH', 'fraud_model.pkl')
    FRAUD_THRESHOLD: float = float(os.getenv('FRAUD_THRESHOLD', '0.7'))
    TRAIN_MODEL_ON_BATCH: bool = os.getenv('TRAIN_MODEL_ON_BATCH', 'false').lower() == 'true'

    # ── API / Dashboard ───────────────────────────────────────────
    MAX_BLOCKS_PER_REQUEST: int = int(os.getenv('MAX_BLOCKS_PER_REQUEST', '1'))
    STORE_BATCH_RESULTS: bool = os.getenv('STORE_BATCH_RESULTS', 'true').lower() == 'true'

    # ── Output ────────────────────────────────────────────────────
    OUTPUT_MODE: str = os.getenv('OUTPUT_MODE', 'console')
    WEBHOOK_URL: str = os.getenv('WEBHOOK_URL', '')

    # ── Scheduler ─────────────────────────────────────────────────
    ETL_SCHEDULE_HOUR: str = os.getenv('ETL_SCHEDULE_HOUR', '0')
    ETL_SCHEDULE_MINUTE: str = os.getenv('ETL_SCHEDULE_MINUTE', '0')

    # ── Disk Cleanup ──────────────────────────────────────────────
    DISK_THRESHOLD_PERCENT: int = int(os.getenv('DISK_THRESHOLD_PERCENT', '20'))

    @property
    def rpc_candidates(self) -> list:
        """Get ordered list of RPC URLs to try (env var + fallbacks)."""
        urls = [u.strip() for u in self.RPC_URL.split(',') if u.strip()]
        return urls or self.RPC_FALLBACK_URLS

    def _check_db_credentials(self) -> None:
        """Warn if default database credentials are in use."""
        import warnings
        if 'change-me-to-secure-password' in self.DATABASE_URL:
            warnings.warn(
                "Using default database password. Set DATABASE_URL env var with secure credentials.",
                stacklevel=2,
            )


# Singleton instance — import this everywhere
cfg = _Config()
cfg._check_db_credentials()
