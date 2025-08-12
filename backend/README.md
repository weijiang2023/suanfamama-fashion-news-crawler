# Backend (FastAPI + Supabase Postgres)

## Quickstart

1. Create a `.env` file in this directory:

```
cp .env.example .env
```

2. (Optional) Configure Supabase:
- Set `SUPABASE_URL` and `SUPABASE_ANON_KEY` for the Supabase client.
- Set `SUPABASE_DB_URL` to connect directly to the Supabase Postgres database.

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run the server:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. Health check:
- `GET /health` returns service status, DB connectivity, and Supabase availability.

## Testing

```
pytest -q
```