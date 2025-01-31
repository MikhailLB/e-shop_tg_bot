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
    '''

    # Фильтруем данные: убираем строки, где обязательные поля пустые
    filtered_data = [row for row in data_list if row[0] and row[6] and row[7]]

    try:
        cursor.executemany(query, filtered_data)
        conn.commit()
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