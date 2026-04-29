import sqlite3
import os

#DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "system-metrics.db")
DB_PATH = r"C:\Users\camal\PycharmProjects\system-monitor\data\system-metrics.db"


conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

for row in c.execute("SELECT * FROM metrics2"):
    print(row)

conn.close()
