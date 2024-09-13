from files import *
session_user = None

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
    if session_user:
        user_menu(choice_)
    else:
        auth_menu(choice_)

def auth_menu(choice_):
    global session_user
    auth_service = AuthService()
    try:
        match choice_:
            case "1":
                username = input("Username: ")
                password = input("Password: ")
                session_user = auth_service.login_user(username=username, password=password)
            case "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                phone = input("Enter phone: ")
                email = input("Enter email: ")
                auth_service.register_user(User(
                    username=username,
                    password=password,
                    email=email,
                    phone=phone
                    )
                )
                print("User successfully registered!!!")
    except BadRequestException as error:
        print(error.message)
    main_menu()


def user_menu(choice_):
    global session_user
    user_todo = TodoService(user=session_user)
    match choice_:
        case "1":
            todos = user_todo.my_todos()
            for todo in todos:
                print(" | ".join(list(map(str, todo))))

        case "2":
            title = input("Enter Todo title: ")
            user_todo.create_todo(title=title)

        case "3":
            todo_id = input("Enter Todo id: ")
            print("\tStatus\t")
            print("1. todo")
            print("2. process")
            print("3. done")
            s = input("Choose status: ")
            match s:
                case "1":
                    status = "todo"
                case "2":
                    status = "process"
                case "3":
                    status = "done"
            user_todo.update_todo(todo_id, value=status)

        case "4":
            todo_id = input("Enter Todo id: ")
            user_todo.delete_todo(todo_id=todo_id)

        case "5":
            todo_id = input("Enter Todo id: ")
            title = input("Enter title: ")
            user_todo.edit_todo_title(todo_id, title)

        case "6":
            session_user = None
            main_menu()
    main_menu()

if __name__ == "__main__":
    main_menu()