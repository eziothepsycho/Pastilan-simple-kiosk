import tkinter as tk
from tkinter import messagebox
import subprocess
import os
try:
    from PIL import Image, ImageTk
except ImportError:
    print("Please install Pillow: pip install pillow")
    messagebox.showerror("Missing dependency", "Please install Pillow: pip install pillow")
    raise

# --- DATA ---
Chicken = {
    1: ("Regular Chicken", 20),
    2: ("Spicy Chicken", 30),
    3: ("Double Regular Chicken", 40),
    4: ("Double Spicy Chicken", 60)
}

cart = []

# --- STYLES ---
button_style = {
    "font": ("Helvetica", 12),
    "bg": "#3a3a3a",
    "fg": "#ffffff",
    "activebackground": "#555555",
    "activeforeground": "#ffffff",
    "bd": 0
}

label_style = {"bg": "#1e1e1e", "fg": "#ffffff"}
frame_style = {"bg": "#1e1e1e"}
text_style = {"bg": "#2a2a2a", "fg": "#ffffff", "insertbackground": "#ffffff", "font": ("Tahoma")}

# --- FUNCTIONS ---
def center_window(win, width=500, height=650):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def add_to_cart(item_id):
    item_name, item_price = Chicken[item_id]
    show_quantity_pad(item_name, item_price)

def show_quantity_pad(item_name, item_price):
    pad = tk.Toplevel(root)
    pad.overrideredirect(True)
    center_window(pad, 300, 300)
    pad.configure(bg="#1e1e1e")
    pad.grab_set()

    tk.Label(pad, text="Select Quantity", font=("Helvetica", 16, "bold"), bg="#1e1e1e", fg="#ffffff").pack(pady=(15, 5))
    qty = tk.IntVar(value=1)
    display = tk.Label(pad, textvariable=qty, font=("Helvetica", 24), width=10, bg="#1e1e1e", fg="#ffffff")
    display.pack(pady=20)

    btn_frame = tk.Frame(pad, bg="#1e1e1e")
    btn_frame.pack(pady=10)

    def increase():
        qty.set(qty.get() + 1)

    def decrease():
        if qty.get() > 1:
            qty.set(qty.get() - 1)

    tk.Button(btn_frame, text="−", width=8, command=decrease, **button_style).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="+", width=8, command=increase, **button_style).grid(row=0, column=1, padx=10)

    def confirm_quantity_pad():
        confirm_quantity(qty.get(), item_name, item_price, pad)

    tk.Button(pad, text="Confirm", width=15, command=confirm_quantity_pad, **button_style).pack(pady=10)
    tk.Button(pad, text="Cancel", width=15, command=pad.destroy, **button_style).pack(pady=5)

def confirm_quantity(qty, item_name, item_price, pad):
    if qty <= 0:
        show_ok_popup("Please select a valid quantity.")
        return
    subtotal = item_price * qty
    for i in range(len(cart)):
        name, q, total = cart[i]
        if name == item_name:
            new_qty = q + qty
            new_total = item_price * new_qty
            cart[i] = (name, new_qty, new_total)
            break
    else:
        cart.append((item_name, qty, subtotal))
    update_cart_display()
    pad.destroy()

def update_cart_display():
    cart_list.configure(state="normal")
    cart_list.delete("1.0", "end")
    total = 0
    for name, qty, subtotal in cart:
        cart_list.insert("end", f"{qty} x {name} = ₱{subtotal}\n")
        total += subtotal
    cart_list.configure(state="disabled")
    total_label.config(text=f"Total: ₱{total}")

def checkout():
    if not cart:
        show_ok_popup("Your cart is empty.")
        return

    def ask_order_type():
        choice_window = tk.Toplevel(root)
        choice_window.title("Order Type")
        center_window(choice_window, 250, 200)
        choice_window.grab_set()
        choice_window.overrideredirect(True)

        tk.Label(choice_window, text="Select Order Type", font=("Helvetica", 12)).pack(pady=10)

        def set_order_type(mode):
            choice_window.destroy()
            show_receipt(mode)

        tk.Button(choice_window, text="Dine In", command=lambda: set_order_type("Dine In"), **button_style, padx=17, pady=10).pack(pady=5)
        tk.Button(choice_window, text="Take Out", command=lambda: set_order_type("Take Out"), **button_style, padx=10, pady=10).pack(pady=5)
        tk.Button(choice_window, text="Cancel",command=choice_window.destroy,font=("Helvetica", 11),bg="#e57373", fg="white",activebackground="#ef5350", activeforeground="white",bd=0, padx=20, pady=10).pack(pady=10)

    def show_receipt(order_mode):
        loading = tk.Toplevel(root)
        loading.title("Processing Order")
        loading.overrideredirect(True)
        center_window(loading, 250, 100)
        loading.grab_set()

        tk.Label(loading, text="⏳ Preparing your receipt...", font=("Helvetica", 14)).pack(pady=30)

        def finish_loading():
            loading.destroy()
            receipt = "\n".join([f"{qty}x {name}" for name, qty, _ in cart])
            total = sum(total for _, _, total in cart)

            message = (f"Your order:\n{receipt}\n\n"
                       f"Total: ₱{total}\n"
                       f"Order Type: {order_mode}\n\n"
                       "Thank you!")
            cart.clear()
            update_cart_display()
            # Instead of destroying immediately, wait until OK is clicked
            def on_ok():
                root.withdraw()
                subprocess.Popen(["python", "main.py"])

            show_ok_popup(message, on_ok)
        loading.after(1500, finish_loading)
    ask_order_type()

def delete_cart_item(index, window):
    item_name, qty, _ = cart[index]

    # use your custom yes/no popup
    if show_yes_no_popup(f"Delete {qty} x {item_name}?"):
        del cart[index]
        update_cart_display()
        # close and reopen manage cart to refresh the list
        window.destroy()
        manage_cart()
        show_ok_popup(f"{qty} x {item_name} has been removed.")
    else:
        print("User cancelled deletion.")


def edit_cart_item(index, window):
    item_name, _, _ = cart[index]
    item_price = next(price for name, price in Chicken.values() if name == item_name)
    window.destroy()
    show_quantity_pad_edit(item_name, item_price, index)

def show_quantity_pad_edit(item_name, item_price, index):
    pad = tk.Toplevel(root)
    pad.overrideredirect(True)
    center_window(pad, 300, 300)
    pad.configure(bg="#1e1e1e")
    pad.grab_set()

    tk.Label(pad, text="Update Quantity", font=("Helvetica", 16, "bold"), bg="#1e1e1e", fg="#ffffff").pack(pady=(15, 5))
    current_qty = cart[index][1]
    qty = tk.IntVar(value=current_qty)

    display = tk.Label(pad, textvariable=qty, font=("Helvetica", 24), width=10, bg="#1e1e1e", fg="#ffffff")
    display.pack(pady=20)

    btn_frame = tk.Frame(pad, bg="#1e1e1e")
    btn_frame.pack(pady=10)

    def increase():
        qty.set(qty.get() + 1)

    def decrease():
        if qty.get() > 1:
            qty.set(qty.get() - 1)

    tk.Button(btn_frame, text="−", width=8, command=decrease, **button_style).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="+", width=8, command=increase, **button_style).grid(row=0, column=1, padx=10)

    def confirm_edit():
        new_qty = qty.get()
        new_total = item_price * new_qty
        cart[index] = (item_name, new_qty, new_total)
        update_cart_display()
        pad.destroy()

    tk.Button(pad, text="Confirm", width=15, command=confirm_edit, **button_style).pack(pady=10)
    tk.Button(pad, text="Cancel", width=15, command=pad.destroy, **button_style).pack(pady=5)

def manage_cart():
    if not cart:
        show_ok_popup("Your cart is empty.")
        return

    cart_window = tk.Toplevel(root)
    cart_window.overrideredirect(True)
    center_window(cart_window, 400, 300)
    cart_window.grab_set()

    tk.Label(cart_window, text="🛠️ Edit or Delete Items", font=("Helvetica", 14)).pack(pady=10)

    for index, (name, qty, total) in enumerate(cart):
        frame = tk.Frame(cart_window)
        frame.pack(fill='x', padx=10, pady=5)

        tk.Label(frame, text=f"{qty} x {name} = ₱{total}", font=("Helvetica", 11)).pack(side='left')
        tk.Button(frame, text="Edit", width=6,  **button_style, command=lambda i=index: edit_cart_item(i, cart_window)).pack(side='right', padx=5)
        tk.Button(frame, text="Delete", width=6, **button_style, command=lambda i=index: delete_cart_item(i, cart_window)).pack(side='right')

    bottom_frame = tk.Frame(cart_window)
    bottom_frame.pack(side='bottom', fill='x', pady=10, padx=10)

    tk.Button(bottom_frame, text="Cancel", width=10, bg="#1e1e1e", fg="white", font=("Helvetica", 11), bd=0, relief="flat", command=cart_window.destroy).pack(side='right', padx=5)
    tk.Button(bottom_frame,text="Delete All",width=10,bg="#f44336",fg="white",font=("Helvetica", 11),bd=0,relief="flat",command=lambda: delete_all_items(cart_window)
    ).pack(side='right', padx=5)


def go_back_to_main():
    root.destroy()
    subprocess.Popen(["python", "mainmenu.py"])

def delete_all_items(window):
    if show_yes_no_popup("Are you sure you want to delete all items?"):
        cart.clear()
        update_cart_display()
        window.destroy()
        show_ok_popup("All items are deleted.")

    else:
        print("User cancelled deletion.")

def show_ok_popup(message, on_ok=None):
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    center_window(popup, 300, 300)
    popup.configure(bg="#ffffff")

    tk.Label(popup, text=message, padx=20, font=("Helvetica", 12),
             bg="#ffffff", fg="#2a2a2a", wraplength=260).pack(pady=15)

    def close_popup():
        popup.destroy()
        if on_ok:
            on_ok()  # run callback if provided

    tk.Button(popup, text="OK", command=close_popup,
              font=("Helvetica", 10), bg="#4caf50", fg="#ffffff",
              activebackground="#66bb6a", activeforeground="#ffffff",
              bd=0, width=10).pack(pady=10)

def show_yes_no_popup(message):
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    center_window(popup, 300, 150)
    popup.configure(bg="#ffffff")

    result = tk.BooleanVar(value=False)  # store user's choice

    tk.Label(
        popup,
        text=message,
        padx=20,
        font=("Helvetica", 12),
        bg="#ffffff",
        fg="#2a2a2a"
    ).pack(pady=20)

    button_frame = tk.Frame(popup, bg="#ffffff")
    button_frame.pack(pady=10)

    def choose_yes():
        result.set(True)
        popup.destroy()

    def choose_no():
        result.set(False)
        popup.destroy()

    tk.Button(
        button_frame, text="Yes",
        command=choose_yes,
        font=("Helvetica", 10), bg="#4caf50", fg="#ffffff",
        activebackground="#66bb6a", activeforeground="#ffffff",
        bd=0, width=10
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame, text="No",
        command=choose_no,
        font=("Helvetica", 10), bg="#f44336", fg="#ffffff",
        activebackground="#e57373", activeforeground="#ffffff",
        bd=0, width=10
    ).pack(side="left", padx=10)

    popup.grab_set()
    popup.wait_window()  # wait until popup closes
    return result.get()


# --- MAIN WINDOW ---
root = tk.Tk()
root.title("Pastil Kiosk - Chicken Menu")
root.configure(bg="#1e1e1e")
root.attributes("-fullscreen", True)
def load_image(filename, size=(100, 100)):
    """Load image with PIL and return an ImageTk.PhotoImage.
       If file not found or invalid, return an empty PhotoImage placeholder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)

    if not os.path.exists(path):
        print(f"[load_image] file not found: {path}")
        return tk.PhotoImage(width=size[0], height=size[1])  # blank placeholder

    try:
        img = Image.open(path)
        # convert to a format TK likes and resize to fit UI
        img = img.convert("RGBA")
        img.thumbnail(size)  # keeps aspect ratio
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"[load_image] error opening {path}: {e}")
        return tk.PhotoImage(width=size[0], height=size[1])

images = {
    1: load_image("images/regular.jpg", size=(200, 200)),
    2: load_image("images/spicy.jpg", size=(200, 200)),
    3: load_image("images/regular.jpg", size=(200, 200)),
    4: load_image("images/spicy.jpg", size=(200, 200))
}

# --- UI ---
tk.Button(root, text="← Back", font=("Helvetica", 12, "bold"), width=8, bg="#e57373", bd=0, padx=15, pady=8, fg="#ffffff", command=go_back_to_main).pack(anchor='nw', padx=20, pady=20)
tk.Label(root, text="🍗 Chicken Menu", font=("Helvetica", 32, "bold"), **label_style).pack(pady=10)

menu_frame = tk.Frame(root, **frame_style)
for key, (name, price) in Chicken.items():
    item_frame = tk.Frame(menu_frame, bg="#1e1e1e", padx=10, pady=5)
    item_frame.pack(side="left", padx=10, pady=10)

    img_label = tk.Label(item_frame, image=images[key], bg="#1e1e1e")
    img_label.image = images[key]
    img_label.pack(side="top", pady=(5, 2))

    btn = tk.Button(item_frame, text=f"{name} - ₱{price}", command=lambda k=key: add_to_cart(k), **button_style)
    btn.pack(side="top", pady=(10, 5))

menu_frame.pack(pady=10)

tk.Label(root, text="🛒 Your Cart", font=("Helvetica", 20), **label_style).pack(pady=10)
cart_list = tk.Text(root, width=60, height=15, **text_style)
cart_list.pack(pady=5)
cart_list.configure(state="disabled")

total_label = tk.Label(root, text="Total: ₱0", font=("Helvetica", 12, "bold"), **label_style)
total_label.pack(pady=5)

tk.Button(
    root,
    text="Checkout",
    font=("Helvetica", 12),
    bg="#4caf50",
    fg="white",
    bd=0,
    padx=15,   # left-right padding inside button
    pady=8,    # top-bottom padding inside button
    command=checkout
).pack(pady=10, padx=10)
tk.Button(
    root,
    text="Manage",
    font=("Helvetica", 12),
    bg="#2196f3",
    fg="white",
    bd=0,
    padx=20,   # left-right padding inside button
    pady=8,    # top-bottom padding inside button
    command=manage_cart
).pack(pady=10, padx=10)

root.mainloop()
