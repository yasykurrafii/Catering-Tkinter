import enum
from sqlalchemy import Column, Integer, Enum, String, ForeignKey, Float, Time, Text, Date
from sqlalchemy.orm import relationship

import datetime

from database import Base

# All Enum Class

class EnumRole(str, enum.Enum):
    admin = "admin"
    kitchen = "kitchen"
    packing = "packing"

class EnumSatuanMassa(str, enum.Enum):
    unit = "unit"
    kilogram = "kg"
    pcs = "pcs"
    liter = "liter"

class EnumShift(str, enum.Enum):
    pagi = "pagi"
    siang = "siang"
    malam = "malam"

class EnumStatus(str, enum.Enum):
    pending = "pending"
    cooking = 'cooking'
    packing = 'packing'
    finish = "finish"

class EnumInventJenis(str, enum.Enum):
    kering = "kering"
    basah = "basah"

class EnumInventCat(str, enum.Enum):
    sayuran = "sayuran"
    buah = "buah"
    daging = "daging"
    bumbu_dapur = "bumbu dapur"
    cairan = "cairan"

# User Model

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_role = Column(Enum(EnumRole))

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password = Column(String(256))
    role_id = Column(Integer, ForeignKey("role.id"))
    
    role = relationship("Role", back_populates="users")

# Menu Models

class CategoryInventory(Base):
    __tablename__ = "category_inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_category = Column(String(50))

    inventories = relationship("Inventory", back_populates="relation_category")

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_ingredient = Column(String(50))
    jumlah_inventory = Column(Float)
    satuan_inventory = Column(Enum(EnumSatuanMassa))
    jenis_inventory  = Column(Enum(EnumInventJenis))
    category_inventory  = Column(Integer, ForeignKey("category_inventory.id"))

    relation_category = relationship("CategoryInventory", back_populates="inventories")
    ingredients = relationship("Ingredients", back_populates="inventory")

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_menu = Column(String(100))
    last_update = Column(Date, default=datetime.datetime.now().date())

    inventorys = relationship("Ingredients", back_populates="menu")    
    pesanan = relationship("Pesanan", secondary = 'pesanan_menu',back_populates="menu")

class Ingredients(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_menu = Column(ForeignKey("menu.id"))
    id_inventory = Column(ForeignKey("inventory.id"))
    jumlah_ingredient = Column(Float)
    satuan_ingredient = Column(Enum(EnumSatuanMassa))

    inventory = relationship("Inventory", back_populates="ingredients")
    menu = relationship("Menu", back_populates="inventorys")

# Pesanan
class Pesanan(Base):
    __tablename__ = "pesanan"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama_PT = Column(String(255))
    shift = Column(Enum(EnumShift))
    alamat = Column(Text, default = "")
    status_pesanan = Column(Enum(EnumStatus), default=EnumStatus.pending)
    jumlah_pesanan = Column(Integer)
    update = Column(Date, default = datetime.datetime.now().date())

    menu = relationship("Menu", secondary="pesanan_menu", back_populates="pesanan")

class PesananMenu(Base):
    __tablename__ = "pesanan_menu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_pesanan = Column(ForeignKey("pesanan.id"))
    id_menu = Column(ForeignKey("menu.id"))

class Pemasukan(Base):
    __tablename__ = "pemasukan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jumlah = Column(Integer)
    tanggal = Column(Date, default = datetime.date.today())

class Pengeluaran(Base):
    __tablename__ = 'pengeluaran'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jumlah = Column(Integer)
    tanggal = Column(Date, default = datetime.date.today())
