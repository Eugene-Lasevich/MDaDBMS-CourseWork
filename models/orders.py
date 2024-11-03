class Orders:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              pickuppoint_id INTEGER,
                              good_id INTEGER,
                              customer_id INTEGER,
                              status TEXT,
                              total_cost REAL,
                              supplier_id INTEGER,
                              FOREIGN KEY(pickuppoint_id) REFERENCES pickup_points(id),
                              FOREIGN KEY(good_id) REFERENCES goods(id),
                              FOREIGN KEY(customer_id) REFERENCES customers(id),
                              FOREIGN KEY(supplier_id) REFERENCES suppliers(id))''')

    @staticmethod
    def insert_order(cursor, pickuppoint_id, good_id, customer_id, supplier_id):
        cursor.execute(
            "INSERT INTO orders (pickuppoint_id, good_id, customer_id, supplier_id, status) VALUES (?, ?, ?, ?, ?)",
            (pickuppoint_id, good_id, customer_id, supplier_id, "Отправлен на обработку",))


    @staticmethod
    def get_all_orders(cursor):
        cursor.execute("SELECT id, pickuppoint_id, good_id, status, total_cost FROM orders")
        return cursor.fetchall()

    @staticmethod
    def get_column_names(cursor):
        cursor.execute("PRAGMA table_info(orders)")
        return [column[1] for column in cursor.fetchall() if column[1] not in ['pickuppoint_id', 'good_id', 'supplier_id']]

    @staticmethod
    def drop_table(cursor):
        cursor.execute("DROP TABLE IF EXISTS orders")

    @staticmethod
    def get_orders_of_pickuppoint(cursor, pickuppoint_id):
        cursor.execute("SELECT id, good_id, status, total_cost FROM orders WHERE pickuppoint_id=?", (pickuppoint_id,))
        return cursor.fetchall()

    @staticmethod
    def update_order(cursor, order_id, new_status):
        cursor.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))

    @staticmethod
    def delete_order(cursor, order_id):
        cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))

    @staticmethod
    def insert_order_by_name(cursor, pickuppoint_id, good_name, supplier_name, user_id, total_cost):
        cursor.execute("SELECT id FROM goods WHERE name=?", (good_name,))
        good_result = cursor.fetchone()
        if good_result:
            good_id = good_result[0]
            cursor.execute("SELECT supplier_id FROM suppliers WHERE name=?", (supplier_name,))
            supplier_result = cursor.fetchone()
            if supplier_result:
                supplier_id = supplier_result[0]
                cursor.execute("INSERT INTO orders (pickuppoint_id, good_id, supplier_id, status, customer_id, total_cost) VALUES (?, ?, ?, ?, ?, ?)",
                               (pickuppoint_id, good_id, supplier_id, "Отправлен на обработку", user_id, total_cost))
            else:
                print("The specified Supplier Name does not exist.")
        else:
            print("The specified Good Name does not exist.")

    @staticmethod
    def join_orders(cursor):
        cursor.execute('''
                SELECT orders.id, goods.name,orders.total_cost, orders.status, pickup_points.name AS pickup_point_name, 
                pickup_points.address, suppliers.name AS supplier_name, suppliers.phone 
                FROM orders
                LEFT JOIN pickup_points ON orders.pickuppoint_id = pickup_points.id
                LEFT JOIN goods ON orders.good_id = goods.id
                LEFT JOIN suppliers ON orders.supplier_id = suppliers.supplier_id
            ''')
        return cursor.fetchall()

    @staticmethod
    def get_orders_with_column_names():
        return ["order_id", "name", "total_cost", "status", "pickup_point_name", "address",
                "supplier_name", "supplier_phone"]

    @staticmethod
    def join_orders_1(cursor):
        cursor.execute('''
                SELECT orders.id, goods.name,orders.total_cost, orders.status, pickup_points.name AS pickup_point_name, 
                pickup_points.address, customers.first_name AS customer_name, customers.phone 
                FROM orders
                LEFT JOIN pickup_points ON orders.pickuppoint_id = pickup_points.id
                LEFT JOIN goods ON orders.good_id = goods.id
                LEFT JOIN customers ON orders.customer_id = customers.customer_id
            ''')
        return cursor.fetchall()

    @staticmethod
    def get_orders_with_column_names_1():
        return ["order_id", "name", "total_cost", "status", "pickup_point_name", "address",
                "customer_name", "customer_phone"]


