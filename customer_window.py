import tkinter as tk
from tools.user_window import UserWindow
from tools.customer_register import RegistrationApp
from tools.customer_login import LoginApp

class MainAppCustomer:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")

        self.register_button = tk.Button(self.root, text="Register", command=self.open_registration)
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", command=self.open_login)
        self.login_button.pack(pady=10)

    def open_registration(self):
        registration_window = tk.Toplevel(self.root)
        app = RegistrationApp(registration_window)

    def open_login(self):
        login_window = tk.Toplevel(self.root)
        app = LoginApp(login_window)
        self.root.wait_window(login_window)  # Ждем закрытия окна входа
        login_result = app.get_result()
        self.user_window = None
        if login_result:
            print(login_result)
            if not self.user_window:  # Если окно пользователя еще не было создано
                self.user_window = tk.Toplevel()  # Создаем окно пользователя
                user_app = UserWindow(self.user_window, (login_result[0], login_result[1]))  # Передаем его в окно пользователя
        else:
            print("Invalid name or password")


def run_main():
    root = tk.Tk()
    app = MainAppCustomer(root)
    root.mainloop()

if __name__ == "__main__":
    run_main()
