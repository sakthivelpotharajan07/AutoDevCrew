class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class LoginPage:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists.")
        else:
            self.users[username] = User(username, password)
            print("User registered successfully.")

    def login_user(self, username, password):
        if username in self.users:
            if self.users[username].password == password:
                print("Login successful.")
                return True
            else:
                print("Invalid password.")
        else:
            print("Username does not exist.")
        return False

def main():
    login_page = LoginPage()
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_page.register_user(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_page.login_user(username, password)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()