CREATE_TABLE_store = """
    CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    size TEXT,
    price TEXT,
    productid TEXT,
    photo TEXT
    )
"""

CREATE_TABLE_products_details = """
    CREATE TABLE IF NOT EXISTS products_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    productid TEXT,
    category TEXT,
    infoproduct TEXT 
    )
"""

INSERT_store_query = """
    INSERT INTO store (name_product, size, price, productid, photo)
    VALUES (?, ?, ?, ?, ?)
"""

INSERT_products_details_query = """
    INSERT INTO products_details (productid, category, infoproduct)
    VALUES (?, ?, ?)
"""