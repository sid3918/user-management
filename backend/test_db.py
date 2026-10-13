from database import get_connection

conn = get_connection()
with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) AS total FROM users")
    print("Connected OK. Rows in users:", cur.fetchone()["total"])
conn.close()