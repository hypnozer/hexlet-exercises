# url: https://ru.hexlet.io/courses/python-sql/lessons/query/exercise_unit
#
# Создайте функцию, batch_insert(), которая принимает соединение, и список
# товаров
#  и массово добавляет их в базу. Каждый товар представлен словарем с ключами
#  name, price, и quantity. Для безопасной и быстрой работы с базой данных
#  используйте плейсхолдеры.

# Так же создайте функцию get_all_products(), которая принимает соединение, и
# возвращает весь список товаров, отсортированый по цене товара DESC.

# CREATE TABLE products (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     price NUMERIC NOT NULL,
#     quantity INT NOT NULL
# );
# conn = psycopg2.connect('..')

# products = [
#     {'name': 'milk', 'price': 12, 'quantity': 20},
#     {'name': 'bread', 'price': 3, 'quantity': 10},
#     {'name': 'orange', 'price': 6, 'quantity': 5}
# ]
# get_all_products(conn) # []

# batch_insert(conn, products)
# get_all_products(conn)
# # [(1, 'milk', 12, 20),
# #  (3, 'orange', 6, 5),
# #  (2, 'bread', 3, 10)]
# Подсказки
# Для массовой вставки в БД используется функция execute_values

import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect('postgresql://tirion:secret@localhost:5432/tirion')


# BEGIN (write your solution here)
def batch_insert(conn, products):
    with conn.cursor() as curs:
        for product in products:
            execute_values(curs, """INSERT INTO products (name, price, quantity)
             VALUES (%(name)s, %(price)s, %(quantity)s);""", products)
    conn.commit()
    conn.close()


def get_all_products(conn):
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM products ORDER BY price DESC;")
        return curs.fetchall()
# END

# BEGIN reference solution
def batch_insert(conn, products):
    with conn.cursor() as cur:
        values = [(p['name'], p['price'], p['quantity']) for p in products]

        insert_query = "INSERT INTO products (name, price, quantity) VALUES %s"

        execute_values(cur, insert_query, values)
    conn.commit()


def get_all_products(conn):
    with conn.cursor() as cur:
        sql = "SELECT * FROM products ORDER BY price DESC;"
        cur.execute(sql)
        result = cur.fetchall()
    conn.commit()
    return result
# END reference solution
