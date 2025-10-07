import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog

# Menu data
Fish = {
    1: ("Regular Fish", 20),
    2: ("Spicy Fish", 30),
    3: ("Double Regular Fish", 40),
    4: ("Double Spicy Fish", 60)
}

cart = []

# Add to cart
def add_to_cart(item_id):
    item_name, item_price = Fish[item_id]
    show_quantity_pad(item_name, item_price)

def show_quantity_pad(item_name, item_price):
    pad = tk.Toplevel(root)
    pad.title("Select Quantity")
    pad.geometry("400x350")
    pad.configure(bg="#f0f0f0")
    pad.grab_set()

    selected_qty = tk.StringVar(value="")

    display = tk.Label(pad, textvariable=selected_qty, font=("Helvetica", 20), bg="#ffffff", width=6, relief="sunken")
    display.pack(pady=10)

    btn_frame = tk.Frame(pad, bg="#f0f0f0")
    btn_frame.pack()

    delete_btn = tk.Button(btn_frame, text="←", font=("Helvetica", 14), width=4,
                           command=lambda: selected_qty.set(selected_qty.get()[:-1]))
    delete_btn.grid(row=3, column=0, padx=5, pady=5)

    for i in range(1, 10):
        btn = tk.Button(btn_frame, text=str(i), font=("Helvetica", 14), width=4,
                        command=lambda n=i: selected_qty.set(selected_qty.get() + str(n)))
        btn.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)

    btn0 = tk.Button(btn_frame, text="0", font=("Helvetica", 14), width=4,
                     command=lambda: selected_qty.set(selected_qty.get() + "0"))
    btn0.grid(row=3, column=1, padx=5, pady=5)

    confirm_btn = tk.Button(pad, text="Confirm", font=("Helvetica", 12), bg="#4caf50", fg="white",
                            command=lambda: confirm_quantity(selected_qty, item_name, item_price, pad))
    confirm_btn.pack(pady=10)

    cancel_btn = tk.Button(pad, text="Cancel", font=("Helvetica", 12), bg="#f44336", fg="white",
                           command=pad.destroy)
    cancel_btn.pack(pady=5)

def confirm_quantity(selected_qty, item_name, item_price, pad):
    try:
        qty = int(selected_qty.get())
        if qty <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Quantity", "Please select a valid quantity.")
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

# Update cart
def update_cart_display():
    cart_list.delete(0, tk.END)
    total = 0
    for name, qty, subtotal in cart:
        cart_list.insert(tk.END, f"{qty} x {name} = ₱{subtotal}")
        total += subtotal
    total_label.config(text=f"Total: ₱{total}")

# Checkout
def checkout():
    if not cart:
        messagebox.showinfo("Cart Empty", "Your cart is empty.")
        return

    def ask_order_type():
        choice_window = tk.Toplevel(root)
        choice_window.title("Order Type")
        choice_window.geometry("250x150")
        choice_window.configure(bg="#f0f0f0")
        choice_window.grab_set()

        tk.Label(choice_window, text="Select Order Type", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)

        def set_order_type(mode):
            show_receipt(mode)
            choice_window.destroy()

        tk.Button(choice_window, text="Dine In", font=("Helvetica", 12), width=10, command=lambda: set_order_type("Dine In")).pack(pady=5)
        tk.Button(choice_window, text="Take Out", font=("Helvetica", 12), width=10, command=lambda: set_order_type("Take Out")).pack(pady=5)

    def show_receipt(order_mode):
        receipt = "\n".join([f"{qty}x {name}" for name, qty, _ in cart])
        total = sum(total for _, _, total in cart)
        messagebox.showinfo("Receipt", f"Your order:\n{receipt}\n\nTotal: ₱{total}\nOrder Type: {order_mode}\n\nThank you!")
        cart.clear()
        update_cart_display()

    ask_order_type()

#Cart Functions
def delete_cart_item(index, window):
    item_name, qty, _ = cart[index]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {qty} x {item_name}?")
    if confirm:
        del cart[index]
        update_cart_display()
        window.destroy()
        manage_cart()

def edit_cart_item(index, window):
    item_name, _, _ = cart[index]
    item_price = next(price for name, price in Fish.values() if name == item_name)
    window.destroy()
    show_quantity_pad_edit(item_name, item_price, index)

def show_quantity_pad_edit(item_name, item_price, index):
    pad = tk.Toplevel(root)
    pad.title("Edit Quantity")
    pad.geometry("400x350")
    pad.configure(bg="#f0f0f0")
    pad.grab_set()

    selected_qty = tk.StringVar(value="")

    display = tk.Label(pad, textvariable=selected_qty, font=("Helvetica", 20), bg="#ffffff", width=6, relief="sunken")
    display.pack(pady=10)

    btn_frame = tk.Frame(pad, bg="#f0f0f0")
    btn_frame.pack()

    delete_btn = tk.Button(btn_frame, text="←", font=("Helvetica", 14), width=4,
                           command=lambda: selected_qty.set(selected_qty.get()[:-1]))
    delete_btn.grid(row=3, column=0, padx=5, pady=5)

    for i in range(1, 10):
        btn = tk.Button(btn_frame, text=str(i), font=("Helvetica", 14), width=4,
                        command=lambda n=i: selected_qty.set(selected_qty.get() + str(n)))
        btn.grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)

    btn0 = tk.Button(btn_frame, text="0", font=("Helvetica", 14), width=4,
                     command=lambda: selected_qty.set(selected_qty.get() + "0"))
    btn0.grid(row=3, column=1, padx=5, pady=5)

    def confirm_edit():
        try:
            qty = int(selected_qty.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Please select a valid quantity.")
            return
        new_total = item_price * qty
        cart[index] = (item_name, qty, new_total)
        update_cart_display()
        pad.destroy()

    confirm_btn = tk.Button(pad, text="Confirm", font=("Helvetica", 12), bg="#4caf50", fg="white", command=confirm_edit)
    confirm_btn.pack(pady=10)

    cancel_btn = tk.Button(pad, text="Cancel", font=("Helvetica", 12), bg="#f44336", fg="white", command=pad.destroy)
    cancel_btn.pack(pady=5)

#Manage Cart
def manage_cart():
    if not cart:
        messagebox.showinfo("Cart Empty", "Your cart is empty.")
        return

    cart_window = tk.Toplevel(root)
    cart_window.title("Manage Cart")
    cart_window.geometry("400x300")
    cart_window.configure(bg="#f0f0f0")
    cart_window.grab_set()

    tk.Label(cart_window, text="🛠️ Edit or Delete Items", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=10)

    for index, (name, qty, total) in enumerate(cart):
        frame = tk.Frame(cart_window, bg="#f0f0f0")
        frame.pack(fill='x', padx=10, pady=5)

        tk.Label(frame, text=f"{qty} x {name} = ₱{total}", font=("Helvetica", 11), bg="#f0f0f0").pack(side='left')

        tk.Button(frame, text="Edit", font=("Helvetica", 10), command=lambda i=index: edit_cart_item(i, cart_window)).pack(side='right', padx=5)
        tk.Button(frame, text="Delete", font=("Helvetica", 10), command=lambda i=index: delete_cart_item(i, cart_window)).pack(side='right')
#MAIN MENU GO BACK
def go_back_to_main():
    root.destroy()
    subprocess.Popen(["python", "MAINMENU.py"])

# Main
root = tk.Tk()
back_btn = tk.Button(root, text="← Back", font=("Helvetica", 10), bg="#e57373", fg="white", command=go_back_to_main)
back_btn.pack(anchor='nw', padx=10, pady=5)
root.title("Pastil Kiosk - Fish Menu")
root.geometry("500x650")
root.configure(bg="#f5f5f5")

title_label = tk.Label(root, text="🐟 Fish Menu", font=("Helvetica", 16, "bold"), bg="#f5f5f5")
title_label.pack(pady=10)

menu_frame = tk.Frame(root, bg="#f5f5f5")
menu_frame.pack(pady=5)

for key, (name, price) in Fish.items():
    btn = tk.Button(menu_frame, text=f"{name} - ₱{price}", font=("Helvetica", 12), bg="#e0e0e0",
                    command=lambda k=key: add_to_cart(k))
    btn.pack(fill='x', padx=20, pady=4)

cart_label = tk.Label(root, text="🛒 Your Cart", font=("Helvetica", 14), bg="#f5f5f5")
cart_label.pack(pady=10)

cart_list = tk.Listbox(root, width=40, font=("Helvetica", 11))
cart_list.pack(pady=5)

total_label = tk.Label(root, text="Total: ₱0", font=("Helvetica", 12, "bold"), bg="#f5f5f5")
total_label.pack(pady=5)

checkout_btn = tk.Button(root, text="Checkout", font=("Helvetica", 12), bg="#4caf50", fg="white", command=checkout)
checkout_btn.pack(pady=15)

tk.Button(root, text="Manage Cart", font=("Helvetica", 12), bg="#2196f3", fg="white", command=manage_cart).pack(pady=5)

root.mainloop()