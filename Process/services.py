from Process.db import Database


class AuthServices:
    def __init__(self):
        self.database = Database()
        super().__init__()

    def register_user(self):
        pass

    def login_user(self):
        pass


class ToDoServices:
    def __init__(self, user):
        self.user = user
        self.database = Database()

    def create_tod(self):
        pass

    def update_todo(self):
        pass

    def delete_todo(self):
        pass

    def edit_todo_title(self):
        pass

    


