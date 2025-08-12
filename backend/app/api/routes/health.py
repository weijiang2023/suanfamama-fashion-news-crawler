from fastapi import APIRouter

from app.clients.supabase_client import ping_supabase
from app.db.session import ping_database

router = APIRouter()


@router.get("/health")
async def health_check():
    db_ok = await ping_database()
    supabase_ok = ping_supabase()

    return {
        "status": "ok",
        "database": (
            "skipped" if db_ok is None else ("up" if db_ok is True else "down")
        ),
        "supabase": (
            "skipped" if supabase_ok is None else ("up" if supabase_ok is True else "down")
        ),
    }