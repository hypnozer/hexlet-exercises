# url: https://ru.hexlet.io/courses/python-sql/lessons/dao/exercise_unit

# src/solution.py
# Мы уже рассмотрели методы сохранения и поиска конкретной сущности в таблице.
# В дополнение к ним, может понадобиться метод для извлечения всех сущностей
# из таблицы. В этом упражнении вам предстоит создать такой метод.


# В упражнении уже созданы модели для сущностей Course и Lesson

# src/solution.py
# В упражнении уже созданы функции для работы с таблицей курсов courses. Есть
# функции для сохранения курса и поиска конкретного курса по его идентификатору.

# Создайте функции для работы с сущностью Lesson:

# save_lesson() - принимает соединение и урок, сохраняет его в базу и возвращает
# id урока
# find_lesson() - принимает соединение и id урока, и возращает его из базы
# get_course_lessons() - принимает соединение и id курса, и возвращает все
# уроки,
# связанные с этим курсом. Отсортируйте результат по возрастанию id урока
import psycopg2
from psycopg2.extras import NamedTupleCursor


from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    name: str
    description: str
    id: Optional[int] = None


@dataclass
class Lesson:
    name: str
    text: str
    course_id: int
    id: Optional[int] = None


conn = psycopg2.connect('postgresql://tirion:secret@localhost:5432/tirion')


def commit(conn):
    conn.commit()


def save_course(conn, course):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        if course.id is None:
            cur.execute(
                """INSERT INTO courses (name, description) VALUES (%s, %s)
                RETURNING id;""",
                (course.name, course.description)
            )
            course.id = cur.fetchone().id
        else:
            cur.execute(
                "UPDATE courses SET name = %s, description = %s WHERE id = %s;",
                (course.name, course.description, course.id)
            )
    return course.id


def find_course(conn, course_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """SELECT id, name, description FROM
            courses WHERE id = %s;""", (course_id,))
        result = cur.fetchone()
        if result:
            return Course(
                id=result.id,
                name=result.name,
                description=result.description
                )
    return None


def get_all_courses(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT id, name, description FROM courses;")
        return [
            Course(id=row.id, name=row.name, description=row.description)
            for row in cur.fetchall()
        ]


# BEGIN (write your solution here)
def save_lesson(conn, lesson):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        if lesson.id is None:
            cur.execute(
                """INSERT INTO lessons (name, text, course_id) VALUES (%s, %s, %s)
                RETURNING id;""",
                (lesson.name, lesson.text, lesson.course_id)
            )
            lesson.id = cur.fetchone().id
        else:
            cur.execute(
                """UPDATE lessons SET name = %s, text = %s, course_id = %s
                WHERE id = %s;""",
                (lesson.name, lesson.text, lesson.course_id, lesson.id)
            )
    return lesson.id


def find_lesson(conn, lesson_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("""SELECT id, name, text, course_id
        FROM lessons WHERE id = %s;""", (lesson_id,))
        result = cur.fetchone()
        if result:
            return Lesson(
                id=result.id,
                name=result.name,
                text=result.text,
                course_id=result.course_id
                )
    return None


def get_course_lessons(conn, course_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("""SELECT id, name, text, course_id FROM lessons
        WHERE course_id = %s ORDER BY id ASC;""", (course_id,))
        return [
        Lesson(
            id=row.id,
            name=row.name,
            text=row.text,
            course_id=row.course_id
        )
        for row in cur.fetchall()
    ]
# END


# BEGIN reference solution
def save_lesson(conn, lesson):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        if lesson.id is None:
            cur.execute(
                "INSERT INTO lessons (name, text, course_id) VALUES (%s, %s, %s) RETURNING id;",
                (lesson.name, lesson.text, lesson.course_id)
            )
            lesson.id = cur.fetchone().id
        else:
            cur.execute(
                "UPDATE lessons SET name = %s, text = %s, course_id = %s WHERE id = %s;",
                (lesson.name, lesson.text, lesson.course_id, lesson.id)
            )
    return lesson.id


def find_lesson(conn, lesson_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT id, name, text, course_id FROM lessons WHERE id = %s;", (lesson_id,))
        result = cur.fetchone()
        if result:
            return Lesson(
                id=result.id,
                name=result.name,
                text=result.text,
                course_id=result.course_id
                )
    return None


def get_course_lessons(conn, course_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM lessons WHERE course_id = %s ORDER BY id;", (course_id,))
        return [
            Lesson(id=row.id, name=row.name, text=row.text, course_id=row.course_id)
            for row in cur.fetchall()
        ]
# END reference solution
