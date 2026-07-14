import sqlite3

conn = sqlite3.connect("traces.db")
cursor = conn.execute("""
    SELECT name, (end_time - start_time) AS duration
    FROM spans
""")

for name, duration in cursor:
    print(f"{name}: {duration}")

conn.close()