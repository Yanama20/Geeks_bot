import sqlite3
from db import queries

db = sqlite3.connect('db/db.sqlite3')

cursor = db.cursor()

async def create_db():
    if db:
        print('Базы данных подключены.')
    cursor.execute(queries.CREATE_TABLE_store)
    cursor.execute(queries.CREATE_TABLE_products_details)


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