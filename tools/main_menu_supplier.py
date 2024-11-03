import tkinter as tk
from models.transport import Transport
from models.warehouses import Warehouses
from models.goods import Goods
from models.orders import Orders
from database import Database
from tkinter import ttk, messagebox




class MainMenu:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.parent.title("Main Menu")

        self.last_button_pressed = None
        self.current_table = None
        self.user_id = user_id
        self.selected_row = None

        # Фрейм для кнопок слева
        self.buttons_frame = tk.Frame(self.parent)
        self.buttons_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        # Кнопки
        self.warehouse_button = tk.Button(self.buttons_frame, text="My Warehouses", command=self.open_warehouses)
        self.warehouse_button.pack(side="top", pady=10, fill="x")

        self.products_button = tk.Button(self.buttons_frame, text="My Products", command=self.open_products)
        self.products_button.pack(side="top", pady=10, fill="x")

        self.transport_button = tk.Button(self.buttons_frame, text="My Transport", command=self.open_transport)
        self.transport_button.pack(side="top", pady=10, fill="x")

        self.orders_button = tk.Button(self.buttons_frame, text="Orders", command=self.open_orders)
        self.orders_button.pack(side="top", pady=10, fill="x")

        # Фрейм для экрана справа
        self.screen_frame = tk.Frame(self.parent)
        self.screen_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def create_entity_buttons(self, parent):
        # Кнопки
        create_button = tk.Button(parent, text="Create", command=self.create_row)
        create_button.pack(side="left", padx=5)

        update_button = tk.Button(parent, text="Update", command=self.update_row)
        update_button.pack(side="left", padx=5)

        delete_button = tk.Button(parent, text="Delete", command=self.delete_row)
        delete_button.pack(side="left", padx=5)

        confirm_button = tk.Button(parent, text="Confirm", command=self.confirm_changes)
        confirm_button.pack(side="left", padx=5)

        cancel_button = tk.Button(parent, text="Cancel", command=self.cancel_changes)
        cancel_button.pack(side="left", padx=5)

        self.all_buttons = [create_button, update_button, delete_button, confirm_button, cancel_button]

    def create_table_and_buttons(self, headers):
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()
        # Проверяем существует ли уже таблица, и если да, удаляем ее
        if hasattr(self, "tree") and self.tree is not None:
            self.tree.destroy()

        # Перебираем все кнопки и удаляем их
        if hasattr(self, "all_buttons"):
            for button in self.all_buttons:
                button.destroy()

        # Перебираем все элементы ввода и удаляем их
        if hasattr(self, "input_entries"):
            for entry in self.input_entries:
                entry.destroy()

        # Перебираем все фреймы таблицы и удаляем их
        if hasattr(self, "all_table_frames"):
            for frame in self.all_table_frames:
                frame.destroy()

        self.all_table_frames = []
        # Создаем фрейм для таблицы
        table_frame = tk.Frame(self.screen_frame)
        table_frame.pack(fill="both", expand=True)
        self.all_table_frames.append(table_frame)

        # Создаем таблицу и сохраняем ссылку на нее
        self.tree = ttk.Treeview(table_frame, show="headings")
        self.tree["columns"] = list(range(len(headers)))
        for i, header in enumerate(headers):
            self.tree.heading(i, text=header)
            self.tree.column(i, width=100)
        self.tree.pack(expand=True, fill="both")

        if self.current_table == Transport:
            for row in self.current_table.get_all_transport_of_user(cursor, self.user_id):
                self.tree.insert("", "end", values=row[1::])
        if self.current_table == Warehouses:
            for row in self.current_table.get_all_warehouses_of_user(cursor, self.user_id):
                self.tree.insert("", "end", values=row[1::])
        if self.current_table == Goods:
            for row in self.current_table.get_goods_with_warehouses(cursor, self.user_id):
                self.tree.insert("", "end", values=row[1::])
        if self.current_table == Orders:
            for row in self.current_table.join_orders_1(cursor):
                self.tree.insert("", "end", values=row)

        # Создаем фрейм для элементов ввода
        entry_frame = tk.Frame(table_frame)
        entry_frame.pack(fill="both", expand=True)
        self.all_table_frames.append(entry_frame)

        # Создаем кнопки для сущности
        self.create_entity_buttons(entry_frame)

        self.input_entries = []
        for i in range(len(headers)):
            entry = tk.Entry(entry_frame, width=15)  # Создаем элемент ввода
            entry.pack(side="left", padx=5, pady=5)  # Размещаем элемент ввода в таблице
            self.input_entries.append(entry)
        # conn.commit()
        conn.close()

    def create_row(self):
        # Получаем текст из всех элементов ввода
        for button in self.all_buttons:
            if button["text"] not in ["Confirm", "Cancel"]:
                button.configure(state="disabled")
        self.last_button_pressed = "create"

    def update_row(self):
        selected_item = self.tree.selection()

        if selected_item:
            self.selected_row = selected_item  # Сохраняем выделенную строку

            values = self.tree.item(selected_item, "values")

            for entry, value in zip(self.input_entries, values):
                entry.delete(0, "end")
                entry.insert(0, value)

            for button in self.all_buttons:
                if button["text"] not in ["Confirm", "Cancel"]:
                    button.configure(state="disabled")

            self.last_button_pressed = "update"
        else:
            messagebox.showerror("Error", "Please select a row to update.")

    def delete_row(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row = selected_item
            for button in self.all_buttons:
                if button["text"] not in ["Confirm", "Cancel"]:
                    button.configure(state="disabled")
            # Сохраняем выделенную строку

        self.last_button_pressed = "delete"

    def confirm_changes(self):
        for entry in self.input_entries:
            if not entry.get() and (self.last_button_pressed != 'delete' and self.last_button_pressed=="orders"):
                messagebox.showerror("Error", "Please fill in all fields before confirming changes")
                return

        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        if self.last_button_pressed == 'create':
            new_values = [entry.get() for entry in self.input_entries]
            self.tree.insert("", "end", values=new_values)
            if self.current_table == Transport:
                Transport.insert_transport(cursor, *new_values, self.user_id)
                conn.commit()
            if self.current_table == Warehouses:
                Warehouses.insert_warehouse(cursor, *new_values, self.user_id)
                conn.commit()
            if self.current_table == Goods:
                Goods.insert_goods(cursor, *new_values, self.user_id)
                conn.commit()



        elif self.last_button_pressed == 'update':

            if self.selected_row:

                updated_values = [entry.get() for entry in self.input_entries]
                selected_item = self.tree.selection()

                if selected_item:
                    value_of_current_row = self.tree.item(self.selected_row, "values")
                    print(value_of_current_row)
                    old_type = value_of_current_row
                    print(*old_type, *updated_values)
                    if self.current_table == Transport:
                        Transport.update_transport(cursor, *old_type, *updated_values, self.user_id)
                        conn.commit()
                    if self.current_table == Warehouses:
                        Warehouses.update_warehouse(cursor, *old_type, *updated_values, self.user_id)
                        conn.commit()
                    if self.current_table == Goods:
                        Goods.update_goods(cursor, *old_type, *updated_values, self.user_id)
                        conn.commit()
                    if self.current_table == Orders:
                        print(old_type[0], updated_values[3])
                        Orders.update_order(cursor, old_type[0], updated_values[3])
                        conn.commit()



                    self.tree.item(selected_item, values=updated_values)

            else:

                messagebox.showerror("Error", "Please select a row to update.")

        elif self.last_button_pressed == 'delete':
            if self.selected_row:

                delete_values = [entry.get() for entry in self.input_entries]
                selected_item = self.tree.selection()

                if selected_item:
                    value_of_current_row = self.tree.item(self.selected_row, "values")
                    old_type = value_of_current_row  # Получаем старый тип из текущей строки
                    if self.current_table == Transport:
                        Transport.delete_transport(cursor, *old_type, self.user_id)
                        conn.commit()
                    if self.current_table == Warehouses:
                        Warehouses.delete_warehouse(cursor, *old_type, self.user_id)
                        conn.commit()
                    if self.current_table == Goods:
                        Goods.delete_goods(cursor, *old_type, self.user_id)
                        conn.commit()



                    self.tree.delete(selected_item)

            else:

                messagebox.showerror("Error", "Please select a row to delete.")


        # Разблокируем все кнопки
        for button in self.all_buttons:
            button.config(state="normal")

        # Сбрасываем информацию о последней нажатой кнопке
        self.last_button_pressed = None

    def cancel_changes(self):
        self.create_table_and_buttons(self.headers)
        self.last_button_pressed = None

    def open_warehouses(self):
        print(self.user_id)
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        Warehouses.create_table(cursor)
        conn.commit()
        self.current_table = Warehouses
        self.headers = Warehouses.get_column_names(cursor)
        if "id" in self.headers:
            self.headers.remove("id")
        self.create_table_and_buttons(self.headers)
        conn.close()

    def open_products(self):
        print(self.user_id)
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        Goods.create_table(cursor)
        conn.commit()
        self.current_table = Goods
        self.headers = Goods.get_goods_with_warehouses_column_names()
        if "id" in self.headers:
            self.headers.remove("id")
        self.create_table_and_buttons(self.headers)
        conn.close()

    def open_transport(self):
        print(self.user_id)
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()

        Transport.create_table(cursor)
        conn.commit()
        self.current_table = Transport
        self.headers = Transport.get_column_names(cursor)
        if "id" in self.headers:
            self.headers.remove("id")
        self.create_table_and_buttons(self.headers)
        conn.close()

    def open_orders(self):

        print(self.user_id)
        db = Database('example.db')
        conn = db.connect()
        cursor = conn.cursor()
        self.last_button_pressed="orders"

        Orders.create_table(cursor)
        conn.commit()
        self.current_table = Orders
        self.headers = Orders.get_orders_with_column_names_1()
        self.create_table_and_buttons(self.headers)
        for button in self.all_buttons:
            if button["text"] not in ["Confirm", "Cancel", "Update"]:
                button.configure(state="disabled")
        count =0
        for entry in self.input_entries:
            if count == 3:
                count += 1
                continue
            else:
                entry.configure(state="disabled")
            count+=1
        conn.close()


def show_main_menu():
    root = tk.Toplevel()
    app = MainMenu(root)

# Пример использования
