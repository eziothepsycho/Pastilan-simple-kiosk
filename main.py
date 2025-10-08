import tkinter as tk
import subprocess

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

def open_main_menu():
    app.withdraw()  # 👈 Hide this window instead of destroy
    subprocess.Popen(["python", "mainmenu.py"])

app = tk.Tk()
app.title("Welcome to the Kiosk")
app.attributes("-fullscreen", True)
app.configure(bg="#1e1e1e")

center_frame = tk.Frame(app, bg="#1e1e1e")
center_frame.pack(expand=True)

title_label = tk.Label(center_frame, text="Welcome!", font=("Helvetica", 90),
                       bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20, padx=20)

order_button = tk.Button(center_frame, text="Order Now", command=open_main_menu, **button_style)
order_button.pack(pady=15)

app.mainloop()
