import sqlite3

def add_user(telegram_user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (id, name, surname, country, city, street, district, post_index)
    VALUES (?, 'None', 'None', 'None', 'None', 'None', 'None', '1')
    """, (telegram_user_id,))

    conn.commit()
    conn.close()



def update_user_data(user_id, name, second_name, city, street, district, index, telephone, delivery_method):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET name = ?, surname = ?, city = ?, street = ?, district = ?, post_index = ?, telephone = ?, delivery_method = ?
    WHERE id = ?
    """, (name, second_name, city, street, district, index, telephone, delivery_method, user_id))
    conn.commit()
    conn.close()

def delete_user_data(user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET name = ?, surname = ?, city = ?, street = ?, district = ?, post_index = ?, telephone = ?, delivery_method = ?
        WHERE id = ?
    """, ('None', 'None', 'None', 'None', 'None', 1, 1, 'None', user_id))
    conn.commit()
    conn.close()

def add_review(user_id, rating, comment, user_name):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reviews (user_id, rating, comment, user_name)
    VALUES (?, ?, ?, ?)
    """, (user_id, rating, comment, user_name))

    conn.commit()
    conn.close()


def add_cart_to_db(user_id, name, url, size, color, description, photo_id, price, product_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO cart (user_id, name, url, size, color, description, photo_id, price, product_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name, url, size, color, description, photo_id, price, product_id))

        conn.commit()
    finally:
        conn.close()



def insert_products(data_list):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    query = '''
        INSERT INTO products (name, url, size, color, description, photo_id, price, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(name, url) DO UPDATE SET
            name= excluded.name,
            url= excluded.url,
            size = excluded.size,
            color = excluded.color,
            description = excluded.description,
            photo_id = excluded.photo_id,
            price = excluded.price,
            category = excluded.category
        '''

    filtered_data = [row for row in data_list if row[0] and row[6] and row[7]]

    try:
        cursor.executemany(query, filtered_data)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Ошибка целостности данных: {e}")
    finally:
        conn.close()


def delete_cart_item(user_id: int, product_id: int):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
        (user_id, product_id)
    )

    conn.commit()
    conn.close()

def add_order_status(order_id, status):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE orders
    SET order_status = ?
    WHERE id = ?
    """, (status, order_id))

    conn.commit()
    conn.close()

def add_order_delivery_link(order_id, tracking):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE orders
    SET tracking = ?
    WHERE id = ?
    """, (tracking, order_id))

    conn.commit()
    conn.close()

def delete_product_by_name(name):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM products WHERE name = ? OR url = ?", (name,name))


    conn.commit()
    conn.close()


def add_admin_to_db(telegram_id: int, name):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO administrators (telegram_id, role, name) VALUES (?, 'admin', ?)",
        (telegram_id,name)
    )

    conn.commit()
    conn.close()

def delete_admin_from_bd(telegram_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM administrators WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()
