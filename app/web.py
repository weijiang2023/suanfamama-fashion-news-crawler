import argparse
import os
import sqlite3
from typing import Any, Dict, List, Tuple

from flask import Flask, g, render_template, request, url_for, redirect


def create_app(db_path: str) -> Flask:
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "../templates"))
    app.config["DB_PATH"] = db_path

    def get_db() -> sqlite3.Connection:
        if "db" not in g:
            connection = sqlite3.connect(app.config["DB_PATH"])  # type: ignore
            connection.row_factory = sqlite3.Row
            g.db = connection
        return g.db

    @app.teardown_appcontext
    def close_db(exc: Exception | None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def build_filters() -> Tuple[str, List[Any]]:
        where_clauses: List[str] = []
        params: List[Any] = []
        q = request.args.get("q")
        source = request.args.get("source")
        category = request.args.get("category")
        days = request.args.get("days")
        if q:
            where_clauses.append("(title LIKE ? OR summary LIKE ? OR content LIKE ?)")
            pattern = f"%{q}%"
            params.extend([pattern, pattern, pattern])
        if source:
            where_clauses.append("source = ?")
            params.append(source)
        if category:
            where_clauses.append("category = ?")
            params.append(category)
        if days:
            try:
                days_int = int(days)
                where_clauses.append("(published_at >= datetime('now', ?))")
                params.append(f"-{days_int} days")
            except Exception:
                pass
        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        return where_sql, params

    @app.route("/")
    def index():
        db = get_db()
        page = max(1, int(request.args.get("page", 1)))
        per_page = min(100, max(5, int(request.args.get("per_page", 20))))
        offset = (page - 1) * per_page

        where_sql, params = build_filters()

        # Total count
        total = db.execute(f"SELECT COUNT(*) AS c FROM articles {where_sql}", params).fetchone()[0]

        rows = db.execute(
            f"""
            SELECT id, title, source, category, published_at, fetched_at, summary, substr(content, 1, 400) AS snippet, top_image, url
            FROM articles
            {where_sql}
            ORDER BY (published_at IS NULL), published_at DESC, fetched_at DESC
            LIMIT ? OFFSET ?
            """,
            params + [per_page, offset],
        ).fetchall()

        sources = db.execute(
            "SELECT source, COUNT(*) AS c FROM articles GROUP BY source ORDER BY c DESC LIMIT 30"
        ).fetchall()
        categories = db.execute(
            "SELECT category, COUNT(*) AS c FROM articles GROUP BY category ORDER BY c DESC"
        ).fetchall()

        return render_template(
            "index.html",
            rows=rows,
            page=page,
            per_page=per_page,
            total=total,
            sources=sources,
            categories=categories,
            args=request.args,
        )

    @app.route("/article/<int:article_id>")
    def article_detail(article_id: int):
        db = get_db()
        row = db.execute(
            "SELECT id, title, author, source, category, published_at, fetched_at, content, top_image, url FROM articles WHERE id = ?",
            (article_id,),
        ).fetchone()
        if not row:
            return redirect(url_for("index"))
        return render_template("article.html", article=row)

    return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Fashion News web UI")
    parser.add_argument("--db", default="/workspace/data/articles.db", help="Path to SQLite database file")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app = create_app(args.db)
    app.run(host=args.host, port=args.port, debug=args.debug)