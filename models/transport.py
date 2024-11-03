class Transport:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS transport
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          type TEXT,
                          supplier_id INTEGER,
                          FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id))''')

    @staticmethod
    def insert_transport(cursor, type, supplier_id):
        cursor.execute("INSERT INTO transport (type, supplier_id) VALUES (?, ?)", (type, supplier_id))

    @staticmethod
    def get_all_transport(cursor):
        cursor.execute("SELECT id, type FROM transport")
        return cursor.fetchall()

    @staticmethod
    def get_column_names(cursor):
        cursor.execute("PRAGMA table_info(transport)")
        return [column[1] for column in cursor.fetchall() if column[1] != 'supplier_id']

    @staticmethod
    def drop_table(cursor):
        cursor.execute("DROP TABLE IF EXISTS transport")

    @staticmethod
    def get_all_transport_of_user(cursor, supplier_id):
        cursor.execute("SELECT id, type FROM transport WHERE supplier_id=?", (supplier_id,))
        return cursor.fetchall()

    @staticmethod
    def update_transport(cursor, old_type, new_type, supplier_id):
        cursor.execute("UPDATE transport SET type=? WHERE type=? AND supplier_id=?", (new_type, old_type, supplier_id))

    @staticmethod
    def delete_transport(cursor, type, supplier_id):
        cursor.execute("DELETE FROM transport WHERE type=? AND supplier_id=?", (type, supplier_id))
