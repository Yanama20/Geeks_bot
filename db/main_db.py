import sqlite3
from db import queries

db = sqlite3.connect('db/store.sqlite3')

cursor = db.cursor()

async def create_db():
    if db:
        print('Базы данных подключены.')
    cursor.execute(queries.CREATE_TABLE_store)
    cursor.execute(queries.CREATE_TABLE_products_details)
    cursor.execute(queries.CREATE_TABLE_collections)


async def sql_insert_store(name_product, size, price, productid, photo):
    cursor.execute(queries.INSERT_store_query, (
        name_product, size, price, productid, photo
    ))
    db.commit()

async def sql_insert_product_details(productid, category, infoproduct):
    cursor.execute(queries.INSERT_products_details_query, (
        productid, category, infoproduct
    ))
    db.commit()

async def sql_insert_collection(collection, productid):
    cursor.execute(queries.INSERT_collections, (
        collection, productid
    ))
    db.commit()

# CRUD - 1
#=====================================================================================================

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute('''SELECT * FROM store
    INNER JOIN products_details ON store.productid = products_details.productid
    INNER JOIN collections ON store.productid = collections.productid''').fetchall()
    conn.close()
    return products

def delete_product(productid):
    conn = get_db_connection()

    conn.execute('DELETE FROM store WHERE productid = ?', (productid,))
    conn.execute('DELETE FROM products_details WHERE productid = ?', (productid,))
    conn.execute('DELETE FROM collections WHERE productid = ?', (productid,))
    conn.commit()
    conn.close()

#CRUD - update
######################################
def update_product_field(productid, field, new_value):
    conn = get_db_connection()
    store_table = ('name_product', 'size', 'price', 'photo')
    products_details_table = ('category', 'infoproduct')
    collections_table = ('collections')
    try:
        if field in store_table:
            query = f'UPDATE store SET {field} = ? WHERE productid = ?'
        elif field in products_details_table:
            query = f'UPDATE products_details SET {field} = ? WHERE productid = ?'
        elif field in collections_table:
            query = f'UPDATE collections SET {field} = ? WHERE productid = ?'
        else:
            raise ValueError(f'Поле {field} не найдено.')

        conn.execute(query,(new_value, productid))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'Ошибка - {e}')
    finally:
        conn.close()

