import sqlite3


# ======================================
# СОЗДАНИЕ БАЗЫ ДАННЫХ
# ======================================

def create_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        crypto TEXT,
        amount REAL,
        price REAL,
        status TEXT,
        check_photo TEXT
    )
    """)

    conn.commit()
    conn.close()


# ======================================
# СОЗДАНИЕ ЗАЯВКИ
# ======================================

def add_order(
    user_id,
    username,
    crypto,
    amount,
    price
):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orders
    (user_id, username, crypto, amount, price, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        user_id,
        username,
        crypto,
        amount,
        price,
        "Ожидает чек"
    ))

    conn.commit()

    order_id = cursor.lastrowid

    conn.close()

    return order_id


# ======================================
# ДОБАВЛЕНИЕ ЧЕКА
# ======================================

def add_check(order_id, photo_id):

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE orders
    SET check_photo = ?, status = ?
    WHERE id = ?
    """,
    (
        photo_id,
        "Чек отправлен"
    ))

    conn.commit()
    conn.close()


# ======================================
# ИЗМЕНЕНИЕ СТАТУСА
# ======================================

def update_status(order_id, status):

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE orders
    SET status = ?
    WHERE id = ?
    """,
    (
        status,
    ))

    conn.commit()
    conn.close()


# ======================================
# ПОЛУЧЕНИЕ ЗАЯВКИ
# ======================================

def get_order(order_id):

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM orders
    WHERE id = ?
    """,
    (
        order_id,
    ))

    order = cursor.fetchone()

    conn.close()

    return order


# ======================================
# СТАТИСТИКА
# ======================================

def get_stats():

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM orders
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result
