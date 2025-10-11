import tkinter as tk
from chicken import ChickenKiosk
from beef import BeefKiosk
from fish import FishKiosk
from admin import AdminPanel

root = tk.Tk()
root.title("Kiosk")
root.attributes("-fullscreen", True)
root.configure(bg="#282c73")

# --- Functions ---
def open_main_menu():
    welcome_frame.pack_forget()
    main_menu_frame.pack(expand=True, fill="both")

def show_admin():
    welcome_frame.pack_forget()
    admin_panel = AdminPanel(root)
    admin_panel.pack(expand=True, fill="both")

# --- Welcome Frame ---
welcome_frame = tk.Frame(root, bg="#282c73")
welcome_frame.pack(expand=True, fill="both")

center_welcome = tk.Frame(welcome_frame, bg="#282c73")
center_welcome.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    center_welcome,
    text="Welcome!",
    font=("Helvetica", 36, "bold"),
    bg="#282c73",
    fg="white"
).pack(pady=20)

tk.Button(
    center_welcome,
    text="Order Now",
    font=("Helvetica", 16, "bold"),
    width=20,
    height=2,
    bg="white",
    fg="#282c73",
    command=open_main_menu
).pack(pady=10)

# --- Admin Panel Button (bottom-right) ---
admin_button = tk.Button(
    welcome_frame,
    text="👨‍💼 Admin Panel",
    font=("Helvetica", 14, "bold"),
    bg="white",
    fg="#282c73",
    padx=20,
    pady=10,
    bd=0,
    command=show_admin
)
admin_button.place(relx=0.95, rely=0.95, anchor="se")  # bottom-right corner

# --- Main Menu ---
main_menu_frame = tk.Frame(root, bg="#282c73")

center_menu = tk.Frame(main_menu_frame, bg="#282c73")
center_menu.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(center_menu, text="PASTILAN", font=("Helvetica", 48, "bold"),
         bg="#282c73", fg="white").pack(pady=20)
tk.Label(center_menu, text="🍽️ Select a Category 🍽️", font=("Helvetica", 24, "bold"),
         bg="#282c73", fg="white").pack(pady=10)

def show_chicken():
    main_menu_frame.pack_forget()
    chicken_menu = ChickenKiosk(root)
    chicken_menu.pack(expand=True, fill="both")

def show_beef():
    main_menu_frame.pack_forget()
    beef_menu = BeefKiosk(root)
    beef_menu.pack(expand=True, fill="both")

def show_fish():
    main_menu_frame.pack_forget()
    fish_menu = FishKiosk(root)
    fish_menu.pack(expand=True, fill="both")

tk.Button(center_menu, text="🐔 Chicken 🐔", font=("Helvetica", 16, "bold"),
          width=20, height=2, bg="white", fg="#282c73",
          command=show_chicken).pack(pady=15)

tk.Button(center_menu, text="🥩 Beef 🥩", font=("Helvetica", 16, "bold"),
          width=20, height=2, bg="white", fg="#282c73",
          command=show_beef).pack(pady=15)

tk.Button(center_menu, text="🐟 Fish 🐟", font=("Helvetica", 16, "bold"),
          width=20, height=2, bg="white", fg="#282c73",
          command=show_fish).pack(pady=15)

root.mainloop()
