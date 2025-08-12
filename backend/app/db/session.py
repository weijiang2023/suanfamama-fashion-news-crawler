from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from app.core.config import get_settings

_settings = get_settings()

_engine: Optional[AsyncEngine] = None
_SessionLocal: Optional[async_sessionmaker[AsyncSession]] = None


def _create_engine() -> Optional[AsyncEngine]:
    if not _settings.supabase_db_url:
        return None

    db_url = _settings.supabase_db_url

    if db_url.startswith("postgresql+asyncpg://") or db_url.startswith("postgresql://"):
        async_url = db_url if db_url.startswith("postgresql+asyncpg") else db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgres://"):
        # old scheme
        async_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    else:
        # As a safe fallback, try to prefix with asyncpg
        async_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

    return create_async_engine(async_url, echo=_settings.debug, pool_pre_ping=True, pool_size=5, max_overflow=10)


def get_engine() -> Optional[AsyncEngine]:
    global _engine, _SessionLocal
    if _engine is None:
        _engine = _create_engine()
        if _engine is not None:
            _SessionLocal = async_sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)
    return _engine


def get_session_maker() -> Optional[async_sessionmaker[AsyncSession]]:
    if _SessionLocal is None:
        get_engine()
    return _SessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker()
    if session_maker is None:
        raise RuntimeError("Database is not configured. Set SUPABASE_DB_URL in environment.")

    async with session_maker() as session:
        yield session


async def ping_database() -> Optional[bool]:
    engine = get_engine()
    if engine is None:
        return None
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False