class Reviews:
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS reviews
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          customer_id INTEGER,
                          good_id INTEGER,
                          text TEXT,
                          rating INTEGER,
                          FOREIGN KEY(customer_id) REFERENCES customers(id),
                          FOREIGN KEY(good_id) REFERENCES goods(id))''')

    @staticmethod
    def insert_review(cursor, customer_id, good_id, text, rating):
        cursor.execute("INSERT INTO reviews (customer_id, good_id, text, rating) VALUES (?, ?, ?, ?)",
                       (customer_id, good_id, text, rating))

    @staticmethod
    def get_all_reviews(cursor):
        cursor.execute("SELECT id, customer_id, good_id, text, rating FROM reviews")
        return cursor.fetchall()

    @staticmethod
    def get_column_names(cursor):
        cursor.execute("PRAGMA table_info(reviews)")
        return [column[1] for column in cursor.fetchall() if column[1] not in ['customer_id', 'good_id']]

    @staticmethod
    def drop_table(cursor):
        cursor.execute("DROP TABLE IF EXISTS reviews")

    @staticmethod
    def get_reviews_of_customer(cursor, customer_id):
        cursor.execute("SELECT id, good_id, text, rating FROM reviews WHERE customer_id=?", (customer_id,))
        return cursor.fetchall()

    @staticmethod
    def get_reviews_of_good(cursor, good_id):
        cursor.execute("SELECT id, customer_id, text, rating FROM reviews WHERE good_id=?", (good_id,))
        return cursor.fetchall()

    @staticmethod
    def update_review(cursor, review_id, new_text, new_rating):
        cursor.execute("UPDATE reviews SET text=?, rating=? WHERE id=?",
                       (new_text, new_rating, review_id))

    @staticmethod
    def delete_review(cursor, review_id):
        cursor.execute("DELETE FROM reviews WHERE id=?", (review_id,))

    @staticmethod
    def insert_review_by_name(cursor, customer_id, name, text, rating):
        cursor.execute("SELECT id FROM goods WHERE name=?", (name,))
        result = cursor.fetchone()
        print(result)
        if result:
            good_id = result[0]
            cursor.execute("INSERT INTO reviews (customer_id, good_id, text, rating) VALUES (?, ?, ?, ?)",
                           (customer_id, good_id, text, rating))
        else:
            # Если товар с указанным именем не найден, выдаем предупреждение
            print("The specified Good Name does not exist.")

