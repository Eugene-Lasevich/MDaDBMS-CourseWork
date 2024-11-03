class Customer:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers
                          (customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          first_name TEXT,
                          last_name TEXT,
                          phone TEXT,
                          password TEXT)''')

    @staticmethod
    def insert_customer(cursor, first_name, last_name, phone, password):  # Убрано поле name
        cursor.execute("INSERT INTO customers (first_name, last_name, phone, password) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, phone, password))

    @staticmethod
    def get_all_customers(cursor):
        cursor.execute("SELECT * FROM customers")
        return cursor.fetchall()

    @staticmethod
    def check_password(cursor, first_name, last_name, password):  # Изменено на first_name и last_name
        cursor.execute("SELECT * FROM customers WHERE first_name=? AND last_name=? AND password=?",
                       (first_name, last_name, password))  # Изменено на first_name и last_name
        return cursor.fetchone()
