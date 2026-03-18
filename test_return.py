import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'library.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT id, status FROM transactions WHERE status = 'returned' ORDER BY id DESC LIMIT 5")
returned = c.fetchall()
print("Returned transactions:", returned)
conn.close()
