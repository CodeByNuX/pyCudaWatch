import os
import sqlite3


# ---
# Locate the directory where this script resides.
# Ensuring the database is created next to the script,
# ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gpu_stats.db")

# ---
# Create database & connection to database
# ---
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ---
# Create 'metrics' table if it does not exist.
#
# id          - Auto-increment primary key
# ts          - Timestamp
# gpu_util    - GPU utilization percentage
# mem_used    - GPU memory used (MiB)
# mem_total   - Total GPU memory (MiB)
# temp        - GPU temperature in Celsius
# ---
cur.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    gpu_util INTEGER,
    mem_used INTEGER,
    mem_total INTEGER,
    temp INTEGER
)
""")

# ---
# Commit and close database connection.
# ---
conn.commit()
conn.close()

print("Database initialized.")