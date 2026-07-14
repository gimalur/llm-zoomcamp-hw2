import sqlite3

conn = sqlite3.connect("traces.db")
cursor = conn.execute("""
    SELECT name, input_tokens
    FROM spans
    WHERE name = 'llm'
""")

for name, input_tokens in cursor:
    print(f"{name}: {input_tokens}")

conn.close()