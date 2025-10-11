import tkinter as tk
from tkinter import ttk
import os, sys
import sqlite3

def resource_path(relative_path):
    """Get absolute path for PyInstaller EXE and normal Python"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Use this for the DB path
db_path = resource_path("orders.db")

class AdminPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#282c73")
        self.parent = parent

        # --- Create frames ---
        self.login_frame = tk.Frame(self, bg="#282c73")
        self.dashboard_frame = tk.Frame(self, bg="#282c73")

        # --- Show login first ---
        self.create_login_ui()
        self.login_frame.pack(expand=True, fill="both")

    # --- LOGIN UI ---
    def create_login_ui(self):
        # Create a frame to center login form
        center_frame = tk.Frame(self.login_frame, bg="#282c73")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center_frame, text="🔐 Admin Login",
            font=("Helvetica", 24, "bold"),
            bg="#282c73", fg="white"
        ).pack(pady=20)

        tk.Label(
            center_frame, text="Username:",
            font=("Helvetica", 14), bg="#282c73", fg="white"
        ).pack(pady=(10, 5))
        self.username_entry = tk.Entry(center_frame, font=("Helvetica", 14), width=25)
        self.username_entry.pack()

        tk.Label(
            center_frame, text="Password:",
            font=("Helvetica", 14), bg="#282c73", fg="white"
        ).pack(pady=(15, 5))
        self.password_entry = tk.Entry(center_frame, font=("Helvetica", 14), width=25, show="•")
        self.password_entry.pack()

        tk.Button(
            center_frame, text="Login", font=("Helvetica", 14, "bold"),
            bg="#4caf50", fg="white", padx=15, pady=5, bd=0,
            command=self.check_login
        ).pack(pady=25)

        self.login_msg = tk.Label(
            center_frame, text="", font=("Helvetica", 12),
            bg="#282c73", fg="red"
        )
        self.login_msg.pack()

    # --- CHECK LOGIN ---
    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Simple static login
        if username == "admin" and password == "1234":
            self.login_frame.pack_forget()
            self.create_dashboard_ui()
            self.dashboard_frame.pack(expand=True, fill="both")
        else:
            self.login_msg.config(text="❌ Invalid username or password!")

    # --- DASHBOARD UI ---
    def create_dashboard_ui(self):
        # Main layout container
        container = tk.Frame(self.dashboard_frame, bg="#282c73")
        container.pack(expand=True, fill="both", padx=40, pady=30)

        tk.Label(
            container,
            text="📋 Pastil Kiosk - Admin Panel",
            font=("Helvetica", 20, "bold"),
            bg="#282c73",
            fg="white"
        ).pack(pady=10)

        # --- Search Frame ---
        search_frame = tk.Frame(container, bg="#282c73")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search:", bg="#282c73", fg="white", font=("Helvetica", 12)).pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30, font=("Helvetica", 12)).pack(side="left", padx=5)

        tk.Button(
            search_frame, text="🔍 Find", font=("Helvetica", 11, "bold"),
            bg="#2196f3", fg="white", padx=8, pady=3, bd=0,
            command=self.search_orders
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame, text="🧹 Clear", font=("Helvetica", 11, "bold"),
            bg="#9e9e9e", fg="white", padx=8, pady=3, bd=0,
            command=self.load_orders
        ).pack(side="left", padx=5)

        # --- Table Frame ---
        table_frame = tk.Frame(container, bg="#282c73")
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = ("ref", "date", "customer", "type", "items", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("ref", text="Reference #")
        self.tree.heading("date", text="Date")
        self.tree.heading("customer", text="Customer")
        self.tree.heading("type", text="Order Type")
        self.tree.heading("items", text="Items")
        self.tree.heading("total", text="Total (₱)")

        for col in columns:
            self.tree.column(col, anchor="center", width=150)
        self.tree.column("items", width=300, anchor="w")
        self.tree.column("total", width=100, anchor="e")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # --- Buttons ---
        btn_frame = tk.Frame(container, bg="#282c73")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="🔄 Refresh", font=("Helvetica", 12, "bold"),
            bg="#4caf50", fg="white", padx=10, pady=5, bd=0,
            command=self.load_orders
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame, text="🗑 Delete", font=("Helvetica", 12, "bold"),
            bg="#f44336", fg="white", padx=10, pady=5, bd=0,
            command=self.delete_order
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame, text="❌ Close", font=("Helvetica", 12, "bold"),
            bg="#9c27b0", fg="white", padx=10, pady=5, bd=0,
            command=self.back_to_main
        ).grid(row=0, column=2, padx=5)

        self.total_label = tk.Label(
            container, text="", bg="#282c73", fg="white", font=("Helvetica", 12)
        )
        self.total_label.pack(pady=(5, 10))

        self.load_orders()

    # --- DATABASE + FUNCTIONS (no change) ---
    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT reference_number, date, customer_name, order_type, items, total FROM orders")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)
        self.total_label.config(text=f"Total Orders: {len(rows)}")

    def search_orders(self):
        query = self.search_var.get().strip()
        if not query:
            self.show_ok_popup("Please enter a search term.")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT reference_number, date, customer_name, order_type, items, total
            FROM orders
            WHERE reference_number LIKE ? OR customer_name LIKE ?
        """, (f"%{query}%", f"%{query}%"))
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.total_label.config(text=f"Search Results: {len(rows)} order(s) found")

    def delete_order(self):
        selected = self.tree.selection()
        if not selected:
            self.show_ok_popup("Please select an order to delete.")
            return
        confirm = self.show_yes_no_popup("Are you sure you want to delete this order?")
        if not confirm:
            return
        item = self.tree.item(selected[0])
        ref_number = item["values"][0]
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE reference_number = ?", (ref_number,))
        conn.commit()
        conn.close()
        self.tree.delete(selected[0])
        self.total_label.config(text="Order deleted successfully ✅")

    def back_to_main(self):
        self.destroy()
        self.parent.children["!frame"].pack(expand=True, fill="both")

    # --- POPUPS (same) ---
    def center_window(self, win, width=300, height=150):
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def show_ok_popup(self, message):
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)
        self.center_window(popup, 300, 150)
        popup.configure(bg="#ffffff")
        popup.grab_set()
        tk.Label(popup, text=message, padx=20, font=("Helvetica", 12),
                 bg="#ffffff", fg="#282c73", wraplength=260).pack(pady=30)
        tk.Button(popup, text="OK", command=popup.destroy,
                  font=("Helvetica", 10), bg="#4caf50", fg="#ffffff",
                  bd=0, width=10).pack(pady=10)

    def show_yes_no_popup(self, message):
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)
        self.center_window(popup, 300, 200)
        popup.configure(bg="#ffffff")
        popup.grab_set()
        result = tk.BooleanVar(value=False)
        tk.Label(popup, text=message, padx=20, font=("Helvetica", 12),
                 bg="#ffffff", fg="#282c73", wraplength=260).pack(pady=20)
        button_frame = tk.Frame(popup, bg="#ffffff")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Yes", command=lambda: [result.set(True), popup.destroy()],
                  font=("Helvetica", 10), bg="#4caf50", fg="#ffffff",
                  bd=0, width=10).pack(side="left", padx=10)
        tk.Button(button_frame, text="No", command=lambda: [result.set(False), popup.destroy()],
                  font=("Helvetica", 10), bg="#f44336", fg="#ffffff",
                  bd=0, width=10).pack(side="left", padx=10)
        popup.wait_window()
        return result.get()
