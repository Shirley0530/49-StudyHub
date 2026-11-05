import sqlite3
from pathlib import Path
from flask import g, current_app

def get_db():
    if "db" not in g:
        db_path = Path(current_app.root_path) / "studyhub.db"
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    from flask import Flask
    # app.py 在启动时调用；使用独立连接初始化数据库
    db_path = Path(__file__).resolve().parents[1] / "studyhub.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            course TEXT NOT NULL DEFAULT '',
            category TEXT NOT NULL DEFAULT '',
            file_type TEXT NOT NULL DEFAULT '',
            description TEXT NOT NULL DEFAULT '',
            filename TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
