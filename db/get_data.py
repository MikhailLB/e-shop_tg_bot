import sqlite3


def get_info_for_account_check(user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, surname, country FROM users WHERE id = ?
    """, (user_id,))

    user_info = cursor.fetchone()
    conn.close()

    if user_info:
        return user_info
    else:
        return None


def get_reviews():
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_name, rating, comment, created_at
    FROM reviews
    ORDER BY created_at DESC
    """, )

    reviews = cursor.fetchall()

    conn.close()
    return reviews

def find_id(user_id, thing_link):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()


    cursor.execute("""
    SELECT id FROM cart WHERE user_id = ? AND thing_link = ?
    """, (user_id, thing_link))

    cart_items = cursor.fetchall()

    conn.close()

    if cart_items:
        return [item[0] for item in cart_items]


def get_products_by_category(category):

    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, name, url, size, color, description, photo_id, price 
        FROM products WHERE category = ?
    ''', (category,))

    products = cursor.fetchall()
    conn.close()


    return [{"id": row[0], "name": row[1], "url": row[2], "size": row[3], "color": row[4],
             "description": row[5], "photo_id": row[6], "price": row[7]} for row in products]

def check_existing_products(data_list):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    query = '''
    SELECT * FROM products WHERE name = ? AND url = ?
    '''

    existing_products = []

    for row in data_list:
        name, url = row[0], row[1]
        cursor.execute(query, (name, url))
        results = cursor.fetchall()
        if results:
            existing_products.extend(results)

    conn.close()
    return existing_products


def get_products_by_id(id):

    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, name, url, size, color, description, photo_id, price 
        FROM products WHERE id = ?
    ''', (id,))

    products = cursor.fetchall()
    conn.close()

    return products

def get_cart_items(user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT name, description, size, color, price, photo_id, product_id FROM cart WHERE user_id = ?;
        """, (user_id,))

        results = cursor.fetchall()
        return results
    finally:
        conn.close()


def find_item_in_cart(product_id, user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT name FROM cart WHERE product_id = ? AND user_id = ?;
        """, (product_id, user_id,))

        results = cursor.fetchall()
        return results
    finally:
        conn.close()

def get_faq():
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT question,answer FROM faq;
        """,)

        results = cursor.fetchall()
        return results
    finally:
        conn.close()

def get_item_for_name(name):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, name, description, size, color, price, photo_id FROM products WHERE name = ?;
        """, (name,))

        results = cursor.fetchall()
        return results
    finally:
        conn.close()


def get_item_for_link(url):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, name, description, size, color, price, photo_id FROM products WHERE url = ?;
        """, (url,))

        results = cursor.fetchall()
        return results
    finally:
        conn.close()

def get_orders(user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
                SELECT product_name, total_price, delivery_method, size, color, address, order_status, tracking
                FROM orders
                WHERE user_id = ? AND order_status != "Заказ выполнен";
            """, (user_id,))

        results = cursor.fetchall()
        return results
    finally:
        conn.close()


def get_all_orders(user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
                SELECT product_name, total_price, delivery_method, size, color, address, order_status, tracking
                FROM orders
                WHERE user_id = ? AND order_status == "Заказ выполнен";
            """, (user_id,))

        results = cursor.fetchall()
        return results
    finally:
        conn.close()

def get_orders_for_admin():
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
                SELECT id, product_name, total_price, delivery_method, size, color, address, order_status, tracking
                FROM orders
                WHERE order_status != "Заказ выполнен";
            """,)

        results = cursor.fetchall()
        return results
    finally:
        conn.close()

def get_all_orders_for_admin():
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
                SELECT id, product_name, total_price, delivery_method, size, color, address, order_status, tracking
                FROM orders
                WHERE order_status == "Заказ выполнен";
            """,)

        results = cursor.fetchall()
        return results
    finally:
        conn.close()


def fetch_admins():
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT telegram_id, role FROM administrators")
    admins = dict(cursor.fetchall())

    conn.close()

    return admins

def admins_name():
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT telegram_id, name FROM administrators")
    admins = dict(cursor.fetchall())

    conn.close()

    return admins

def get_product_by_id(id):

    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, name, url, size, color, description, price 
        FROM products WHERE id = ?
    ''', (id,))

    products = cursor.fetchall()
    conn.close()

    return products


def get_info_about_account(user_id):
    conn = sqlite3.connect("omnia_shop.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, surname, city, street, district, post_index, telephone, delivery_method  FROM users WHERE id = ?
    """, (user_id,))

    user_info = cursor.fetchone()
    conn.close()

    if user_info:
        return user_info
    else:
        return None