from datetime import time, date
from pydantic import BaseModel

from typing import List, Optional

# User Schema

class Role(BaseModel):
    id : int
    name_role : str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username : str
    
class UserCreate(UserBase):
    role_id : int
    password : str

class UserLogin(UserBase):
    password : str

    class Config:
        orm_mode = True

class User(UserBase):
    role_id : int

class User(UserBase):
    id : int
    role : Role

    class Config:
        orm_mode = True

# Menu Schema

class CategoryInventory(BaseModel):
    id : int
    name_category : str

    class Config:
        orm_mode = True

class InventoryBase(BaseModel):
    name_ingredient : str
    jumlah_inventory : int
    satuan_inventory : str
    jenis_inventory : str
    category_inventory : int

class Inventory(InventoryBase):
    relation_category : CategoryInventory
    
    class Config:
        orm_mode = True

class InventoryPost(InventoryBase):
    pass

    class Config:
        orm_mode = True

class InventoryUpdate(BaseModel):
    jumlah_inventory : float

    class Config:
        orm_mode = True

class IngredientBase(BaseModel):
    name_ingredient : str
    jumlah_ingredient :float
    satuan_ingredient : str

class Ingredient(IngredientBase):
    id_inventory : int

    class Config:
        orm_mode = True

class MenuBase(BaseModel):
    name_menu : str

class Menu(MenuBase):
    id : int
    inventory : List[Ingredient]

    class Config:
        orm_mode = True

class MenuUpdate(BaseModel):
    name_menu : str
    inventory : List[Ingredient]

    class Config:
        orm_mode = True

# Pesanan Schema
class PesananBase(BaseModel):
    nama_PT : str
    alamat : str
    shift : str

class PesananCreate(PesananBase):
    menu : List[MenuBase]
    jumlah_pesanan : int

    class Config:
        orm_mode = True

class Pesanan(PesananBase):
    status_pesanan : str = "pending"

    class Config:
        orm_mode = True

class PesananUpdate(BaseModel):
    menu_before : str
    menu_after : str

class PesananStatusUpdate(BaseModel):
    status_pesanan : str

class PesananJumlahUpdate(BaseModel):
    jumlah_pesanan : int

class LoggingKeuanganBase(BaseModel):
    jumlah : int

class Keuangan(LoggingKeuanganBase):
    tanggal : date

    class Config:
        orm_mode = True



