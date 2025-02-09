import sqlite3

def remove_from_cart(user_id: int, item_id: int):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM cart
    WHERE user_id = ? AND id = ?
    """, (user_id, item_id))

    conn.commit()
    conn.close()