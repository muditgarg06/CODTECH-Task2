import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

# Initialize the database
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT,
                    category TEXT NOT NULL,
                    checked_out BOOLEAN NOT NULL DEFAULT 0,
                    due_date TEXT)''')
    conn.commit()
    conn.close()

# Functions for database interactions
def add_item_to_db(title, author, category):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('INSERT INTO items (title, author, category) VALUES (?, ?, ?)', (title, author, category))
    conn.commit()
    conn.close()

def search_items(title=None, author=None):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    query = 'SELECT * FROM items WHERE 1=1'
    params = []
    if title:
        query += ' AND title LIKE ?'
        params.append(f'%{title}%')
    if author:
        query += ' AND author LIKE ?'
        params.append(f'%{author}%')
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def checkout_item(item_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    due_date = datetime.now() + timedelta(days=14)  # 2 weeks from today
    c.execute('UPDATE items SET checked_out = 1, due_date = ? WHERE id = ?', (due_date.strftime('%Y-%m-%d'), item_id))
    conn.commit()
    conn.close()

def return_item(item_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE items SET checked_out = 0, due_date = NULL WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

def get_overdue_items():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT * FROM items WHERE checked_out = 1 AND due_date < ?', (today,))
    rows = c.fetchall()
    conn.close()
    return rows

# Tkinter GUI Setup
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        # Configuring the grid to center the content
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_rowconfigure(9, weight=1)
        self.root.grid_rowconfigure(10, weight=1)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Add item section
        self.label_title = tk.Label(self.root, text="Title:")
        self.label_title.grid(row=0, column=0, padx=20, pady=5, sticky="e")
        self.entry_title = tk.Entry(self.root)
        self.entry_title.grid(row=0, column=1, padx=20, pady=5)

        self.label_author = tk.Label(self.root, text="Author:")
        self.label_author.grid(row=1, column=0, padx=20, pady=5, sticky="e")
        self.entry_author = tk.Entry(self.root)
        self.entry_author.grid(row=1, column=1, padx=20, pady=5)

        self.label_category = tk.Label(self.root, text="Category:")
        self.label_category.grid(row=2, column=0, padx=20, pady=5, sticky="e")
        self.entry_category = tk.Entry(self.root)
        self.entry_category.grid(row=2, column=1, padx=20, pady=5)

        # Making buttons bigger and centered
        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item, width=20, height=2)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # Search section
        self.search_label = tk.Label(self.root, text="Search Items")
        self.search_label.grid(row=4, column=0, columnspan=2, padx=20, pady=5)

        self.search_title_label = tk.Label(self.root, text="Title:")
        self.search_title_label.grid(row=5, column=0, padx=20, pady=5, sticky="e")
        self.search_title_entry = tk.Entry(self.root)
        self.search_title_entry.grid(row=5, column=1, padx=20, pady=5)

        self.search_author_label = tk.Label(self.root, text="Author:")
        self.search_author_label.grid(row=6, column=0, padx=20, pady=5, sticky="e")
        self.search_author_entry = tk.Entry(self.root)
        self.search_author_entry.grid(row=6, column=1, padx=20, pady=5)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_items, width=20, height=2)
        self.search_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        self.items_listbox = tk.Listbox(self.root, width=50)
        self.items_listbox.grid(row=8, column=0, columnspan=2, padx=20, pady=10)

        # Check out and return section
        self.checkout_button = tk.Button(self.root, text="Check Out Item", command=self.checkout_item, width=20, height=2)
        self.checkout_button.grid(row=9, column=0, padx=20, pady=10, sticky="nsew")

        self.return_button = tk.Button(self.root, text="Return Item", command=self.return_item, width=20, height=2)
        self.return_button.grid(row=9, column=1, padx=20, pady=10, sticky="nsew")

        self.show_overdue_button = tk.Button(self.root, text="Show Overdue Items", command=self.show_overdue_items, width=20, height=2)
        self.show_overdue_button.grid(row=10, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

    def add_item(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        category = self.entry_category.get()
        if title and category:
            add_item_to_db(title, author, category)
            messagebox.showinfo("Success", "Item added successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Title and category are required!")

    def search_items(self):
        title = self.search_title_entry.get()
        author = self.search_author_entry.get()
        items = search_items(title=title, author=author)
        self.items_listbox.delete(0, tk.END)
        for item in items:
            self.items_listbox.insert(tk.END, f"ID: {item[0]} | Title: {item[1]} | Author: {item[2]} | Category: {item[3]} | Checked Out: {item[4]}")

    def checkout_item(self):
        selected_item = self.items_listbox.get(tk.ACTIVE)
        if selected_item:
            item_id = int(selected_item.split('|')[0].split(':')[1].strip())
            checkout_item(item_id)
            messagebox.showinfo("Success", "Item checked out successfully!")

    def return_item(self):
        selected_item = self.items_listbox.get(tk.ACTIVE)
        if selected_item:
            item_id = int(selected_item.split('|')[0].split(':')[1].strip())
            return_item(item_id)
            messagebox.showinfo("Success", "Item returned successfully!")

    def show_overdue_items(self):
        overdue_items = get_overdue_items()
        self.items_listbox.delete(0, tk.END)
        for item in overdue_items:
            self.items_listbox.insert(tk.END, f"Overdue: ID: {item[0]} | Title: {item[1]} | Due Date: {item[5]}")

    def clear_entries(self):
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
