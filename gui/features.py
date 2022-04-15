from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo

import datetime

import assets
import dataAPI

from typing import Optional

data_url = {
            "dashboard" : "http://localhost:8000/pesanan/",
            "anggaran" : "http://localhost:8000/pesanan/",
            "riwayat" : "http://localhost:8000/",
            "menu" : "http://localhost:8000/menu/",
            "inventaris" : "http://localhost:8000/inventory/",
            "perusahaan" : "http://localhost:8000/pesanan/",
}

# Generating Profile Frame
class Profile(ttk.Frame):

    image_file = {
        "admin" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/ProfileAdmin.png",
        "kitchen" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/ProfileKitchen.png",
        "packing" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/ProfilePacking.png"
    }

    current_profile = ""

    def __init__(self, name : str):
        super().__init__()
        self.name = name.lower()
        self.image = Profile.image_file[self.name]

        Profile.current_profile = self.name

        assets.Text(self, "hello,", 12, 70, 16, color="#65666F")
        assets.Text(self, name.upper(), 20, 70,35, weight="bold", color="#2B2A2A")
        assets.Image(10,16, 50,50, self.image)

        self.place(x=0,y=0, width = 296, height = 90)

# Generating Thumbnail Frame
class Thumbnail(ttk.Frame):

    current_menu = "Dashboard / "
    menu_dir = ""

    def __init__(self):
        super().__init__()

        self.time = datetime.datetime.now().time()
        self.shift = "Pagi"

        self._checking_time()
        self._checking_profile()

        self.menu_dir = assets.Text(self, Thumbnail.current_menu, 12, 34, 50, color="#65666F")
        Thumbnail.menu_dir = self.menu_dir
        assets.Text(self, "Current Shift,", 16, 1300, 24, color = "#65666F")
        assets.Text(self, self.shift, 16, 1300, 53, color = "#000000", weight = "bold")

        self.place(x=300,y=0, width = 1500, height =90)

    def _checking_time(self):
        time_1 = datetime.datetime.strptime("07:00AM", "%I:%M%p").time()
        time_2 = datetime.datetime.strptime("01:00PM", "%I:%M%p").time()
        time_3 = datetime.datetime.strptime("03:00PM", "%I:%M%p").time()
        time_4 = datetime.datetime.strptime("06:00PM", "%I:%M%p").time()

        if self.time >=  time_1 and self.time <= time_2:
            self.shift = "Pagi"
        elif self.time >= time_2 and self.time <= time_3:
            self.shift = "Siang"
        elif self.time >= time_3 and self.time <= time_4:
            self.shift = "Sore"
        elif self.time >= time_4:
            self.shift = "Malam"

    def _checking_profile(self):
        if Profile.current_profile == "admin":
            Thumbnail.current_menu = "Dashboard / "
        elif Profile.current_profile == "kitchen":
            Thumbnail.current_menu = "Dashboard / Kitchen "
        elif Profile.current_profile == "packing":
            Thumbnail.current_menu = "Dashboard / Packing "
    
    def refresh_menu_dir(self):
        self.menu_dir.delete(0, END)
        self.menu_dir.insert(0, Thumbnail.current_menu)

# Base For Content
class ContentBase(ttk.Frame):

    def __init__(self):
        super().__init__()
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", foreground = "#65666F", font = ("Inter", 15))
        if Profile.current_profile == "admin":
            self.__current_menu = Menu.current_menu
        else:
            self.__current_menu = Profile.current_profile.title()

        self.place(x = 300, y = 95, width = 1500, height = 621)

    def build(self):
        assets.Text(self, self.__current_menu, 28, 20, 37, weight = "bold", color = "#000000")


"""
Detail Everything Start Here
- Detail in admin
- Detail in Packing
- Detail in Cooking
- etc
"""

class DetailPesananContent(ContentBase):

    def __init__(self, menu :list, nama_perusahaan, jumlah_pack):
        super().__init__()
        self.menu = menu
        self.nama_perusahaan = nama_perusahaan
        self.jumlah_pack = jumlah_pack
        self.start_menu_y = 201

        assets.Text(self, "Nama Perusahaan", 16, 30, 30, color = "#65666F")
        assets.Text(self, self.nama_perusahaan, 20, 30, 70, color = "#2B2A2A", weight = "bold")
        assets.Text(self, "Jumlah Pack", 16, 30, 102, color = "#65666F")
        assets.Text(self, self.jumlah_pack, 20, 30, 129, color = "#2B2A2A", weight = "bold")
        assets.Text(self, "Menu", 16, 30, 174, color = "#65666F")
        for me in self.menu:
            assets.Text(self, me, 20, 62, self.start_menu_y, color = "#2B2A2A", weight = "bold")
            self.start_menu_y += 20
        assets.ButtonToggle(self, 30, 511, 305, 33, "Menu Set Selesai", active = "active")
        self.place(x=1405, y=122, width=380, height=574)

class DetailAdminContent(ContentBase):

    def __init__(self, data : list):
        super().__init__()
        self.data = data
        self.place(x=1405, y=122, width=380, height=574)

    def build_detail_dashboard(self, status : str, alamat : str):
        menu_y = 410
        color = {
            "pending" : "#AB3E00",
            "cooking" : "#7D6200",
            "packing" : "#AB3E00"
        }
        assets.Text(self, "Nama Perusahaan", 16, 30, 30, color = "#65666F")
        assets.Text(self, self.data[1], 20, 30, 60, color = "#2B2A2A", weight = "bold")
        
        assets.Text(self, "Alamat", 16, 30, 112, color = "#65666F")
        assets.Text(self, alamat, 20, 30, 142, color = "#2B2A2A", weight = "bold")
        
        assets.Text(self, "Jumlah Pack", 16, 30, 224, color = "#65666F")
        assets.Text(self, self.data[2], 20, 30, 254, color = "#2B2A2A", weight = "bold")
        
        assets.Text(self, "Status", 16, 30, 304, color = "#65666F")
        assets.Text(self, status.title(), 20, 30, 334, color = color[status], weight = "bold")
        
        assets.Text(self, "Menu", 16, 30, 384, color = "#65666F")
        for i in self.data[3]:
            assets.Text(self, i, 20, 30, menu_y, color = "#2B2A2A", weight = "bold")
            menu_y += 20

    def build_detail_menu(self, item :list, data_full : dict):
        menu_y = 320
        assets.Text(self, "Nama Menu", 16, 30, 30, color = "#65666F")
        assets.Text(self, self.data[1], 20, 30, 70, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Banyak Porsi", 16, 30, 127, color = "#65666F")
        assets.Text(self, self.data[2], 20, 30, 160, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Last Update", 16, 30, 200, color = "#65666F")
        assets.Text(self, self.data[3], 20, 30, 240, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Bahan", 16, 30, 280, color = "#65666F")
        for i in item:
            assets.Text(self, i, 20, 30, menu_y, color = "#2B2A2A", weight = "bold")
            menu_y += 20
        assets.ButtonToggle(self, 30, 503, 305, 41, "Sunting Menu", active = "edit", command = lambda x = None: FormEdit("edit menu", data_full))

    def build_detail_perusahaan(self):
        assets.Text(self, "Nama Perusahaan", 16, 30, 30, color = "#65666F")
        assets.Text(self, self.data[1], 20, 30, 60, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Alamat", 16, 30, 112, color = "#65666F")
        assets.Text(self, self.data[2], 20, 30, 142, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Last Update", 16, 30, 202, color = "#65666F")
        assets.Text(self, self.data[4], 20, 30, 242, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Shift", 16, 30, 302, color = "#65666F")
        assets.Text(self, self.data[3], 20, 30, 342, color = "#2B2A2A", weight = "bold")

        assets.ButtonToggle(self, 30, 453, 305, 41, "Sunting Detail Perusahaan", active = "edit",command = lambda x = None: FormEdit().change_page(x))
        assets.ButtonToggle(self, 30, 503, 305, 41, "Tambah Menu Hari ini", active = "active", command = lambda x = None: FormEdit().change_page(x))

    def build_detail_inventaris(self):
        assets.Text(self, "Nama Produk", 16, 30, 30, color = "#65666F")
        assets.Text(self, self.data[0], 20, 30, 60, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Jenis Produk", 16, 30, 172, color = "#65666F")
        assets.Text(self, self.data[1], 20, 30, 199, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Kategori Produk", 16, 193, 172, color = "#65666F")
        assets.Text(self, self.data[2], 18, 193, 199, color = "#2B2A2A", weight = "bold")

        assets.Text(self, "Jumlah Produk", 16, 30, 254, color = "#65666F")
        assets.Text(self, self.data[3], 20, 30, 284, color = "#2B2A2A", weight = "bold")
        
        assets.ButtonToggle(self, 30, 453, 305, 41, "Sunting", active = "edit",command = lambda x = None: FormEdit().change_page(x))

"""
End In Here
"""


"""
Form Edit Start Here
"""

class FormEdit(ContentBase):

    def __init__(self, page_to, data = None):
        super().__init__()
        self.data = data
        self.page = {"tambah menu" : self.menu_form,
                    "edit menu" : self.menu_form
                    }
        self.title= {"tambah menu" : "Tambah Menu Baru",
                    "edit menu" : "Sunting Menu"}
        self.get_all = []
        self.value = []

        self.page[page_to](self.title[page_to])
        
    def menu_form(self, title):
        assets.Text(self, title, 28, 20, 37, weight = "bold", color = "#000000")
        style = "filled"
        if self.data is None:
            self.data = {"name_menu" : "Nama Menu",
                        "jumlah_porsi" : "Jumlah Porsi",
                        "inventory" : [
                            {"name_ingredient" : "Nama Bahan","jumlah_ingredient" : "Jumlah Bahan", "satuan_ingredient" : "kg"}
                        ]
                        }
            style = "entry"
        x, y = 30,120
        for key, value in self.data.items():
            if key == "inventory":
                add_ing = AddingIngredient(self, value, style)
                add_ing.build(30,250)
                self.get_all.append(add_ing)
                break
            if "_" in key:
                splitting = key.split("_")
                key = " ".join(splitting)
            assets.Text(self, key.title(), 16, x, y, color = "#65666F")
            box = assets.TextBox(self, x + 150, y, 330, 42, value, style)
            self.get_all.append(box)
            y += 70
        self.build_button_batal()
    
    def build_button_batal(self):
        assets.ButtonToggle(self, 800, 120, 305, 41, "Menyimpan", active = "active", command = lambda x = None: self.get_value())

    def get_value(self):
        idx = 0
        for key, _ in self.data.items():
            if key == 'inventory':
                self.data[key] = self.get_all[-1].get_value()
            else:
                self.data[key] = self.get_all[idx].get()
            idx += 1
        print(self.data)

class AddingIngredient:

    def __init__(self, root, inventory, style):
        self.root = root
        self.inventory = inventory
        self.style = style
        self.value_dropdown = ["kg", "liter", "unit", "pcs"]
        self.x = ""
        self.y = ""

        self.empty_data = {"name_ingredient" : "Nama Bahan","jumlah_ingredient" : "Jumlah Bahan", "satuan_ingredient" : "kg"}

        self.text_dict = []
        self.minus_button = None
    
    def build(self, x, y):
        self.x = x + 150
        self.y = y
        assets.Text(self.root, "Bahan Menu", 16, x, y, color = "#65666F")
        self.__build_button()
        if len(self.inventory) > 1 :
            self.__build_button(positive = False)
        for i in self.inventory:
            self.__build_text(i)   
            self.y += 70
        self.style = "entry"

    def get_value(self):
        value = []
        for i in self.text_dict:
            idx = 0
            for key, _ in self.empty_data.items():
                self.empty_data[key] = i[idx].get()
                idx += 1
            value.append(self.empty_data)
        return value

    def __build_button(self, item = None, positive = True):
        if item is None:
            item = self.empty_data
        if positive:
            button = assets.ButtonAdd(self.root, self.x+550,self.y, 100, 42)
            button.add_command(lambda x: self.__add_button(item))
            button.add()
        else:
            button = assets.ButtonAdd(self.root, self.x+650,self.y - 70, 100, 42)
            button.add_command(lambda x : self.__minus_button())
            button.minus()
            self.minus_button = button

    def __build_text(self, item):
        b = assets.TextBox(self.root, self.x + 340, self.y, 100, 42, "1", self.style)
        a = assets.TextBox(self.root, self.x, self.y, 330, 42, item["name_ingredient"], self.style)
        c = assets.Dropdown(self.root,self.x + 450, self.y, 85, 42, item["satuan_ingredient"], self.value_dropdown)
        self.text_dict.append([a,b,c])
        return [a,b,c]

    def __add_button(self, item):
        if self.minus_button is None:
            self.__build_text(item)
            self.__build_button(item, positive = False)
        else:
            self.__build_text(item)
        self.y += 70
    
    def __minus_button(self):
        for i in self.text_dict[-1]:
            i.destroy()
        self.text_dict.pop(-1)
        if len(self.text_dict) < 2:
            self.minus_button.destroy()
            self.minus_button = None
        self.y -= 70




"""
Generate Content Start Here
"""
class KitchenContent(ContentBase):

    def __init__(self):
        super().__init__()
        super().build()
        self.url = "http://localhost:8000/pesanan/"
        self.header = ["id", "Nama Perusahaan", "Jumlah Pack", "Menu"]
        self.width = [70,259,173,259]
        self.anchor = ["c","w","w","w"]

        self.table = assets.TableContent(self, 25, 100, 1057, 510, self.header, self.width, self.anchor, self.__on_click_treeview)

        data = dataAPI.fetch_api(self.url)

        for i in data:
            value = [i["id"],i['nama_PT'], i['jumlah_pesanan']]
            menus = ""
            for menu in i["menu"]:
                menus += menu["name_menu"] + "\n"
            value.append(menus)
            value = tuple(value)
            self.table.insert("", END, values = value)
    
    def __on_click_treeview(self, a):
        curitem = self.table.focus()
        item = self.table.item(curitem)['values']
        menu = item[-1].split("\n")
        DetailPesananContent(menu, item[1], item[2])

class PackingContent(ContentBase):

    def __init__(self):
        super().__init__()
        super().build()
        self.url = "http://localhost:8000/pesanan/"
        self.header = ["id", "Nama Perusahaan", "Jumlah Pack", "Menu", "Visual Packing"]
        self.width = [70,259,173,259, 193]
        self.anchor = ["c","w","w","w", "w"]

        self.table = assets.TableContent(self, 25, 100, 1057, 510, self.header, self.width, self.anchor, self.__on_click_treeview)

        data = dataAPI.fetch_api(self.url)

        for i in data:
            value = [i["id"],i['nama_PT'], i['jumlah_pesanan']]
            menus = ""
            for menu in i["menu"]:
                menus += menu["name_menu"] + "\n"
            value.append(menus)
            value.append("*")
            value = tuple(value)
            self.table.insert("", END, values = value)
    
    def __on_click_treeview(self, a):
        curitem = self.table.focus()
        item = self.table.item(curitem)['values']
        menu = item[3].split("\n")
        DetailPesananContent(menu, item[1], item[2])

class AdminContent(ContentBase):

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.table = ""
        self.data = {}
        self.fetching_data()
        self.status = ""

    def build_dashboard(self):
        assets.Text(self, "Dashboard", 28, 20, 37, weight = "bold", color = "#000000")
        header = ["id", "Nama Perusahaan", "Jumlah Pack", "Menu"]
        width = [70,279,220,299]
        anchor = ["c","w","w","w"]
        item_needed = ["id", "nama_PT", "jumlah_pesanan", "menu"]
        self.table = assets.TableContent(self, 25, 100, 1057, 510, header, width, anchor, self.__on_click_treeview)
        self.__input_data_table(item_needed)

    def build_menu(self):
        assets.Text(self, "Menu", 28, 20, 37, weight = "bold", color = "#000000")
        header = ["id", "Menu", "Banyak Porsi", "Last Update"]
        width = [70,279,220,299]
        anchor = ["c","w","w","w"]
        for x in self.data:
            x['jumlah_porsi'] = 1
        item_needed = ["id", "name_menu", "jumlah_porsi", "last_update"]
        self.table = assets.TableContent(self, 25, 100, 1057, 510, header, width, anchor, self.__on_click_treeview)
        self.__input_data_table(item_needed)
        Form = self.__form_menu()
        tambah_button = assets.ButtonToggle(self, 772, 37, 307, 41, "Tambah Menu", active = "active")
        tambah_button['command'] = lambda x = "tambah menu" : Form.change_page(x)

        # menyimpan = assets.ButtonToggle(self, 772, 37, 307, 41, "Tambah Menu", active = "active")
        # menyimpan['command'] = lambda : Form.get_value()

        # batal = assets.ButtonToggle(self, 772, 37, 307, 41, "Tambah Menu", active = "inactive")
        # tambah_button['command'] = lambda x = "tambah menu" : FormEdit(x)

    def build_perusahaan(self):
        assets.Text(self, "Perusahaan", 28, 20, 37, weight = "bold", color = "#000000")
        header = ["id", "Nama Perusahaan", "Alamat", "Shift", "Last Update"]
        width = [70,259,280,172, 174]
        anchor = ["c","w","w","w", "w"]
        item_needed = ["id", "nama_PT", "alamat", "shift", "update", "jumlah_pesanan"]
        self.table = assets.TableContent(self, 25, 100, 1057, 510, header, width, anchor, self.__on_click_treeview)
        self.__input_data_table(item_needed)

        tambah_button = assets.ButtonToggle(self, 772, 37, 307, 41, "Tambah Perusahaan", active = "active")
        tambah_button['command'] = lambda x = "tambah_menu" : FormEdit().change_page(x)

    def build_inventory(self):
        assets.Text(self, "Inventaris", 28, 20, 37, weight = "bold", color = "#000000")
        header = ["Nama Produk", "Jenis", "Kategori", "Jumlah"]
        width = [193,153,192,173,153]
        anchor = ["w","w","w","w",""]
        for x in self.data:
            x['jumlah_inventory'] = f"{x['jumlah_inventory']} {x['satuan_inventory']}"
            x["category_inventory"] = x["relation_category"]["name_category"]
        item_needed = ["name_ingredient", "jenis_inventory", "category_inventory", "jumlah_inventory"]
        self.table = assets.TableContent(self, 25, 100, 1057, 510, header, width, anchor, self.__on_click_treeview)
        self.__input_data_table(item_needed)

        tambah_button = assets.ButtonToggle(self, 772, 37, 307, 41, "Tambah Inventaris", active = "active")
        tambah_button['command'] = lambda x = "tambah_menu" : FormEdit().change_page(x)

    def build_riwaya(self):
        assets.Text(self, "Riwayat", 28, 20, 37, weight = "bold", color = "#000000")
        header = [ "Nama Perusahaan", "Shift", "Jumlah Pack", "Waktu Selesai"]
        width = [259,173,173,279]
        anchor = ["w","w","w","w", "w"]
        item_needed = ["nama_PT", "shift", "jumlah_pesanan", "update"]
        self.table = assets.TableContent(self, 25, 100, 1057, 510, header, width, anchor, self.__on_click_treeview)
        self.__input_data_table(item_needed)

    def __on_click_treeview(self, a):
        curitem = self.table.focus()
        item = self.table.item(curitem)['values']
        for i in range(len(item)):
            if "\n" in str(item[i]):
                item_split = [x.split("\n") for x in item if "\n" in str(x)]
                split_res = [i[0] for i in item_split]
                item[i] = split_res
        detail = DetailAdminContent(item)
        self.__filter_detail(detail)

    def __input_data_table(self, item_needed : list):
        for item in self.data:
            value = [item[key] for key in item_needed if key != "menu"]
            if "menu" in item_needed:
                menus = ""
                for menu in item["menu"]:
                    menus += menu["name_menu"] + "\n"
                value.append(menus)   
            if Menu.current_menu.lower() == "perusahaan":
                value[3] = f"{value[3].title()} ({value[-1]})"
                value.pop(-1)
            value = tuple(value)
            self.table.insert("", END, values = value)
    
    def __filter_detail(self, item : DetailAdminContent):
        global data_url
        if Menu.current_menu.lower() == 'dashboard':
            self.status = {item['id'] : item['status_pesanan'] for item in self.data}
            id_ = item.data[0]
            status = self.status[id_]
            item.build_detail_dashboard(status, self.data[id_ - 1]['alamat'])
        elif Menu.current_menu.lower() == "menu":
            items = []
            id_ = item.data[0] - 1
            data_id = self.data[id_]
            self.url += f"{id_ + 1}/"
            self.fetching_data()
            data_needed = ["jumlah_ingredient", "satuan_ingredient"]
            for ingredient in data_id['inventorys']:
                bahan_bahan = " ".join(str(ingredient[x]) for x in data_needed)
                bahan_bahan += " " + ingredient["inventory"]["name_ingredient"]
                items.append(bahan_bahan)
            item.build_detail_menu(items, self.data)
        elif Menu.current_menu.lower() == "perusahaan":
            item.build_detail_perusahaan()
        elif Menu.current_menu.lower() == "inventaris" :
            item.build_detail_inventaris()

    def fetching_data(self):
        try:
            self.data = dataAPI.fetch_api(self.url)
        except:
            showinfo("Error", "Koneksi gagal")

    def delete_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def __form_menu(self):
        form = ""
        def changes():
            pass
        def change_page(x):
            form = FormEdit(x)
        
        def get_value():
            form.get_value()

        changes.change_page = change_page
        changes.get_value = get_value
        return changes
"""
End of Generate Content
"""

# Generating Menu Frame
class Menu(ttk.Frame):

    Icon_File = {
        "dashboard" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/icons/Dashboard.png",
        "anggaran" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/icons/Anggaran.png",
        "riwayat" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/icons/History.png",
        "menu" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/icons/Menu.png",
        "inventaris" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/icons/Packing.png",
        "perusahaan" : "/home/yasykur_rafii/coding/kerjaan/Catring Aby/gui/images/icons/Perusahaan.png"
    }

    current_menu = ""

    def __init__(self, title : list):
        super().__init__()
        self.__start_x = 0
        self.__start_y = 70
        self.__width = 296
        self.__height = 40

        self.focus_menu = "Dashboard"
        self.before = ""

        assets.Text(self, "MENU", 12, 34, 39, color="#65666F")
        for i in title:
            if i == self.focus_menu:
                button = assets.ButtonToggle(self, self.__start_x, self.__start_y,
                                    self.__width, self.__height, i, Menu.Icon_File[i.lower()], active = 'focus')
                self.before = button
            else:
                button = assets.ButtonToggle(self, self.__start_x, self.__start_y,
                                self.__width, self.__height, i, Menu.Icon_File[i.lower()], active = "menu")
            button["command"] = self.__on_click_button(button)

            self.__start_y += self.__height
        self.place(x = 0, y = 95, width = 296, height = 621)

    def __on_click_button(self, button : assets.ButtonToggle):
        def on_click():
            self.focus_menu = button["text"]

            if self.focus_menu == "Dashboard":
                Thumbnail.current_menu = "Dashboard / "
                if Profile.current_profile == "kitchen" or Profile.current_profile == "packing":
                    
                    Thumbnail.current_menu = "Dashboard / " + Profile.current_profile.title() + " "
            else:
                Thumbnail.current_menu = "Dashboard / " + self.focus_menu
            Thumbnail.menu_dir.configure(text = Thumbnail.current_menu)

            Menu.current_menu = self.focus_menu

            if Profile.current_profile == "admin":
                self.__choosing_admin_content()
            
            self.before.configure(style = "Menu.TButton")
            self.before = button
            button.configure(style = "TButton")
        
        return on_click

    def __choosing_admin_content(self):
        global data_url
        content = AdminContent(data_url[Menu.current_menu.lower()])
        self.__build_content(content)

    def __build_content(self, content: AdminContent):
        content.delete_frame()
        if Menu.current_menu.lower() == "dashboard":
            content.build_dashboard()
        elif Menu.current_menu.lower() == "menu":
            content.build_menu()
        elif Menu.current_menu.lower() == "perusahaan":
            content.build_perusahaan()
        elif Menu.current_menu.lower() == "inventaris":
            content.build_inventory()
        elif Menu.current_menu.lower() == "riwayat":
            content.build_riwayat()






