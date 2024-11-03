class PickupPoint:
    def __init__(self, address, name):
        self.address = address
        self.name = name

    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS pickup_points
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          address TEXT,
                          name TEXT)''')

    @staticmethod
    def insert_pickup_point(cursor, address, name):
        cursor.execute("INSERT INTO pickup_points (address, name) VALUES (?, ?)", (address, name))

    @staticmethod
    def get_all_pickup_points(cursor):
        cursor.execute("SELECT id, address, name FROM pickup_points")
        return cursor.fetchall()

    @staticmethod
    def get_column_names(cursor):
        cursor.execute("PRAGMA table_info(pickup_points)")
        return [column[1] for column in cursor.fetchall() if column[1] != 'id']

    @staticmethod
    def drop_table(cursor):
        cursor.execute("DROP TABLE IF EXISTS pickup_points")
