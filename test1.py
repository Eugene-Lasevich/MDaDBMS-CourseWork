import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from models.pickup_points import PickupPoint
from models.orders import Orders
from models.goods import Goods
from models.suppliers import Supplier

class OrderWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Window")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=10)

        # Label and Dropdown for Product
        product_label = ttk.Label(self.main_frame, text="Product:")
        product_label.grid(row=0, column=0, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_combobox = ttk.Combobox(self.main_frame, textvariable=self.product_var, state="readonly")
        self.product_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Label and Dropdown for Supplier
        supplier_label = ttk.Label(self.main_frame, text="Supplier:")
        supplier_label.grid(row=1, column=0, padx=5, pady=5)
        self.supplier_var = tk.StringVar()
        self.supplier_combobox = ttk.Combobox(self.main_frame, textvariable=self.supplier_var, state="readonly")
        self.supplier_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Label and Dropdown for Pickup Points
        pickup_label = ttk.Label(self.main_frame, text="Pickup Point:")
        pickup_label.grid(row=2, column=0, padx=5, pady=5)
        self.pickup_var = tk.StringVar()
        self.pickup_combobox = ttk.Combobox(self.main_frame, textvariable=self.pickup_var, state="readonly")
        self.pickup_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Label and Dropdown for Quantity
        quantity_label = ttk.Label(self.main_frame, text="Quantity:")
        quantity_label.grid(row=3, column=0, padx=5, pady=5)
        self.quantity_var = tk.StringVar()
        self.quantity_combobox = ttk.Combobox(self.main_frame, textvariable=self.quantity_var, state="readonly")
        self.quantity_combobox['values'] = [1, 2, 3, 4, 5]  # Пример значений, вы можете настроить их по вашему усмотрению
        self.quantity_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Submit Button
        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.submit_order)
        submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Заполняем выпадающие списки значениями из базы данных
        self.populate_product_combobox()
        self.populate_supplier_combobox()
        self.populate_pickup_points()

    def populate_product_combobox(self):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        products = Goods.get_all_goods(cursor)
        print(products)
        conn.close()

        product_values = [product[1] for product in products]
        self.product_combobox['values'] = product_values

    def populate_supplier_combobox(self):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        # Получаем список поставщиков из базы данных
        suppliers = Supplier.get_all_suppliers(cursor)
        print(suppliers)

        # Закрываем соединение с базой данных
        conn.close()

        # Создаем список значений для выпадающего списка поставщиков
        supplier_values = [supplier[1] for supplier in suppliers]

        # Устанавливаем значения для выпадающего списка поставщиков
        self.supplier_combobox['values'] = supplier_values

    def populate_pickup_points(self):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        # Получаем список пунктов выдачи из базы данных
        pickup_points = PickupPoint.get_all_pickup_points(cursor)

        # Закрываем соединение с базой данных
        conn.close()

        # Создаем список значений для выпадающего списка пунктов выдачи
        pickup_values = [(point[1], point[2]) for point in pickup_points]

        # Устанавливаем значения для выпадающего списка пунктов выдачи
        self.pickup_combobox['values'] = pickup_values

    def submit_order(self):
        product = self.product_var.get()
        supplier = self.supplier_var.get()
        pickup_point = self.pickup_var.get()
        quantity = self.quantity_entry.get()

        try:
            quantity = int(quantity)

            if not product:
                messagebox.showwarning("Warning", "Please select a product.")
            elif not supplier:
                messagebox.showwarning("Warning", "Please select a supplier.")
            elif not pickup_point:
                messagebox.showwarning("Warning", "Please select a pickup point.")
            elif quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be greater than zero.")
            else:
                # Placeholder for order submission
                print(f"Order submitted successfully for {quantity} units of {product}, from supplier {supplier}, "
                      f"pickup point {pickup_point}.")
                self.root.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.")

# Пример использования:
def open_order_window():
    root = tk.Toplevel()
    app = OrderWindow(root)

# Создание главного окна
root = tk.Tk()
root.title("Main Window")

# Кнопка для открытия окна заказа
order_button = ttk.Button(root, text="Order", command=open_order_window)
order_button.pack(padx=20, pady=10)

root.mainloop()
