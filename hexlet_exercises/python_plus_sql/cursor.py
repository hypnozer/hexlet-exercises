# url: https://ru.hexlet.io/courses/python-sql/lessons/cursor/exercise_unit
# В практике вам доступны следующие таблицы
# orders
# order_id - id заказа
# customer_id - id покупателя
# order_date - дата заказа
# total_amount - сумма заказа
# customers

# customer_id - id покупателя
# customer_name - имя покупателя
# src/solution.py
# Допишите функцию get_order_sum(), которая принимает соединение и месяц,
# и возвращает общую сумму заказов каждого покупателя за этот месяц. Функция
# должна вернуть результат в виде строки:

# Покупатель Emily White совершил покупок на сумму 290
# Покупатель John Smith совершил покупок на сумму 130
# conn = psycopg2.connect('..')

# month = 2
# get_order_sum(conn, month)
# Покупатель Emily White совершил покупок на сумму 290
import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://tirion:secret@localhost:5432/tirion')


# BEGIN (write your solution here)
def get_order_sum(conn, month):
    sql = """SELECT customers.customer_name AS name, sum(orders.total_amount)
     AS amount FROM customers INNER JOIN orders ON
     customers.customer_id = orders.customer_id WHERE
     EXTRACT(MONTH FROM orders.order_date) = %s GROUP BY name;"""
    with conn.cursor() as curs:
        curs.execute(sql, (month,))
        stats = curs.fetchall()
        report = "\n".join([f"Покупатель {row[0]} совершил покупок на сумму {row[1]}"
        for row in stats])
    return report
# END


# BEGIN reference solution
def get_order_sum(conn, month):
    template = "Покупатель {customer} совершил покупок на сумму {total}".format
    with conn.cursor(cursor_factory=DictCursor) as cur:
        query = """
            SELECT
                c.customer_name,
                SUM(o.total_amount) AS total
            FROM
                customers c
            LEFT JOIN
                orders o ON c.customer_id = o.customer_id
            WHERE
                EXTRACT(MONTH FROM o.order_date) = %s
            GROUP BY
                c.customer_name;"""
        month_formated = '{:02d}'.format(month)
        cur.execute(query, (month_formated,))
        result = []
        for row in cur:
            customer_name = row['customer_name']
            total = row['total']
            result.append(template(customer=customer_name, total=total))
    conn.commit()

    return '\n'.join(result)
# END reference solution
