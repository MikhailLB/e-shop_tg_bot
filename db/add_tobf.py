
import sqlite3


conn = sqlite3.connect("../omnia_shop.db")
cursor = conn.cursor()


cursor.execute("""
    ALTER TABLE users ADD COLUMN delivery_method TEXT;
    
""")


conn.commit()
conn.close()