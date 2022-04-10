import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import datetime

import features

TITLE = "Catering"

class Kitchen(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.geometry("1800x720") 
        self.style = ttk.Style(self)
        self.configure(bg="#F5F7F9")
        self.time = datetime.datetime.now().time()
        self.shift = "Pagi"

        self._menu_list = ["Dashboard"]

        self.style.configure(".", background="#FFFFFF")

        features.Profile("Kitchen")
        features.Thumbnail()
        features.Menu(self._menu_list)
        features.KitchenContent()

app = Kitchen()
app.mainloop()
