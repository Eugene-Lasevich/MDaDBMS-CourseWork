import tkinter as tk
from tkinter import messagebox
from database import Database
from models.customers import Customer

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration")

        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack(pady=10)

        self.first_name_label = tk.Label(self.register_frame, text="First Name:")
        self.first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.first_name_entry = tk.Entry(self.register_frame)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.last_name_label = tk.Label(self.register_frame, text="Last Name:")
        self.last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.last_name_entry = tk.Entry(self.register_frame)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.phone_label = tk.Label(self.register_frame, text="Phone:")
        self.phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = tk.Entry(self.register_frame)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.register_frame, text="Password:")
        self.password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.register_frame, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register)
        self.register_button.grid(row=4, column=0, columnspan=2, pady=10)

    def register(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()

        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        Customer.insert_customer(cursor, first_name, last_name, phone, password)

        messagebox.showinfo("Success", "Registration successful!")

        conn.commit()
        conn.close()

        # Закрываем окно регистрации после успешной регистрации
        self.root.destroy()

def main():
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
