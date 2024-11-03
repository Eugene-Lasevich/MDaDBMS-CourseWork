import tkinter as tk
from tkinter import messagebox
from database import Database
from models.customers import Customer

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.result = None  # Инициализируем атрибут для хранения результата

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=10)

        self.first_name_label = tk.Label(self.login_frame, text="First Name:")
        self.first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.first_name_entry = tk.Entry(self.login_frame)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.last_name_label = tk.Label(self.login_frame, text="Last Name:")
        self.last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.last_name_entry = tk.Entry(self.login_frame)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        password = self.password_entry.get()

        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        self.result = Customer.check_password(cursor, first_name, last_name, password)

        conn.close()

        if self.result:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid first name, last name, or password")

        self.root.destroy()  # Закрываем окно после получения результата

    def get_result(self):
        return self.result
