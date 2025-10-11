import sqlite3
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource (works in dev & PyInstaller EXE)"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


db_path = resource_path("orders.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_number TEXT,
    date TEXT,
    customer_name TEXT,
    order_type TEXT,
    items TEXT,
    total REAL
)
""")

conn.commit()
conn.close()
print("✅ Database setup complete.")
