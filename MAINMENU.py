import tkinter as tk
import subprocess

def open_chicken():
    subprocess.Popen(["python", "chicken.py"])
    root.destroy()

def open_beef():
    subprocess.Popen(["python", "beef.py"])
    root.destroy()

def open_fish():
    subprocess.Popen(["python", "fish.py"])
    root.destroy()

# Main
root = tk.Tk()
root.title("Pastil Kiosk - Main Menu")
root.geometry("300x300")
root.configure(bg="#f5f5f5")
root.grab_set()

tk.Label(root, text="PASTILAN", font=("Helvetica", 24, "bold"), bg="#f5f5f5").pack(pady=10)
tk.Label(root, text="🍽️ Select a Category", font=("Helvetica", 16, "bold"), bg="#f5f5f5").pack(pady=20)

tk.Button(root, text="🐔 Chicken", font=("Helvetica", 12), width=20, command=open_chicken).pack(pady=5)
tk.Button(root, text="🥩 Beef", font=("Helvetica", 12), width=20, command=open_beef).pack(pady=5)
tk.Button(root, text="🐟 Fish", font=("Helvetica", 12), width=20, command=open_fish).pack(pady=5)

root.mainloop()