from db import Database
from exceptions import BadRequestExceptions
from models import User
from services import AuthServices, ToDoServices
from prettytable import PrettyTable

session_user = None

def main_menu():
    global session_user

    if session_user:
        print("═════════ Logged in Menu ═════════")
        print("║ 1. 🌟 My Todos                  ║")
        print("║ 2. ➕ Create Todo                ║")
        print("║ 3. ✏️  Update Todo              ║")
        print("║ 4. ❌ Delete Todo                ║")
        print("║ 5. 📝 Edit Todo Title           ║")
        print("║ 6. 🚪 Log out                   ║")
        print("══════════════════════════════════")
    else:
        print("═════════ Welcome ═════════")
        print("║ 1. 🔑 Login             ║")
        print("║ 2. 📝 Register          ║")
        print("═══════════════════════════")

    choice_ = input("Enter your choice: ")

    if session_user:
        user_menu(choice_)
    else:
        auth_menu(choice_)

def auth_menu(choice_):
    global session_user
    auth_service = AuthServices()
    try:
        match choice_:
            case "1":
                print("═════════ Login ═════════")
                username = input("Username: ")
                password = input("Password: ")
                session_user = auth_service.login_user(username=username, password=password)
                print(f"🟢 Successfully logged in as {username}!")
            case "2":
                print("═════════ Register ═════════")
                username = input("Enter username: ")
                password = input("Enter password: ")
                phone_number = input("Enter phone: ")
                email = input("Enter email: ")
                auth_service.register_user(User(
                    username=username,
                    password=password,
                    email=email,
                    phone_number=phone_number
                    )
                )
                print("✅ User successfully registered!!!")
    except BadRequestExceptions as error:
        print(f"❌ Error: {error.message}")
    main_menu()

def user_menu(choice_):
    global session_user
    user_todo = ToDoServices(user=session_user)
    match choice_:
        case "1":
            print("\n═════════ My Todos ═════════")
            todos = user_todo.my_todos()
            if todos:
                print("║ ID  | Title           | Status      | Deadline                 ║")
                print("══════════════════════════════════════════════════════════════")
                for todo in todos:
                    # Exclude owner ID (assumed to be the second item in the tuple)
                    todo_id, title, status, deadline = todo[0], todo[1], todo[2], todo[4]
                    print(f"║ {todo_id:<3} | {title:<15} | {status:<10} | {deadline} ║")
                print("══════════════════════════════════════════════════════════════")
            else:
                print("""
                ╔═════════════════════════════╗
                ║     You have no todos yet    ║
                ╚═════════════════════════════╝
                """)

        case "2":
            print("\n═════════ Create Todo ═════════")
            title = input("Enter Todo title: ")
            user_todo.create_todo(title=title)
            print(f"✅ Todo '{title}' created!")

        case "3":
            print("\n═════════ Update Todo ═════════")
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
            user_todo.update_todo(title=status, todo_id=todo_id)
            print(f"✅ Todo status updated to '{status}'!")

        case "4":
            print("\n═════════ Delete Todo ═════════")
            todo_id = input("Enter Todo id: ")
            user_todo.delete_todo(todo_id=todo_id)
            print(f"❌ Todo with ID {todo_id} deleted!")

        case "5":
            print("\n═════════ Edit Todo Title ═════════")
            todo_id = int(input("Enter Todo id: "))
            title = input("Enter new title: ")
            user_todo.edit_todo_title(todo_id, title)
            print(f"✏️  Todo title updated to '{title}'!")

        case "6":
            print("🚪 Logging out...")
            session_user = None
            print("\n")
            main_menu()

        case _:
            print("""
            ═════════════════════════════════
            ✦  Number not between 1 and 6  ✦
            ═════════════════════════════════
            """)

    print("\n")
    main_menu()

if __name__ == "__main__":
    db = Database()
    db.create_user_table()
    db.create_todo_table()
    main_menu()
