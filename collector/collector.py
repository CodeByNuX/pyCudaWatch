import datetime
import os
import sqlite3
import pynvml

doDEBUG = False

def collect():
    if doDEBUG: print("=== Collector starting ===")

    try:
        # init NVIDIA Management Library
        pynvml.nvmlInit()
        if doDEBUG: print("[DEBUG] NVML initialized")
        
        # Need to grab the handle for first GPU (0-index)
        gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        
        # Collect GPU Metrics.
        util = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
        mem  = pynvml.nvmlDeviceGetMemoryInfo(gpu_handle)
        temp = pynvml.nvmlDeviceGetTemperature(gpu_handle, 0)

        # timestamp for database entry.
        ts = datetime.datetime.now().isoformat()

        # Locate the directory where this script resides.
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.dirname(BASE_DIR)

        # navigate to /db director
        DB_PATH  = os.path.join(ROOT_DIR, "db", "gpu_stats.db")

        if doDEBUG: print("[DEBUG] DB path =", DB_PATH)
        if doDEBUG: print("[DEBUG] DB exists:", os.path.exists(DB_PATH))

        # Connect to SQLITE database
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        if doDEBUG: print("[DEBUG] Attempting INSERT...")
        
        # insert GPU metrics into table 'metrics'
        cur.execute("""
            INSERT INTO metrics (ts, gpu_util, mem_used, mem_total, temp)
            VALUES (?, ?, ?, ?, ?)
        """, (ts, util.gpu, mem.used, mem.total, temp))

        # Hourly cleanup
        now = datetime.datetime.now()

        doVacuum = False
        if now.minute == 0:
            cur.execute(""" 
                        DELETE FROM metrics WHERE ts < datetime('now', '-30 days')
                        """)
            doVacuum = True

        # Commit and close DB connection
        conn.commit()
        conn.close()

        if doVacuum:
            vacuumConn = sqlite3.connect(DB_PATH)
            vacuumCur = vacuumConn.cursor()
            vacuumCur.execute("VACUUM;")
            vacuumConn.commit()
            vacuumConn.close()
            if doDEBUG: print("[CLEANUP] Purged & Vacuumed.")


        print(f"[OK] Logged at {ts}")

    except Exception as e:
        print("[ERROR] Exception occurred:", e)

if __name__ == "__main__":
    collect()
