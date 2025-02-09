import sqlite3

# Подключение к базе данных (или создание, если её нет)
conn = sqlite3.connect("../omnia_shop.db")
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE administrators ADD COLUMN name TEXT')
except sqlite3.OperationalError:
    print("Колонка 'order_status' уже существует.")


conn.commit()
conn.close()