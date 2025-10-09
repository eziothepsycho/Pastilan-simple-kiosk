import tkinter as tk
from chicken import ChickenKiosk
from beef import BeefKiosk     
from fish import FishKiosk     

root = tk.Tk()
root.title("Kiosk")
root.attributes("-fullscreen", True)
root.configure(bg="#282c73")

# --- Welcome Frame ---
welcome_frame = tk.Frame(root, bg="#282c73")
welcome_frame.pack(expand=True)

tk.Label(welcome_frame, text="Welcome!", font=("Helvetica", 90),
         bg="#282c73", fg="white").pack(pady=20)

def open_main_menu():
    welcome_frame.pack_forget()
    main_menu_frame.pack(expand=True)

tk.Button(welcome_frame, text="Order Now", font=("Helvetica", 16),
          width=20, height=2, bg="white", fg="#282c73",
          command=open_main_menu).pack(pady=20)

# --- Main Menu ---
main_menu_frame = tk.Frame(root, bg="#282c73")
tk.Label(main_menu_frame, text="PASTILAN", font=("Helvetica", 48, "bold"),
         bg="#282c73", fg="white").pack(pady=20)
tk.Label(main_menu_frame, text="🍽️ Select a Category 🍽️", font=("Helvetica", 24, "bold"),
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

tk.Button(main_menu_frame, text="🐔 Chicken 🐔", font=("Helvetica", 16),
          width=20, height=2, bg="white", fg="#282c73",
          command=show_chicken).pack(pady=15)

tk.Button(main_menu_frame, text="🥩 Beef 🥩", font=("Helvetica", 16),
          width=20, height=2, bg="white", fg="#282c73",
          command=show_beef).pack(pady=15)

tk.Button(main_menu_frame, text="🐟 Fish 🐟", font=("Helvetica", 16),
          width=20, height=2, bg="white", fg="#282c73",
          command=show_fish).pack(pady=15)

root.mainloop()
