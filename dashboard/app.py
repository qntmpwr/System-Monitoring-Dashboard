"""
Flask API: Serves Real-Time System Monitor metrics to browser dashboard
"""

from flask import Flask, render_template, jsonify
import sqlite3
import time
import psutil
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "system-metrics.db")


def get_latest_system_metrics():
    with sqlite3.connect(DATA_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT timestamp, cpu, memory, disk, net_sent, net_recv 
        FROM metrics2 
        ORDER BY id DESC 
        LIMIT 1
    """)
    return cursor.fetchone()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/latest")
def api_latest():
    uptime_seconds = time.time() - psutil.boot_time()
    row = get_latest_system_metrics()
    if row is None:
        return jsonify({
            "timestamp": None,
            "cpu": None,
            "memory": None,
            "disk": None,
            "net_sent": None,
            "net_recv": None,
            "uptime": uptime_seconds
        })
    return jsonify({
            "timestamp": row[0],
            "cpu": row[1],
            "memory": row[2],
            "disk": row[3],
            "net_sent": row[4],
            "net_recv": row[5],
            "uptime": uptime_seconds
        })

if __name__ == "__main__":
    app.run(debug=True)