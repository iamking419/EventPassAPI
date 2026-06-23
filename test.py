from app.core.database import engine

try:
    conn = engine.connect()
    print("DB CONNECTED 🔥")
    conn.close()
except Exception as e:
    print("DB FAILED:", e)