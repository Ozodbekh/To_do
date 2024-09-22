from datetime import datetime, timedelta
from os import getenv

from dotenv import load_dotenv

load_dotenv()

import psycopg2


class Database:
    def __init__(self):
        self.db = psycopg2.connect(
            host='127.0.0.1',
            dbname=getenv("DB_NAME"),
            password=getenv("DB_PASSWORD"),
            user=getenv("DB_USER")
        )
        self.db.autocommit = True
        self.cursor = self.db.cursor()

    def create_user_table(self):
        with self.db.cursor() as cursor:
            create_user_sql = """
                create table if not exists users(
                    id serial primary key,
                    username varchar(128) unique not null,
                    password varchar(128) not null,
                    email varchar(128) not null,
                    phone_number varchar(56) not null
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
                    deadline TIMESTAMP NOT NULL
                );
            """
            cursor.execute(create_todo_sql)

    def insert_user(self, username, password, email, phone_number):
        insert_user_sql = """
            INSERT INTO users(username, password, email, phone_number) VALUES(%s, %s, %s, %s);  
        """
        with self.db.cursor() as cursor:
            cursor.execute(insert_user_sql, (username, password, email, phone_number))

    def insert_todo(self, title, status, owner_id):

        deadline = datetime.now() + timedelta(days=1)

        insert_todo_sql = """
            insert into todo(title, status, owner_id, deadline) values(%s, %s, %s, %s);
        """
        with self.db.cursor() as cursor:
            cursor.execute(insert_todo_sql, (title, status, owner_id, deadline))

    def check_username_unique(self, username):
        search_username_unique_sql = """
            select * from users where username=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(search_username_unique_sql, (username,))
            result = cursor.fetchall()
            return not bool(result)

    def get_user_by_username(self, username):
        search_user_sql = """
            select * from users where username=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(search_user_sql, (username,))
            result = cursor.fetchone()
            return result

    def update_todo(self, title, todo_id):
        update_todo_sql = """
            update todo set title=%s where id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(update_todo_sql, (title, todo_id))

    def my_todos(self, user_id):
        my_todos_sql = """
            select * from todo where owner_id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(my_todos_sql, (user_id,))
            return cursor.fetchall()

    def edit_todo_title(self, title, todo_id):
        edit_todo_sql = """
                    UPDATE todo SET title=%s WHERE id=%s;
                """
        with self.db.cursor() as cursor:
            cursor.execute(edit_todo_sql, (title, todo_id))

    def delete_todo(self, todo_id):
        delete_todo_sql = """
            delete from todo where id=%s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(delete_todo_sql, (todo_id,))

    def check_exists_todo_user(self, todo_id):
        cursor = self.db.cursor()  # self.connection -> self.db
        check_exists_todo_user_sql = "SELECT owner_id FROM todo WHERE id = %s"
        cursor.execute(check_exists_todo_user_sql, (todo_id,))
        return cursor.fetchone()

# if __name__ == "__main__":
#     db = Database()
#     db.create_user_table()
#     db.create_todo_table()