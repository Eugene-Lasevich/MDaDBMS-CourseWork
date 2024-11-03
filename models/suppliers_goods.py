class SuppliersGoods:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers_goods
                          (supplier_id INTEGER,
                          goods_id INTEGER,
                          PRIMARY KEY (supplier_id, goods_id),
                          FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id),
                          FOREIGN KEY(goods_id) REFERENCES goods(id))''')

    @staticmethod
    def insert_relation(cursor, supplier_id, goods_id):
        cursor.execute("INSERT INTO suppliers_goods (supplier_id, goods_id) VALUES (?, ?)", (supplier_id, goods_id))

    @staticmethod
    def delete_relation(cursor, supplier_id, goods_id):
        cursor.execute("DELETE FROM suppliers_goods WHERE supplier_id=? AND goods_id=?", (supplier_id, goods_id))
