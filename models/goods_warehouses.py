class GoodsWarehouses:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS goods_warehouses
                          (goods_id INTEGER,
                          warehouse_id INTEGER,
                          PRIMARY KEY (goods_id, warehouse_id),
                          FOREIGN KEY(goods_id) REFERENCES goods(id),
                          FOREIGN KEY(warehouse_id) REFERENCES warehouses(id))''')

    @staticmethod
    def insert_relation(cursor, goods_id, warehouse_id):
        cursor.execute("INSERT INTO goods_warehouses (goods_id, warehouse_id) VALUES (?, ?)", (goods_id, warehouse_id))

    @staticmethod
    def delete_relation(cursor, goods_id, warehouse_id):
        cursor.execute("DELETE FROM goods_warehouses WHERE goods_id=? AND warehouse_id=?", (goods_id, warehouse_id))
