class Supplier:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers
                          (supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          phone TEXT,
                          email TEXT,
                          password TEXT)''')

    @staticmethod
    def insert_supplier(cursor, name, phone, email, password):
        cursor.execute("INSERT INTO suppliers (name, phone, email, password) VALUES (?, ?, ?, ?)",
                       (name, phone, email, password))

    @staticmethod
    def get_all_suppliers(cursor):
        cursor.execute("SELECT * FROM suppliers")
        return cursor.fetchall()

    @staticmethod
    def check_password(cursor, name, password):
        cursor.execute("SELECT supplier_id FROM suppliers WHERE name=? AND password=?", (name, password))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def get_all_suppliers_names(cursor):
        cursor.execute("SELECT name FROM suppliers")
        return cursor.fetchall()





