from os import getenv

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

    def insert_user(self):
        pass

    def insert_todo(self):
        pass

    def check_username_unique(self):
        pass

    def get_user_by_username(self):
        pass

    def update_todo(self):
        pass

    def my_todos(self):
        pass

    def edit_todo_title(self):
        pass

    def delete_todo(self):
        pass

    def check_exists_todo_user(self):
        pass


if __name__ == '__main__':
    db = Database()
    db.create_user_table()
    db.create_todo_table()


