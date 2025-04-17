import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Initialize DataBase
def init_db():
    conn = sqlite3.connect('inventory_gui.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL)''')
    conn.commit()
    # Add a default user
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'admin'))
    conn.commit()
    conn.close()


def validate_user(username, password):
    conn = sqlite3.connect('inventory_gui.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result


def add_product(name, quantity, price):
    if not name or quantity < 0 or price < 0:
        return False
    conn = sqlite3.connect('inventory_gui.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()
    return True


def get_products():
    conn = sqlite3.connect('inventory_gui.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    results = c.fetchall()
    conn.close()
    return results


def delete_product(product_id):
    conn = sqlite3.connect('inventory_gui.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect('inventory_gui.db')
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?", (name, quantity, price, product_id))
    conn.commit()
    conn.close()

# GUI
class InventoryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management System")
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.master, text="Username").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()
        tk.Label(self.master, text="Password").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()
        tk.Button(self.master, text="Login", command=self.login).pack()

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if validate_user(user, pwd):
            self.main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def main_screen(self):
        self.clear_screen()

        tk.Label(self.master, text="Inventory Management").grid(row=0, column=0, columnspan=4)

       
        tk.Label(self.master, text="Name").grid(row=1, column=0)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Quantity").grid(row=2, column=0)
        self.quantity_entry = tk.Entry(self.master)
        self.quantity_entry.grid(row=2, column=1)

        tk.Label(self.master, text="Price").grid(row=3, column=0)
        self.price_entry = tk.Entry(self.master)
        self.price_entry.grid(row=3, column=1)

        tk.Button(self.master, text="Add", command=self.add_product_gui).grid(row=4, column=0, columnspan=2)

        
        self.tree = ttk.Treeview(self.master, columns=("ID", "Name", "Qty", "Price"), show='headings')
        for col in ("ID", "Name", "Qty", "Price"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=5, column=0, columnspan=4)

      
        tk.Button(self.master, text="Edit", command=self.edit_product).grid(row=6, column=0)
        tk.Button(self.master, text="Delete", command=self.delete_selected).grid(row=6, column=1)
        tk.Button(self.master, text="Refresh", command=self.populate_products).grid(row=6, column=2)
        tk.Button(self.master, text="Low Stock Report", command=self.low_stock_report).grid(row=6, column=3)

        self.populate_products()

    def add_product_gui(self):
        try:
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            if add_product(name, quantity, price):
                self.populate_products()
                self.name_entry.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Validation", "Invalid data")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and price")

    def populate_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in get_products():
            self.tree.insert('', tk.END, values=row)

    def delete_selected(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            delete_product(item['values'][0])
            self.populate_products()

    def edit_product(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, item[1])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, item[2])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, item[3])

            def update():
                try:
                    update_product(item[0], self.name_entry.get(), int(self.quantity_entry.get()), float(self.price_entry.get()))
                    self.populate_products()
                    update_btn.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Invalid update data")

            update_btn = tk.Button(self.master, text="Update", command=update)
            update_btn.grid(row=4, column=2, columnspan=2)

    def low_stock_report(self):
        low_stock = [p for p in get_products() if p[2] < 10]
        report = "Low Stock Items (Qty < 10):\n"
        for p in low_stock:
            report += f"{p[1]} (Qty: {p[2]})\n"
        messagebox.showinfo("Low Stock Report", report)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
