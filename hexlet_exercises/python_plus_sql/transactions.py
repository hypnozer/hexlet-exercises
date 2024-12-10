# url: https://ru.hexlet.io/courses/python-sql/lessons/transaction/exercise_unit

# В этом упражнении уже создано соединение с базой данных и следующие таблицы:

# posts, которая содержит информацию о постах:

# id — id поста, первичный ключ, генерируется базой данных автоматически
# title — название поста
# content — содержание поста
# author_id — id автора
# created_at - дата создания поста, генерируется автоматически
# comments, которая содержит информацию о комментариях:

# id - id комментария, первичный ключ, генерируется базой данных автоматически
# post_id - id поста, к которому оставлен комментарий
# author_id - id автора
# content - содержание комментария
# created_at - дата создания комментария, генерируется автоматически
# src/solution.py
# Реализуйте следующие функции:

# create_post() - принимает соединение с базой данных и словарь с данными поста.
# Словарь должен содержать ключи: 'title', 'content', 'author_id'. Функция должна
# создать новый пост и вернуть его id.

# add_comment() - принимает соединение с базой данных и словарь с данными
# комментария. Словарь должен содержать ключи: 'post_id', 'author_id', 'content'.
# Функция должна добавить новый комментарий и вернуть его id.

# get_latest_posts() - принимает соединение с базой данных и количество постов n.
# Возвращает список n последних постов с их комментариями. Каждый элемент списка
# должен быть словарем с ключами: 'id', 'title', 'content', 'author_id',
# 'created_at', 'comments'. 'comments' - это список словарей с ключами: 'id',
# 'author_id', 'content', 'created_at'

# conn = psycopg2.connect('..')

# get_latest_posts(conn, 1)
# # []

# post = {'title': 'My Super Post', 'content': 'text', 'author_id': 42}
# create_post(conn, post) # 1

# comment = {'post_id': 1, 'author_id': 42, 'content': 'wow such post'}
# add_comment(conn, comment) # 1

# get_latest_posts(conn, 1)
# [{
# 'id': 1,
# 'title': 'My Super Post',
# 'content': 'text',
# 'author_id': 42,
# 'created_at': datetime.datetime(2022, 7, 19, 14, 32, 37, 123857),
# 'comments': [
#  {
#   'id': 1,
#   'author_id': 42,
#   'content': 'wow such post',
#   'created_at': datetime.datetime(2022, 8, 19, 14, 32, 37, 135319)
#   }
#  ]}]
import psycopg2
from psycopg2.extras import DictCursor,RealDictCursor

conn = psycopg2.connect('postgresql://tirion:secret@localhost:5432/tirion')


# BEGIN (write your solution here)
def create_post(conn, coll):
    sql = """INSERT INTO posts (title, content, author_id)
    VALUES (%s, %s, %s) RETURNING id;"""
    with conn.cursor() as cur:
        cur.execute(
            sql, (coll['title'], coll['content'], coll['author_id'])
        )
        post_id = cur.fetchone()[0]
    return post_id


def add_comment(conn, coll):
    sql = """INSERT INTO comments (post_id, author_id, content)
    VALUES (%s, %s, %s) RETURNING id;"""
    with conn.cursor() as cur:
        cur.execute(
            sql, (coll['post_id'], coll['author_id'], coll['content'])
        )
        comment_id = cur.fetchone()[0]
    return comment_id


def get_latest_posts(conn, n):
    sql_posts = """SELECT * FROM posts ORDER BY created_at DESC LIMIT %s"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql_posts, (n,))
        posts = cur.fetchall()
        if posts:
            ids = tuple((row['id'] for row in posts))
            placeholders = ', '.join(['%s'] * len(ids))
            sql_comments = f'SELECT * FROM comments WHERE post_id IN ({placeholders})'
            cur.execute(sql_comments, ids)
            comments = cur.fetchall()
        else:
            comments = []
    comments_by_post = {}
    for comment in comments:
        if comment['post_id'] not in comments_by_post:
            comments_by_post[comment['post_id']] = []
        comments_by_post[comment['post_id']].append(comment)
    for post in posts:
        post['comments'] = comments_by_post.get(post['id'], [])
    return posts
# END


# BEGIN reference solution
def get_latest_posts(conn, n):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            SELECT
                p.*,
                c.id as comment_id,
                c.author_id as comment_author_id,
                c.content as comment_content,
                c.created_at as comment_created_at
            FROM posts p
            LEFT JOIN comments c ON p.id = c.post_id
            WHERE p.id IN (
                SELECT id FROM posts
                ORDER BY created_at DESC
                LIMIT %s
            )
        """, (n,))

        rows = cur.fetchall()

        posts_dict = {}
        for row in rows:
            post_id = row['id']
            if not posts_dict.get(post_id):
                posts_dict[post_id] = {
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'author_id': row['author_id'],
                    'created_at': row['created_at'],
                    'comments': []
                }

            if row.get('comment_id'):
                posts_dict[post_id]['comments'].append({
                    'id': row['comment_id'],
                    'author_id': row['comment_author_id'],
                    'content': row['comment_content'],
                    'created_at': row['comment_created_at']
                })

        return list(posts_dict.values())
# END reference solution
