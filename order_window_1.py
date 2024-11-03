import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from models.pickup_points import PickupPoint
from models.orders import Orders
from models.goods import Goods
from models.suppliers import Supplier

class OrderWindow:
    def __init__(self, root, id_name):
        self.root = root
        self.root.title("Order Window")
        self.id_name= id_name
        self.current_price = None

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

        # Добавляем обработчики событий для обновления выпадающих списков
        self.product_var.trace_add("write", self.update_supplier_combobox)
        self.supplier_var.trace_add("write", self.update_product_combobox)
        self.product_var.trace_add("write", self.update_quantity_combobox)

        # Добавляем кнопку "Отмена"
        cancel_button = ttk.Button(self.main_frame, text="Cancel", command=self.cancel_selection)
        cancel_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

    def cancel_selection(self):
            # Сбрасываем выбранные значения
        self.product_var.set("")  # Сброс значения продукта
        self.supplier_var.set("")  # Сброс значения поставщика
        self.pickup_var.set("")  # Сброс значения пункта выдачи
        self.quantity_var.set("")  # Сброс значения количества

            # Заполняем выпадающие списки заново
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
        suppliers = Supplier.get_all_suppliers(cursor)
        conn.close()

        supplier_values = [supplier[1] for supplier in suppliers]

        self.supplier_combobox['values'] = supplier_values

    def populate_pickup_points(self):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()
        pickup_points = PickupPoint.get_all_pickup_points(cursor)
        conn.close()
        pickup_values = [(point[0], point[1]) for point in pickup_points]
        self.pickup_combobox['values'] = pickup_values

    def update_supplier_combobox(self, *args):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()
        selected_product = self.product_var.get()
        suppliers_for_product = Goods.get_all_suppliers_by_product_name(cursor, selected_product)
        self.supplier_combobox['values'] = suppliers_for_product

    def update_product_combobox(self, *args):
        pass

    def update_quantity_combobox(self, *args):
        # Получаем
        selected_product = self.product_var.get()

        available_quantities = self.get_available_quantities(selected_product)

        self.quantity_combobox['values'] = available_quantities

    def get_available_quantities(self, selected_product):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()
        print(selected_product, 'dfghjhghjhhjh')
        suppliers_for_product = Goods.get_quantity_price_goods_by_name(cursor, selected_product)
        print(suppliers_for_product, "dfg gbfbafdbadfv")
        self.current_price = suppliers_for_product[0][1]
        return list(range(1, suppliers_for_product[0][0]))

    def submit_order(self):
        product = self.product_var.get()
        supplier = self.supplier_var.get()
        pickup_point = self.pickup_combobox.get()[0]
        quantity = self.quantity_var.get()

        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

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
                      f"pickup point {pickup_point}., {self.current_price}")
                Orders.create_table(cursor)
                Orders.insert_order_by_name(cursor, pickup_point, product, supplier,self.id_name[0], self.current_price*quantity)
                # conn.commit()
                Goods.update_quantity_goods_by_name(cursor,product, quantity)
                conn.commit()
                for tmp in Orders.get_all_orders(cursor):
                    print(tmp)
                self.root.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.")

# Пример использования:
def open_order_window():
    root = tk.Toplevel()
    app = OrderWindow(root,1)

# Создание главного окна
# root = tk.Tk()
# root.title("Main Window")
#
# # Кнопка для открытия окна заказа
# order_button = ttk.Button(root, text="Order", command=open_order_window)
# order_button.pack(padx=20, pady=10)
#
# root.mainloop()
