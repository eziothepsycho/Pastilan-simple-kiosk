import tkinter as tk
import subprocess
import os
try:
    from PIL import Image, ImageTk
except ImportError:
    import tkinter.messagebox as messagebox
    print("Please install Pillow: pip install pillow")
    messagebox.showerror("Missing dependency", "Please install Pillow: pip install pillow")
    raise

class ChickenKiosk(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#282c73")  # set Frame background too
        self.root = master
        self.root.title("Pastil Kiosk - Chicken Menu")
        self.root.configure(bg="#282c73")  # dark background
        self.root.attributes("-fullscreen", True)
        self.pack(fill="both", expand=True)
        # --- DATA ---
        self.Chicken = {
            1: ("Regular Chicken", 20),
            2: ("Spicy Chicken", 30),
            3: ("Double Regular", 40),
            4: ("Double Spicy", 60)
        }
        # --- DATA ---
        self.AddOns = {
            101: ("Softdrinks", 20),
            102: ("Sunny Side Up", 10),
            103: ("Boiled Egg", 8),
            104: ("Lumpiang Shanghai", 15)
        }
        self.cart = []

        # --- STYLES ---
        self.button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#282c73",
            "fg": "#ffffff",
            "activebackground": "#282c73",
            "activeforeground": "#ffffff",
            "bd": 0
        }
        self.label_style = {"fg": "#ffffff", "bg": "#282c73"}
        self.text_style = {"bg": "#2a2a2a", "fg": "#ffffff", "insertbackground": "#ffffff", "font": ("Tahoma")}

        # --- IMAGES ---
        self.images = {
            1: self.load_image("images/regular.jpg"),
            2: self.load_image("images/spicy.jpg"),
            3: self.load_image("images/regular.jpg"),
            4: self.load_image("images/spicy.jpg")
        }

        self.addons_images = {
        101: self.load_image("images/softdrinks.jpg"),
        102: self.load_image("images/sunnysideup.jpg"),
        103: self.load_image("images/boiledegg.jpg"),
        104: self.load_image("images/shanghai.jpg")
    }


        # --- UI ---
        tk.Button(self, text="← Back", font=("Helvetica", 12, "bold"), width=8,
                  bg="#e57373", bd=0, padx=15, pady=8, fg="#ffffff",
                  command=self.go_back_to_main).pack(anchor='nw', padx=20, pady=20)
         # --- Chicken Menu ---
        tk.Label(self, text="🍗 Chicken Menu", font=("Helvetica", 32, "bold"), **self.label_style).pack(pady=10)
        self.chicken_frame = tk.Frame(self, bg="#282c73")
        self.chicken_frame.pack(pady=20)

        columns = 4
        for index, (key, (name, price)) in enumerate(self.Chicken.items()):
            row = index // columns
            col = index % columns
            self.create_menu_item(key, name, price, parent=self.chicken_frame, row=row, col=col, image=self.images.get(key))

        # --- Add-Ons Menu ---
        tk.Label(self, text="➕ Add-Ons", font=("Helvetica", 28, "bold"), **self.label_style).pack(pady=10)
        self.addons_frame = tk.Frame(self, bg="#ffffff")
        self.addons_frame.pack(pady=20)

        for index, (key, (name, price)) in enumerate(self.AddOns.items()):
            row = index // columns
            col = index % columns
            self.create_menu_item(
                key, name, price, parent=self.addons_frame, row=row, col=col, image=self.addons_images.get(key)
            )

        # --- View Cart and Checkout Buttons ---
        buttons_frame = tk.Frame(self, bg="#282c73")
        buttons_frame.pack(pady=20)
        tk.Button(buttons_frame, text="View Cart", font=("Helvetica", 12), bg="#54bd46", fg="#ffffff",
                bd=0, padx=20, pady=8, command=self.manage_cart).pack(side='left', padx=10)

        tk.Button(buttons_frame, text="Checkout", font=("Helvetica", 12), bg="#a13333", fg="#ffffff",
                bd=0, padx=20, pady=8, command=self.checkout).pack(side='left', padx=10)


    # --- IMAGE LOADER ---
    def load_image(self, filename, size=(200, 200)):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, filename)
        if not os.path.exists(path):
            print(f"[load_image] file not found: {path}")
            return tk.PhotoImage(width=size[0], height=size[1])
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            img = img.convert("RGBA")
            img.thumbnail(size)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"[load_image] error opening {path}: {e}")
            return tk.PhotoImage(width=size[0], height=size[1])

    # --- MENU ITEM CREATION ---
    def create_menu_item(self, key, name, price, parent, row, col, image=None):
        item_frame = tk.Frame(parent, bg="#ffffff", padx=10, pady=10, bd=2, relief="ridge")
        item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        if image:
            img_label = tk.Label(item_frame, image=image, bg="#ffffff")
            img_label.image = image
            img_label.pack(pady=(5,10))

        tk.Button(
            item_frame, text=f"{name}\n₱{price}", command=lambda k=key: self.add_to_cart(k),
            **self.button_style, wraplength=150, width=15
        ).pack(pady=(0,5))
        
    # --- CENTER WINDOW HELPER ---
    def center_window(self, win, width=500, height=650):
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    # --- ADD TO CART ---
    def add_to_cart(self, item_id):
        if item_id in self.Chicken:
            item_name, item_price = self.Chicken[item_id]
        else:
            item_name, item_price = self.AddOns[item_id]
        self.show_quantity_pad(item_name, item_price)

    def show_quantity_pad(self, item_name, item_price):
        pad = tk.Toplevel(self.root)
        pad.overrideredirect(True)
        self.center_window(pad, 300, 300)
        pad.configure(bg="#ffffff")
        pad.grab_set()

        tk.Label(pad, text="Select Quantity", font=("Helvetica", 16, "bold"),
                 bg="#ffffff", fg="#282c73").pack(pady=(15, 5))
        qty = tk.IntVar(value=1)
        display = tk.Label(pad, textvariable=qty, font=("Helvetica", 24), width=10,
                           bg="#ffffff", fg="#282c73")
        display.pack(pady=20)

        btn_frame = tk.Frame(pad, bg="#ffffff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="−", width=8, command=lambda: self.modify_qty(qty, -1),
                  **self.button_style).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="+", width=8, command=lambda: self.modify_qty(qty, 1),
                  **self.button_style).grid(row=0, column=1, padx=10)

        tk.Button(pad, text="Confirm", width=15, command=lambda: self.confirm_quantity(qty.get(), item_name, item_price, pad),
                  **self.button_style).pack(pady=10)
        tk.Button(pad, text="Cancel", width=15, command=pad.destroy, **self.button_style).pack(pady=5)

    def modify_qty(self, qty_var, delta):
        if qty_var.get() + delta > 0:
            qty_var.set(qty_var.get() + delta)

    def confirm_quantity(self, qty, item_name, item_price, pad):
        subtotal = item_price * qty
        for i, (name, q, total) in enumerate(self.cart):
            if name == item_name:
                new_qty = q + qty
                new_total = item_price * new_qty
                self.cart[i] = (name, new_qty, new_total)
                break
        else:
            self.cart.append((item_name, qty, subtotal))
        pad.destroy()
        self.show_ok_popup(f"{qty} x {item_name} added to cart.")

    # --- CART MANAGEMENT ---
    def manage_cart(self):
        if not self.cart:
            self.show_ok_popup("Your cart is empty.")
            return

        cart_window = tk.Toplevel(self.root)
        cart_window.overrideredirect(True)
        self.center_window(cart_window, 700, 350)
        cart_window.configure(bg="#1e1e1e")
        cart_window.grab_set()

        tk.Label(cart_window, text="🛠️ Edit or Delete Items", font=("Helvetica", 14),
                bg="#1e1e1e", fg="#ffffff").pack(pady=10)

        # Scrollable frame
        canvas = tk.Canvas(cart_window, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(cart_window, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#1e1e1e")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cart items
        for index, (name, qty, total) in enumerate(self.cart):
            frame = tk.Frame(scroll_frame, bg="#1e1e1e", pady=5, padx=5)
            frame.pack(fill='x', pady=3, padx=5)

            tk.Label(frame, text=f"{qty} x {name} = ₱{total}", font=("Helvetica", 11),
                    bg="#1e1e1e", fg="white").pack(side='left')

            tk.Button(frame, text="Edit", width=6,
                    font=("Helvetica", 10, "bold"), bg="#3a3a3a", fg="white",
                    activebackground="#555555", activeforeground="white",
                    bd=0, command=lambda i=index: self.edit_cart_item(i, cart_window)).pack(side='right', padx=5)

            tk.Button(frame, text="Delete", width=6,
                    font=("Helvetica", 10, "bold"), bg="#f44336", fg="white",
                    activebackground="#d32f2f", activeforeground="white",
                    bd=0, command=lambda i=index: self.delete_cart_item(i, cart_window)).pack(side='right')

        # Bottom buttons
        bottom_frame = tk.Frame(cart_window, bg="#1e1e1e")
        bottom_frame.pack(side='bottom', fill='x', pady=10, padx=10)
        tk.Button(bottom_frame, text="Cancel", width=10,
                font=("Helvetica", 11, "bold"), bg="#3a3a3a", fg="white",
                bd=0, relief="flat", command=cart_window.destroy).pack(side='right', padx=5)
        tk.Button(bottom_frame, text="Delete All", width=10,
                font=("Helvetica", 11, "bold"), bg="#f44336", fg="white",
                bd=0, relief="flat", command=lambda: self.delete_all_items(cart_window)).pack(side='right', padx=5)

    # (The rest of the code remains unchanged, just ensure every popup, label, button, and frame uses dark theme colors)

    def edit_cart_item(self, index, window):
        item_name, _, _ = self.cart[index]

        # Look for the price in Chicken or AddOns
        if any(item_name == name for name, _ in self.Chicken.values()):
            item_price = next(price for name, price in self.Chicken.values() if name == item_name)
        else:
            item_price = next(price for name, price in self.AddOns.values() if name == item_name)

        window.destroy()
        self.show_quantity_pad_edit(item_name, item_price, index)

    def show_quantity_pad_edit(self, item_name, item_price, index):
        pad = tk.Toplevel(self.root)
        pad.overrideredirect(True)
        self.center_window(pad, 300, 300)
        pad.configure(bg="#ffffff")
        pad.grab_set()

        tk.Label(pad, text="Update Quantity", font=("Helvetica", 16, "bold"),
                 bg="#ffffff", fg="#282c73").pack(pady=(15, 5))
        current_qty = self.cart[index][1]
        qty = tk.IntVar(value=current_qty)
        display = tk.Label(pad, textvariable=qty, font=("Helvetica", 24), width=10,
                           bg="#ffffff", fg="#282c73")
        display.pack(pady=20)

        btn_frame = tk.Frame(pad, bg="#ffffff")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="−", width=8, command=lambda: self.modify_qty(qty, -1), **self.button_style).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="+", width=8, command=lambda: self.modify_qty(qty, 1), **self.button_style).grid(row=0, column=1, padx=10)

        tk.Button(pad, text="Confirm", width=15, command=lambda: self.confirm_edit(qty.get(), item_name, item_price, index, pad),
                  **self.button_style).pack(pady=10)
        tk.Button(pad, text="Cancel", width=15, command=pad.destroy, **self.button_style).pack(pady=5)

    def confirm_edit(self, new_qty, item_name, item_price, index, pad):
        new_total = item_price * new_qty
        self.cart[index] = (item_name, new_qty, new_total)
        pad.destroy()
        self.show_ok_popup(f"{new_qty} x {item_name} updated in cart.")

    def delete_cart_item(self, index, window):
        item_name, qty, _ = self.cart[index]
        if self.show_yes_no_popup(f"Delete {qty} x {item_name}?"):
            del self.cart[index]
            window.destroy()
            self.show_ok_popup(f"{qty} x {item_name} removed from cart.")
            self.manage_cart()

    def delete_all_items(self, window):
        if self.show_yes_no_popup("Are you sure you want to delete all items?"):
            self.cart.clear()
            window.destroy()
            self.show_ok_popup("All items removed from cart.")

    # --- CHECKOUT ---
    def checkout(self):
        if not self.cart:
            self.show_ok_popup("Your cart is empty.")
            return

        choice_window = tk.Toplevel(self.root)
        choice_window.overrideredirect(True)
        self.center_window(choice_window, 250, 250)
        choice_window.configure(bg="#ffffff")
        choice_window.grab_set()
        tk.Label(choice_window, text="Select Order Type", bg="#ffffff", fg="#282c73", font=("Helvetica", 12, "bold")).pack(pady=10)

        def finish_checkout(mode):
            choice_window.destroy()
            self.ask_customer_name(mode)

        tk.Button(choice_window, text="Dine In", command=lambda: finish_checkout("Dine In"), **self.button_style, padx=17, pady=10).pack(pady=5)
        tk.Button(choice_window, text="Take Out", command=lambda: finish_checkout("Take Out"), **self.button_style, padx=10, pady=10).pack(pady=5)
        tk.Button(choice_window, text="Cancel", command=choice_window.destroy,
                  font=("Helvetica", 11), bg="#f44336", fg="white",
                  activebackground="#e57373", activeforeground="white",
                  bd=0, padx=20, pady=10).pack(pady=10)
        
    def ask_customer_name(self, order_mode):
        name_popup = tk.Toplevel(self.root)
        name_popup.overrideredirect(True)
        self.center_window(name_popup, 300, 200)
        name_popup.configure(bg="#ffffff")
        name_popup.grab_set()

        tk.Label(name_popup, text="Enter Customer Name", font=("Helvetica", 14, "bold"),
                bg="#ffffff", fg="#282c73").pack(pady=20)

        name_var = tk.StringVar()
        entry = tk.Entry(name_popup, textvariable=name_var, font=("Helvetica", 12), width=25)
        entry.pack(pady=10)
        entry.focus()

        tk.Button(name_popup, text="Confirm", font=("Helvetica", 12), bg="#4caf50", fg="white",
                bd=0, width=10, command=lambda: self.confirm_customer_name(name_var.get(), order_mode, name_popup)
                ).pack(pady=10)
    
    def confirm_customer_name(self, customer_name, order_mode, popup):
        if not customer_name.strip():
            self.show_ok_popup("Please enter a name.")
            return
        popup.destroy()
        self.show_receipt(order_mode, customer_name)
    
    def show_receipt(self, order_mode, customer_name):
        # Loading popup
        loading = tk.Toplevel(self.root)
        loading.overrideredirect(True)
        self.center_window(loading, 250, 100)
        loading.grab_set()
        loading.configure(bg="#ffffff")
        tk.Label(loading, text="⏳ Preparing your receipt...", font=("Helvetica", 14), bg="#ffffff", fg="#282c73").pack(pady=30)

        def finish_loading():
            loading.destroy()

            # Receipt window
            receipt_win = tk.Toplevel(self.root)
            receipt_win.overrideredirect(True)
            receipt_win.configure(bg="#ffffff")  # light background
            self.center_window(receipt_win, 600, 800)
            receipt_win.grab_set()

            # Main frame
            main_frame = tk.Frame(receipt_win, bg="#D3D3D3")  # light gray frame
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Header
            tk.Label(main_frame, text="🍗 Pastil Kiosk", font=("Helvetica", 20, "bold"), bg="#D3D3D3", fg="#282c73").pack(pady=(0, 5))
            tk.Label(main_frame, text="OFFICIAL RECEIPT", font=("Helvetica", 16, "bold"), bg="#D3D3D3", fg="#282c73").pack(pady=(0, 15))

            # Items frame
            item_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")  # white item background
            item_frame.pack(fill="both", expand=True, padx=10, pady=10)

            tk.Label(item_frame, text="Qty  Item                     Subtotal", font=("Helvetica", 12, "bold"),
                    bg="#ffffff", fg="#282c73").pack(anchor="w", padx=10, pady=5)

            total = 0
            for name, qty, subtotal in self.cart:
                tk.Label(item_frame, text=f"{qty:<3} {name:<20} ₱{subtotal}", font=("Helvetica", 12),
                        bg="#ffffff", fg="#282c73").pack(anchor="w", padx=10)
                total += subtotal

            # Total and order type
            tk.Label(main_frame, text=f"TOTAL: ₱{total}", font=("Helvetica", 14, "bold"), bg="#D3D3D3", fg="#282c73").pack(pady=(10, 5))
            tk.Label(main_frame, text=f"Customer: {customer_name}", font=("Helvetica", 12), bg="#D3D3D3", fg="#282c73").pack(pady=(0, 5))
            tk.Label(main_frame, text=f"Order Type: {order_mode}", font=("Helvetica", 12), bg="#D3D3D3", fg="#282c73").pack(pady=(0, 15))
            tk.Label(main_frame, text="Thank you for your order!", font=("Helvetica", 12, "italic"), bg="#D3D3D3", fg="#282c73").pack(pady=(0, 15))

            # Close button
            def close_and_restart():
                receipt_win.destroy()
                self.root.destroy()
                subprocess.Popen(["python", "main.py"])

            tk.Button(main_frame, text="Close", font=("Helvetica", 12, "bold"), bg="#4caf50", fg="white", bd=0, padx=10, pady=10,
                    activebackground="#66bb6a", activeforeground="white",
                    command=close_and_restart).pack(side="bottom", pady=10)

            # Clear cart
            self.cart.clear()
            #self.update_cart_display()

        loading.after(1500, finish_loading)




    # --- POPUPS ---
    def show_ok_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        self.center_window(popup, 300, 150)
        popup.configure(bg="#ffffff")
        popup.grab_set()
        tk.Label(popup, text=message, padx=20, font=("Helvetica", 12),
                bg="#ffffff", fg="#282c73", wraplength=260).pack(pady=30)  # white text
        tk.Button(popup, text="OK", command=popup.destroy,
                font=("Helvetica", 10), bg="#4caf50", fg="#ffffff",
                activebackground="#66bb6a", activeforeground="#ffffff",
                bd=0, width=10).pack(pady=10)

    
    def show_ok_popup_receipt(self, message):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        self.center_window(popup, 300, 150)
        popup.configure(bg="#ffffff")
        popup.grab_set()
        tk.Label(popup, text=message, padx=20, font=("Helvetica", 12),
                bg="#ffffff", fg="#282c73", wraplength=260).pack(pady=30)  # white text
        tk.Button(popup, text="OK", command=popup.destroy,
                font=("Helvetica", 10), bg="#4caf50", fg="#ffffff",
                activebackground="#66bb6a", activeforeground="#ffffff",
                bd=0, width=10).pack(pady=10)

    def show_yes_no_popup(self, message):
        popup = tk.Toplevel(self.root)
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
                  activebackground="#66bb6a", activeforeground="#ffffff",
                  bd=0, width=10).pack(side="left", padx=10)

        tk.Button(button_frame, text="No", command=lambda: [result.set(False), popup.destroy()],
                  font=("Helvetica", 10), bg="#f44336", fg="#ffffff",
                  activebackground="#e57373", activeforeground="#ffffff",
                  bd=0, width=10).pack(side="left", padx=10)

        popup.grab_set()
        popup.wait_window()
        return result.get()

    # --- NAVIGATION ---
    def go_back_to_main(self):
        self.root.destroy()
        subprocess.Popen(["python", "main.py"])



