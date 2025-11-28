from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import os

app = FastAPI()

# DB path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(ROOT_DIR, "db", "gpu_stats.db")

# templates + static dirs
templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "dashboard", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "dashboard", "static")), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history")
def history(limit: int = 1000):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT ts, gpu_util, mem_used, mem_total, temp
        FROM metrics
        ORDER BY ts ASC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()

    return [
        {
            "ts": r[0],
            "gpu_util": r[1],
            "mem_used": r[2],
            "mem_total": r[3],
            "temperature": r[4]
        }
        for r in rows
    ]
