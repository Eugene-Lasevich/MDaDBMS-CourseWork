import tkinter as tk
from tools.supplier_register import RegistrationApp
from tools.supplier_login import LoginApp
from tools.main_menu_supplier import MainMenu  # Предположим, что у нас есть отдельный файл для главного меню

class MainAppSupplier:
    def __init__(self, root):
        self.root = root
        self.root.title("Supplier Main Menu")

        self.register_button = tk.Button(self.root, text="Register", command=self.open_registration)
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", command=self.open_login)
        self.login_button.pack(pady=10)

        self.main_menu = None  # Инициализируем главное меню как пустое окно

    def open_registration(self):
        registration_window = tk.Toplevel(self.root)
        app = RegistrationApp(registration_window)

    def open_login(self):
        login_window = tk.Toplevel(self.root)
        app = LoginApp(login_window)
        self.root.wait_window(login_window)  # Ждем закрытия окна входа
        login_result = app.get_result()  # Получаем результат входа
        if login_result:
            self.main_menu = None
            if not self.main_menu:  # Если главное меню еще не было создано
                self.main_menu = tk.Toplevel()  # Создаем главное меню
                menu_app = MainMenu(self.main_menu, login_result)  # Передаем его в главное меню

        else:
            print("Invalid name or password")

def run_main():
    root = tk.Tk()
    app = MainAppSupplier(root)
    root.mainloop()

if __name__ == "__main__":
    run_main()
