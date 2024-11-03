import tkinter as tk
from tkinter import messagebox
from database import Database
from models.suppliers import Supplier

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Supplier Login")
        self.result = None  # Инициализируем атрибут для хранения результата

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=10)

        self.name_label = tk.Label(self.login_frame, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(self.login_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.name_entry.insert(0, "1")  # Задаем значение по умолчанию

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry.insert(0, "1")  # Задаем значение по умолчанию

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        name = self.name_entry.get()
        password = self.password_entry.get()

        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        self.result = Supplier.check_password(cursor, name, password)

        conn.close()

        if self.result:
            pass
            # messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid name or password")

        self.root.destroy()  # Закрываем окно после получения результата

    def get_result(self):
        return self.result
