import tkinter as tk
from tkinter import ttk
from tools.review_window import ReviewWindow
from models.goods import Goods
from models.suppliers import Supplier
from models.orders import Orders
from database import Database
from order_window_1 import OrderWindow

class UserWindow:
    def __init__(self, root, id_name):
        self.root = root
        self.root.title("User Window")
        self.current_table = None
        self.tree = None  # Initialize self.tree attribute
        self.id_name = id_name
        print(self.id_name)

        # Frame for buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side="left", padx=20, pady=10)

        # Create order button
        create_order_button = ttk.Button(button_frame, text="Create Order", command=self.create_order)
        create_order_button.grid(row=0, column=0, padx=10, pady=5)

        # My orders button
        my_orders_button = ttk.Button(button_frame, text="My Orders", command=self.my_orders)
        my_orders_button.grid(row=1, column=0, padx=10, pady=5)

        # Leave feedback button
        leave_feedback_button = ttk.Button(button_frame, text="Leave Feedback", command=self.leave_feedback)
        leave_feedback_button.grid(row=2, column=0, padx=10, pady=5)

        # Detailed information button
        detailed_info_button = ttk.Button(button_frame, text="Detailed Info", command=self.show_detailed_info)
        detailed_info_button.grid(row=3, column=0, padx=10, pady=5)

        # View products button
        view_products_button = ttk.Button(button_frame, text="View Products", command=self.view_products)
        view_products_button.grid(row=4, column=0, padx=10, pady=5)

        # Dropdown for suppliers
        self.selected_supplier = tk.StringVar()
        self.supplier_dropdown = ttk.Combobox(button_frame, textvariable=self.selected_supplier)
        self.supplier_dropdown.grid(row=5, column=0, padx=10, pady=5)

        # Frame for table
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(side="right", padx=20, pady=10)

        # Fill supplier dropdown
        self.fill_supplier_dropdown()

    def fill_supplier_dropdown(self):
        db = Database('example.db')
        conn = db.connect()
        self.suppliers = ["All"]
        cursor = conn.cursor()
        for row in Supplier.get_all_suppliers_names(cursor):
            self.suppliers.append(row)

        self.supplier_dropdown['values'] = self.suppliers
        self.supplier_dropdown.current(0)  # Set default value

    def create_order(self):
        print("Create Order button clicked")
        # Создаем новое окно для заказа
        order_window = tk.Toplevel(self.root)
        # Инициализируем OrderWindow
        order_app = OrderWindow(order_window,self.id_name)

    def my_orders(self):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()
        self.create_table(Orders.get_orders_with_column_names())
        for row in Orders.join_orders(cursor):
            self.tree.insert("", "end", values=row)
        print("My Orders button clicked")

    def leave_feedback(self):
        print("Leave Feedback button clicked")
        self.review_window = None
        if not self.review_window:  # Если окно отзывов еще не было создано
            self.review_window = tk.Toplevel()  # Создаем окно отзывов
            review_app = ReviewWindow(self.review_window, self.id_name)  # Передаем id_name в окно отзывов

    def show_detailed_info(self):
        selected_item = self.tree.selection()
        values = self.tree.item(selected_item, "values")
        good_name = values[0]
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()
        self.create_table(Goods.get_goods_with_reviews_column_names())
        for row in Goods.get_goods_with_reviews(cursor, good_name):
            self.tree.insert("", "end", values=row[1::])

        if selected_item:
            # Retrieve the values of the selected row
            values = self.tree.item(selected_item, "values")
            print("Detailed Info button clicked")
            print("Selected row values:", values)
        else:
            print("No row selected")

    def view_products(self):
        selected_supplier = self.selected_supplier.get()
        print(f"View Products button clicked. Selected supplier: {selected_supplier}")
        columns = ("Name", "Price", "Quantity", "Description")
        self.create_table(columns)

        if selected_supplier == "All":
            db = Database('example.db')
            conn = db.connect()
            cursor = conn.cursor()
            for row in Goods.get_all_goods(cursor):
                self.tree.insert("", "end", values=row[1::])
            conn.close()
        else:
            db = Database('example.db')
            conn = db.connect()
            cursor = conn.cursor()
            print(selected_supplier)
            for row in Goods.get_all_goods_of_user_by_name(cursor, selected_supplier):
                print(row)
                self.tree.insert("", "end", values=row[1::])
            conn.close()

    def create_table(self, columns):
        if hasattr(self, "tree") and self.tree is not None:
            self.tree.destroy()

        self.tree = ttk.Treeview(self.table_frame, columns=columns)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Устанавливаем ширину колонок
        self.tree.pack(expand=True, fill="both")
        self.tree.column("#0", width=0, stretch=tk.NO)


if __name__ == "__main__":
    root = tk.Tk()
    app = UserWindow(root)
    root.mainloop()
