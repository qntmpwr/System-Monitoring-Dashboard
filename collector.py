"""
Real-Time System Metric Collector
Reads CPU, Memory, Disk, Network Usage and writes to SQLite file
"""

import sqlite3
import time
import psutil
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "system-metrics.db")


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu REAL NOT NULL,
            memory REAL NOT NULL, 
            disk REAL NOT NULL,
            net_sent INTEGER NOT NULL,
            net_recv INTEGER NOT NULL
        )
    """)

def collect_once():
    ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    cpu = psutil.cpu_percent(interval=2)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    net = psutil.net_io_counters()
    net_sent = net.bytes_sent
    net_recv = net.bytes_recv

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
        "INSERT INTO metrics2 (timestamp, cpu, memory, disk, net_sent, net_recv) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (ts, cpu, memory, disk, net_sent, net_recv),
    )

    print("Wrote row:", ts, cpu, memory, disk, net_sent, net_recv)

def main() -> None:
    init_db()
    while True:
        collect_once()
        #time.sleep(2)

if __name__ == "__main__":
    main()