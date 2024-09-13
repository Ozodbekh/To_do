import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.db = psycopg2.connect(
            host='127.0.0.1',
            dbname=getenv("DB_NAME"),
            password=getenv("DB_PASSWORD"),
            user=getenv("DB_USER")
        )
        self.db.autocommit = True

    def create_user_table(self):
        with self.db.cursor() as cursor:
            create_user_sql = """
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(128) UNIQUE NOT NULL,
                    password VARCHAR(128) NOT NULL,
                    email VARCHAR(56),
                    phone VARCHAR(56)
                );
            """
            cursor.execute(create_user_sql)

    def create_todo_table(self):
        with self.db.cursor() as cursor:
            create_todo_sql = """
                CREATE TABLE IF NOT EXISTS todo(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(128) UNIQUE NOT NULL,
                    status VARCHAR(128) NOT NULL,
                    owner_id INT REFERENCES users(id),
                    deadline TIMESTAMP DEFAULT NOW() + INTERVAL '1 day'
                );
            """
            cursor.execute(create_todo_sql)

    def insert_user(self, username, password, email, phone):
        insert_user_sql = """
            INSERT INTO users(username, password, email, phone) VALUES (%s, %s, %s, %s);
        """
        with self.db.cursor() as cursor:
            cursor.execute(insert_user_sql, (username, password, email, phone))

    def insert_todo(self, title, status, owner_id):
        insert_todo_sql = """
            INSERT INTO todo(title, status, owner_id) VALUES (%s, %s, %s);
        """
        with self.db.cursor() as cursor:
            cursor.execute(insert_todo_sql, (title, status, owner_id))

    def check_username_unique(self, username):
        search_username_unique_sql = """
            SELECT * FROM users WHERE username=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(search_username_unique_sql, (username,))
            result = cursor.fetchall()
            return not bool(result)

    def get_user_by_username(self, username):
        search_user_sql = """
            SELECT * FROM users WHERE username=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(search_user_sql, (username,))
            return cursor.fetchone()

    def update_todo(self, value, todo_id):
        update_todo_sql = """
            UPDATE todo SET title=%s WHERE id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(update_todo_sql, (value, todo_id))

    def my_todos(self, user_id):
        my_todo_sql = """
            SELECT * FROM todo WHERE owner_id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(my_todo_sql, (user_id,))
            return cursor.fetchall()

    def edit_todo_title(self, title, todo_id):
        edit_todo_sql = """
            UPDATE todo SET title=%s WHERE id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(edit_todo_sql, (title, todo_id))

    def delete_todo(self, todo_id):
        delete_todo_sql = """
            DELETE FROM todo WHERE id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(delete_todo_sql, (todo_id,))

    def check_exists_todo_user(self, todo_id):
        check_exists_todo_user_sql = """
            SELECT owner_id FROM todo WHERE id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(check_exists_todo_user_sql, (todo_id,))
            return cursor.fetchone()


if __name__ == "__main__":
    db = Database()
    db.create_user_table()
    db.create_todo_table()
