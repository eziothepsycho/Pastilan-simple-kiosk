import tkinter as tk
import subprocess

def open_chicken():
    app.withdraw()
    subprocess.Popen(["python", "chicken.py"])

def open_beef():
    app.withdraw()
    subprocess.Popen(["python", "beef.py"])

def open_fish():
    app.withdraw()
    subprocess.Popen(["python", "fish.py"])

button_style = {
    "width": 20,
    "height": 2,
    "font": ("Helvetica", 16),
    "bg": "#3a3a3a",
    "fg": "#ffffff",
    "activebackground": "#555555",
    "activeforeground": "#ffffff",
    "bd": 0
}

app = tk.Tk()
app.title("Pastil Kiosk - Main Menu")
app.attributes("-fullscreen", True)
app.configure(bg="#1e1e1e")

frame = tk.Frame(app, bg="#1e1e1e")
frame.pack(expand=True)

tk.Label(frame, text="PASTILAN", font=("Helvetica", 32, "bold"),
         bg="#1e1e1e", fg="#ffffff").pack(pady=20)

tk.Label(frame, text="🍽️ Select a Category 🍽️", font=("Helvetica", 20, "bold"),
         bg="#1e1e1e", fg="#cccccc").pack(pady=10)

tk.Button(frame, text="🐔 Chicken 🐔", command=open_chicken, **button_style).pack(pady=15)
tk.Button(frame, text="🥩 Beef 🥩", command=open_beef, **button_style).pack(pady=15)
tk.Button(frame, text="🐟 Fish 🐟", command=open_fish, **button_style).pack(pady=15)

app.mainloop()
