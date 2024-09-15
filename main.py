from Process import *


session_user = None

def main_menu():
    def main_menu():
        global session_user
        if session_user:
            print("1.my todos")
            print("2.create todo")
            print("3.update todo")
            print("4.delete todo")
            print("5.edit todo title")
            print("6.log out")

        else:
            print("1.login")
            print("2.register")

        choice_ = input("Enter your choice: ")
