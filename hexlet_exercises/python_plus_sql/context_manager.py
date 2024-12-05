# url: https://ru.hexlet.io/courses/python-sql/lessons/context-managers
# /exercise_unit
#
# Напишите функцию get_all_cars(), которая принимает соединение, и возвращает
# все автомобили, которые содержатся в базе данных в таблице cars.

# Таблица содержит следующие поля:

# id — идентификатор автомобиля, первичный ключ, который автоматически
# генерируется базой данных
# brand — марка автомобиля
# model — модель автомобиля
# Записи должны быть отсортированы по марке автомобиля в прямом порядке. Для
# автоматического закрытия соединения используйте контекстный менеджер.

# conn = psycopg2.connect('..')

# get_all_cars(conn)
# # [(1, 'kia', 'sorento'),
# #  (2, 'bmw', 'x5')]
# Подсказки
# В этой практике уже созданно соединение conn, и вам не нужно использовать
# контекстный менеджер with conn
# Для получения результата запроса используйте метод курсора cursor.fetchall()
import psycopg2

conn = psycopg2.connect('postgresql://tirion:secret@localhost:5432/tirion')


# BEGIN (write your solution here)
def get_all_cars(conn):
    sql = """SELECT * FROM cars ORDER BY brand ASC"""
    with conn.cursor() as curs:
        curs.execute(sql)
        return curs.fetchall()
# END


# BEGIN reference solution
# def get_all_cars(conn):
#     with conn.cursor() as c:
#         sql = "SELECT * FROM cars ORDER BY brand ASC;"
#         c.execute(sql)
#         result = c.fetchall()
#     return result
# END reference solution

