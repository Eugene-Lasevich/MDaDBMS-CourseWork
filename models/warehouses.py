class Warehouses:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS warehouses
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          address TEXT,
                          supplier_id INTEGER,
                          FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id))''')

    @staticmethod
    def insert_warehouse(cursor, name, address, supplier_id):
        cursor.execute("INSERT INTO warehouses (name, address, supplier_id) VALUES (?, ?, ?)", (name, address, supplier_id))

    @staticmethod
    def get_all_warehouses(cursor):
        cursor.execute("SELECT id, name, address FROM warehouses")
        return cursor.fetchall()

    @staticmethod
    def get_column_names(cursor):
        cursor.execute("PRAGMA table_info(warehouses)")
        return [column[1] for column in cursor.fetchall() if column[1] != 'supplier_id']

    @staticmethod
    def drop_table(cursor):
        cursor.execute("DROP TABLE IF EXISTS warehouses")

    @staticmethod
    def get_all_warehouses_of_user(cursor, supplier_id):
        cursor.execute("SELECT id, name, address FROM warehouses WHERE supplier_id=?", (supplier_id,))
        return cursor.fetchall()

    @staticmethod
    def update_warehouse(cursor, old_name, old_address, new_name,new_address, supplier_id):
        cursor.execute("UPDATE warehouses SET name=?, address=? WHERE name=? AND address=? AND supplier_id=?",
                       (new_name, new_address, old_name, old_address, supplier_id))

    @staticmethod
    def delete_warehouse(cursor, name, address, supplier_id):
        cursor.execute("DELETE FROM warehouses WHERE name=? AND address=? AND supplier_id=?",
                       (name, address, supplier_id))
