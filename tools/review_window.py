import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from models.reviews import Reviews


class ReviewWindow:
    def __init__(self, root, customer_id):
        self.root = root
        self.root.title("Create Review")

        self.customer_id = customer_id[0]

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=10)

        # Label and Entry for Name
        name_label = ttk.Label(self.main_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.main_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label and Entry for Text
        text_label = ttk.Label(self.main_frame, text="Text:")
        text_label.grid(row=1, column=0, padx=5, pady=5)
        self.text_entry = ttk.Entry(self.main_frame)
        self.text_entry.grid(row=1, column=1, padx=5, pady=5)

        # Label and Combobox for Rating
        rating_label = ttk.Label(self.main_frame, text="Rating:")
        rating_label.grid(row=2, column=0, padx=5, pady=5)
        self.rating_combo = ttk.Combobox(self.main_frame, values=[1, 2, 3, 4, 5], state="readonly")
        self.rating_combo.grid(row=2, column=1, padx=5, pady=5)
        self.rating_combo.current(0)

        # Submit Button
        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.submit_review)
        submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def submit_review(self):
        name = self.name_entry.get()
        text = self.text_entry.get()
        rating = self.rating_combo.get()

        try:
            rating = int(rating)

            if not text:
                messagebox.showwarning("Warning", "Please enter the text of the review.")
            elif rating < 1 or rating > 5:
                messagebox.showwarning("Warning", "Rating must be between 1 and 5.")
            else:
                db = Database('example.db')
                conn = db.connect()
                cursor = conn.cursor()
                Reviews.create_table(cursor)

                # Check if the name exists
                cursor.execute("SELECT * FROM goods WHERE name=?", (name,))
                if cursor.fetchone():
                    # Insert the review into the database
                    Reviews.insert_review_by_name(cursor, self.customer_id, name, text, rating)
                    conn.commit()
                    messagebox.showinfo("Success", "Review submitted successfully.")
                    for row in Reviews.get_all_reviews(cursor):
                        print(row)
                    self.root.destroy()
                else:
                    messagebox.showwarning("Warning", "The specified Name does not exist.")

                conn.close()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid value for Rating.")


def open_review_window(customer_id):
    root = tk.Toplevel()
    app = ReviewWindow(root, customer_id)
