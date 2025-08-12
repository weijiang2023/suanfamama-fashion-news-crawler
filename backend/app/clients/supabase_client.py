from typing import Optional

from app.core.config import get_settings

_settings = get_settings()

_supabase_client = None


def get_supabase_client():  # type: ignore[override]
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not _settings.supabase_url or not _settings.supabase_anon_key:
        return None

    try:
        from supabase import create_client
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Supabase client is not installed. Add 'supabase' to requirements.") from exc

    _supabase_client = create_client(_settings.supabase_url, _settings.supabase_anon_key)
    return _supabase_client


def ping_supabase() -> Optional[bool]:
    client = get_supabase_client()
    if client is None:
        return None
    try:
        # Lightweight call: select 1 from any table via RPC or call auth settings
        # Here we'll call auth settings to avoid needing a table
        _ = client.auth.get_session()
        return True
    except Exception:
        return False