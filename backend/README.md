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

## CI/CD to Render

This repo includes a GitHub Actions workflow at `.github/workflows/backend-ci-deploy.yml` that:
- Runs tests on pushes to `main` for changes under `backend/`
- Triggers a Render deploy using a Deploy Hook URL

### Setup
1. In Render, create a Web Service pointing at `backend/` with:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - Environment Variables:
     - Copy from `.env` (e.g., `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_DB_URL`)
2. In Render service Settings, copy the Deploy Hook URL.
3. In GitHub repo settings, add a repository secret:
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: the Deploy Hook URL from Render

On subsequent pushes to `main`, the workflow will run tests and trigger a deploy.