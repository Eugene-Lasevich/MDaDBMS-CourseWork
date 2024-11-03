class Goods:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS goods
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          price REAL,
                          quantity INTEGER,
                          description TEXT,
                          warehouse_id INTEGER,
                          supplier_id INTEGER,
                          FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
                          FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id))''')

    @staticmethod
    def insert_goods(cursor, name, price, quantity, description, warehouse_name, supplier_id):
        # Получаем идентификатор склада по его имени
        cursor.execute("SELECT id FROM warehouses WHERE name=?", (warehouse_name,))
        warehouse_row = cursor.fetchone()
        if warehouse_row:
            warehouse_id = warehouse_row[0]  # Получаем идентификатор склада
            # Вставляем запись о товаре, указывая идентификатор склада
            cursor.execute(
                "INSERT INTO goods (name, price, quantity, description, warehouse_id, supplier_id) VALUES (?, ?, ?, ?, ?, ?)",
                (name, price, quantity, description, warehouse_id, supplier_id))
        else:
            print(f"No warehouse found with name '{warehouse_name}'.")

    @staticmethod
    def get_all_goods(cursor):
        cursor.execute("SELECT id, name, price, quantity, description FROM goods")
        return cursor.fetchall()

    @staticmethod
    def get_all_goods_1(cursor):
        cursor.execute("SELECT id, name, price, quantity, description FROM goods")
        return cursor.fetchall()

    @staticmethod
    def get_all_suppliers_by_product_name(cursor, name):
        cursor.execute("""
                       SELECT name
                       FROM suppliers 
                       WHERE supplier_id = (SELECT supplier_id FROM goods WHERE name = ?)
                   """, (name,))
        return cursor.fetchall()

    @staticmethod
    def get_column_names(cursor):
        cursor.execute("PRAGMA table_info(goods)")
        return [column[1] for column in cursor.fetchall() if column[1] not in ('warehouse_id', 'supplier_id')]

    @staticmethod
    def drop_table(cursor):
        cursor.execute("DROP TABLE IF EXISTS goods")

    @staticmethod
    def get_all_goods_of_user(cursor, supplier_id):
        cursor.execute("SELECT id, name, price, quantity, description FROM goods WHERE supplier_id=?", (supplier_id,))
        return cursor.fetchall()

    @staticmethod
    def update_goods(cursor, old_name, old_price, old_quantity, old_description, old_warehouse_name, new_name,
                     new_price, new_quantity,
                     new_description, new_warehouse_name, supplier_id):
        # Получаем новый идентификатор склада по его имени
        cursor.execute("SELECT id FROM warehouses WHERE name=?", (new_warehouse_name,))
        new_warehouse_row = cursor.fetchone()
        if new_warehouse_row:
            new_warehouse_id = new_warehouse_row[0]  # Получаем идентификатор нового склада
        else:
            print(f"No warehouse found with name '{new_warehouse_name}'.")
            return

        cursor.execute(
            "UPDATE goods SET name=?, price=?, quantity=?, description=?, warehouse_id=? WHERE name=? AND price=? AND quantity=? AND description=? AND supplier_id=?",
            (new_name, new_price, new_quantity, new_description, new_warehouse_id, old_name, old_price, old_quantity,
             old_description, supplier_id))

    @staticmethod
    def delete_goods(cursor, name, price, quantity, description, warehouse_name, supplier_id):
        # Получаем идентификатор склада по его имени
        cursor.execute("SELECT id FROM warehouses WHERE name=?", (warehouse_name,))
        warehouse_row = cursor.fetchone()
        if warehouse_row:
            warehouse_id = warehouse_row[0]  # Получаем идентификатор склада
        else:
            print(f"No warehouse found with name '{warehouse_name}'.")
            return

        # Удаляем товар из таблицы goods, используя имя склада и остальные параметры
        cursor.execute(
            "DELETE FROM goods WHERE name=? AND price=? AND quantity=? AND description=? AND warehouse_id=? AND supplier_id=?",
            (name, price, quantity, description, warehouse_id, supplier_id))

    @staticmethod
    def get_goods_with_warehouses(cursor, supplier_id):
        cursor.execute(
            "SELECT goods.id, goods.name, goods.price, goods.quantity, goods.description, "
            "warehouses.name AS warehouse_name FROM goods "
            "JOIN warehouses ON goods.warehouse_id = warehouses.id "
            "WHERE goods.supplier_id=?", (supplier_id,))
        return cursor.fetchall()

    @staticmethod
    def get_goods_with_warehouses_column_names():
        return ["name", "price", "quantity", "description", "warehouse_name"]

    @staticmethod
    def get_all_goods_of_user_by_name(cursor, supplier_name):
        cursor.execute("""
                SELECT id, name, price, quantity, description 
                FROM goods 
                WHERE supplier_id = (SELECT supplier_id FROM suppliers WHERE name = ?)
            """, (supplier_name,))
        tmp = cursor.fetchall()
        print(tmp)
        print('8' * 60)
        return tmp

    @staticmethod
    def get_goods_with_reviews(cursor, name):
        cursor.execute(
            "SELECT goods.id, goods.name AS good_name, goods.price, goods.quantity, goods.description, "
            "COALESCE(reviews.text, '-') AS review_text, COALESCE(reviews.rating, '-') AS review_rating, "
            "suppliers.name AS supplier_name, suppliers.phone AS supplier_phone, suppliers.email AS supplier_email "
            "FROM goods "
            "LEFT JOIN reviews ON goods.id = reviews.good_id "
            "LEFT JOIN suppliers ON goods.supplier_id = suppliers.supplier_id "
            "WHERE goods.name=?", (name,))
        return cursor.fetchall()

    @staticmethod
    def get_goods_with_reviews_column_names():
        return ["name", "price", "quantity", "description", "review_text", "review_rating",
                "supplier_name", "supplier_phone", "supplier_email"]

    @staticmethod
    def get_all_goods_of_supplier(cursor, supplier_name):
        cursor.execute(
            "SELECT g.name FROM goods AS g JOIN suppliers AS s ON g.supplier_id = s.supplier_id WHERE s.name=?",
            (supplier_name,))
        return cursor.fetchall()

    @staticmethod
    def get_quantity_price_goods_by_name(cursor, name):
        cursor.execute("SELECT quantity, price FROM goods WHERE name=?", (name, ))
        return cursor.fetchall()

    @staticmethod
    def update_quantity_goods_by_name(cursor, name, quantity_to_subtract):
        # Получаем текущее количество товара по его имени
        cursor.execute("SELECT quantity FROM goods WHERE name=?", (name,))
        result = cursor.fetchone()

        if result:
            current_quantity = result[0]
            # Проверяем, достаточно ли товара на складе
            if current_quantity >= quantity_to_subtract:
                # Рассчитываем новое количество товара
                new_quantity = current_quantity - quantity_to_subtract
                # Обновляем количество товара в базе данных
                cursor.execute("UPDATE goods SET quantity=? WHERE name=?", (new_quantity, name))
                print(f"Quantity of {name} updated successfully.")
            else:
                print(f"Not enough {name} in stock.")
        else:
            print(f"No {name} found in the database.")



