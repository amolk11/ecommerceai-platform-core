from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from platform_core.config import settings

_engine: Engine | None = None


def get_platform_engine() -> Engine:
    """
    Return singleton Platform DB engine.
    """

    global _engine

    if _engine is None:
        _engine = create_engine(
            settings.db_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )

    return _engine
