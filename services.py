from db import Database
from exceptions import BadRequestExceptions
from models import User
from password_manager import make_password, match_password


class AuthServices:
    def __init__(self):
        self.database = Database()
        super().__init__()

    def register_user(self, user:User):
        if self.database.check_username_unique(user.username):
            user.password = make_password(password=user.password)
            self.database.insert_user(**user.__dict__)
            print("""\n
            ╔════════════════════════════╗
            ║   Successfully completed   ║
            ╚════════════════════════════╝
            \n""")

        else:
            raise BadRequestExceptions(f"\n\t***USERNAME '{user.username}' ALREADY REGISTERED***\n")

    def login_user(self, username, password):
        data = self.database.get_user_by_username(username)

        if data is None:
            raise BadRequestExceptions("\n\t***USER NOT FOUND***\n")

        user = User(username=data[1], password=data[2], email=data[3], phone_number=data[4])
        user.id = data[0]

        if match_password(password=password, hashed_password=user.password):
            return user
        else:
            raise BadRequestExceptions("\n\t***PASSWORD IS NOT CORRECT***\n")


class ToDoServices:
    def __init__(self, user):
        self.user = user
        self.database = Database()

    def create_todo(self, title):
        self.database.insert_todo(title=title, status="todo", owner_id=self.user.id)

    def update_todo(self, title, todo_id):
        db_user_id = self.database.check_exists_todo_user(todo_id)

        if db_user_id is None:
            print("\n✦  Todo not found  ✦\n")
            return

        if self.user.id == db_user_id[0]:
            self.database.update_todo(title=title, todo_id=todo_id)
            print("""\n
            ╔════════════════════════════╗
            ║   Successfully completed   ║
            ╚════════════════════════════╝
            \n""")
        else:
            print("""\n
              ═══════════════════════════════      
            ✦  You can update only your todos  ✦
              ═══════════════════════════════
            \n""")

    def my_todos(self):
        data = self.database.my_todos(self.user.id)
        return data

    def delete_todo(self, todo_id):
        db_user_id = self.database.check_exists_todo_user(todo_id=todo_id)
        if self.user.id == db_user_id[0]:
            self.database.delete_todo(todo_id=todo_id)
            print("""\n
            ╔════════════════════════════╗
            ║   Successfully completed   ║
            ╚════════════════════════════╝
            \n""")
        else:
            print("""\n
              ═══════════════════════════════      
            ✦ You can delete only your todos  ✦
              ═══════════════════════════════
            \n""")
    def edit_todo_title(self, todo_id, title):
        db_user_id = self.database.check_exists_todo_user(todo_id=todo_id)
        if self.user.id == db_user_id[0]:
            self.database.edit_todo_title(title=title, todo_id=todo_id)
            print("""\n
            ╔════════════════════════════╗
            ║   Successfully completed   ║
            ╚════════════════════════════╝
                \n""")
        else:
            print("""\n
              ═══════════════════════════════      
            ✦ You can delete only your todos  ✦
              ═══════════════════════════════
                        \n""")
    


