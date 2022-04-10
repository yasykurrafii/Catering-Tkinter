import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import assets

TITLE = "Catering"

class Login(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.geometry("1800x720") 
        self.style = ttk.Style(self)
        self.configure(bg="#FFFFFF")

        self.style.configure(".", background="#FFFFFF")

        assets.Text(self,"Selamat Datang!", 34, 1208, 179, weight = "bold")

        assets.Text(self,"Ketik Username dan Password untuk masuk", 16, 1208, 236, color = "#65666F")

        assets.Text(self,"Username", 16, 1208, 288, color = "#2B2A2A")
        assets.Text(self,"Password", 16, 1208,374, color = "#2B2A2A")

        self.username = assets.TextBox(1208, 318,420, 36, "Username")

        self.password = assets.TextBox(1208, 405, 420,36, "Password", password = True)


        # Button
        assets.ButtonToggle(self,1208, 502, 420, 40, self.clicked_button, "Login", active = "active")


    def clicked_button(self):
        showinfo(title="Login", message="Login Successful")

app = Login()
app.mainloop()