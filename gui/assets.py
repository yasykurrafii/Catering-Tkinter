from tkinter import *
from tkinter import ttk


class Text(ttk.Label):
    def __init__(self, root,text, fontSize, x, y,weight = "normal", color = None):
        super().__init__(root, text = text)
        self.configure(font=("Inter", fontSize, weight))
        if color:
            self.configure(foreground = color)
        self.place(x = x, y = y)

class TextBox(ttk.Entry):
    def __init__(self, root, x, y, width, height, placeholder, style = "entry", password = False):
        super().__init__(root)
        self.style = ttk.Style()
        self.configure(font = ("Inter", 16))

        self.style_mode = {
            "entry": "EntryStyle.TEntry",
            "filled" : "TEntry"
            }

        self.style.configure("EntryStyle.TEntry", foreground = "#BDBDBD", fieldbackground = "#F8FAFB")
        self.style.configure("TEntry", fieldbackground = "#F8FAFB")
        self['style'] = self.style_mode[style]

        if password:
            self.configure(show = "*")

        self.placeholder = placeholder
        self.insert(0, placeholder)

        self.bind("<Button-1>", self.click)
        self.bind("<FocusOut>", self.leave)

        self.place(x = x, y = y, width = width, height = height)

    def click(self, *args):
        if self['style'] == "EntryStyle.TEntry":
            self.delete(0, 'end')
            self['style'] = "TEntry"

    def leave(self,*args):
        if not self.get():
            self.insert(0, self.placeholder)
            self['style'] = "EntryStyle.TEntry"
  
class ButtonToggle(ttk.Button):

    def __init__(self,root, x, y, w, h, label, photo = None, active = "active", **kwargs):
        super().__init__(root, text = label, **kwargs)
        self.style = ttk.Style()
        self.active = active
        self.font = ("Inter", 16)

        self.style.configure("Active.TButton", font = self.font, relief = 'flat')
        self.style.configure("Inactive.TButton", font = self.font, relief = 'flat')
        self.style.configure("Menu.TButton", font = self.font, relief = 'flat', anchor = W, padding = [40,0,0,0])
        self.style.configure('TButton', background = "#F5F7F9", foreground = "#65666F", font = self.font, relief = 'flat', anchor = W, padding = [40,0,0,0])
        self.style.configure("EditButton.TButton", font =  ("Inter", 13), relief = 'flat', anchor = "center", padding = [0,0,10,0])

        self.style.map("Active.TButton",
                        foreground=[('!active', '#FFFFFF')],
                        background=[('!active', '#0860FB'),('active', "#C4C4C4")])
        self.style.map("Inactive.TButton",
                        foreground=[('!active', '#FFFFFF')],
                        background=[('!active', '#C4C4C4')])
        self.style.map("Menu.TButton",
                        foreground=[('!active', '#65666F'),("active", "#65666F")],
                        background=[('!active', '#FFFFFF'), ("active", "#F5F7F9")])

        self.style.map("EditButton.TButton",
                        foreground=[('!active', '#FFFFFF'),("active", "#65666F")],
                        background=[('!active', '#C4C4C4'), ("active", "#F5F7F9")]
                    )
                    

        self.menu_dict = {
            "active" : "Active.TButton",
            "inactive" : "Inactive.TButton",
            "menu" : "Menu.TButton",
            "focus" : "TButton",
            "edit" : "EditButton.TButton"
        }

        self['style'] = self.menu_dict[self.active]

        if photo is not None:
            self.photo = PhotoImage(file = photo)
            self.configure(image = self.photo, compound=LEFT)
        
        self.place(x = x, y = y, width = w, height = h)

class Image(ttk.Label):
    def __init__(self, x, y, w, h, file_photo):
        super().__init__()
        self.photo = PhotoImage(file = file_photo)
        self.configure(image = self.photo)
        self.place(x = x, y = y, width = w, height = h)

class TableContent(ttk.Treeview):

    def __init__(self,root, x, y, w, h, header, width, anchor, command, scrollbar = True):
        super().__init__(root)
        if scrollbar:
            self.scrollbar = ttk.Scrollbar(self,orient = "vertical", command = self.yview)
            self.scrollbar.pack(side = "right", fill = "y")
        self['columns'] = tuple([str(x + 1) for x in range(len(header))])
        self['show'] = "headings"
        for i in range(len(header)):
            x = i + 1
            self.column(str(x), width = width[i], anchor =anchor[i])
            self.heading(str(x), text = header[i])
            

        self.bind("<ButtonRelease-1>", command)
        self.place(x = 23, y = y, width = w, height = h)

class Dropdown(ttk.OptionMenu):

    def __init__(self, root, x, y, w, h, menu : str,value : list):
        self.menu = StringVar()
        self.menu.set(menu)
        super().__init__(root, self.menu, ())
        self.style = ttk.Style()
        self.style.configure("Dropdown.TLabel", font = ("Inter", 16), borderwidth = 4, relief = "flat", anchor = "center", bordercolor = "red")
        self['style'] = "Dropdown.TLabel"
        self.place(x = x, y = y, width = w, height = h)

        for item in value:
            self["menu"].add_command(label = item,
                                    command = lambda v = item : self.menu.set(v) )

    def get(self):
        return self.menu.get()

class ButtonAdd(ttk.Button):
    
        def __init__(self, root, x, y, w, h):
            super().__init__(root,compound = CENTER)
            self.image1 = "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/Button/Plus.png"
            self.image2 = "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/Button/Minus.png"
            self.style = ttk.Style()
            self.style.configure("ButtonImage.TButton", flat = 'relief')
            self.style.map("ButtonImage.TButton",
                        foreground=[('!active', '#FFFFFF'),("active", "#65666F")],
                        background=[('!active', '#ffffff'), ("pressed","active", "#ffffff")]
                    )
            self.photo1 = PhotoImage(file = r"{}".format(self.image1))
            self.photo2 = PhotoImage(file = r"{}".format(self.image2))
            self.command = ""

            self.x = x
            self.y = y
            self.w = w
            self.h = h

        def add(self):
            self.configure(image = self.photo1,  style = "ButtonImage.TButton")
            self.image = self.photo1
            self.__placing()
        
        def minus(self):
            self.configure(image = self.photo2,  style = "ButtonImage.TButton")
            self.image = self.photo2
            self.__placing()
        
        def add_command(self, *args):
            self.command = self.__combine_funcs(*args)

        def __placing(self):
            self.place(x = self.x, y = self.y, width = self.w, height = self.h)
            self.bind("<Button-1>", self.command)
        
        def __change_icon(self, a):
            if self.image == self.photo1:
                self.configure(image = self.photo2)
                self.image = self.photo2
            else:
                self.configure(image = self.photo1)
                self.image = self.photo1

        def __combine_funcs(self,*funcs):
            def combined_func(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combined_func

        def change_function(self, *func):
            self.command = self.__combine_funcs(*func)
            self.bind("<Button-1>", self.command)
        
        def destroying(self):
            self.destroy()

        def updating_place(self,y):
            self.place(x = self.x, y = y, width = self.w, height = self.h)
