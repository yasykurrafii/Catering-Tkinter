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
    def __init__(self, x, y, width, height, placeholder, password = False):
        super().__init__()
        self.style = ttk.Style()
        self.configure(font = ("Inter", 16))

        self.style.configure("EntryStyle.TEntry", foreground = "#BDBDBD", fieldbackground = "#F8FAFB")
        self.style.configure("TEntry", fieldbackground = "#F8FAFB")
        self['style'] = "EntryStyle.TEntry"

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
        
        
