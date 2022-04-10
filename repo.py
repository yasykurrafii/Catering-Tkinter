from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import Enum, delete, update
import datetime

from fastapi import HTTPException

import models
import schema

class UserRepo:

    def fetch_all(db : Session):
        return db.query(models.User).all()

    def fetch_role(db : Session, role_id : int):
        db_item = db.query(models.Role).filter(models.Role.id == role_id).first()
        return db_item

    async def create(db : Session, user : schema.UserCreate):
        if UserRepo.fetch_all(db = db) is None:
            ids = 1
        else:
            ids = len(UserRepo.fetch_all(db = db)) + 1

        db_user = models.User(
            id = ids,
            username = user.username,
            password = user.password,
            role_id = user.role_id,
        )
        db_user.role = UserRepo.fetch_role(db = db, role_id = user.role_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def fetch_info(db : Session, id : int):
        db_item = db.query(models.User).options(joinedload(models.User.role)).filter(models.User.id == id).first()
        
        return db_item

    def user_login(db : Session, user : schema.UserLogin):
        db_item = db.query(models.User).filter(models.User.username == user.username).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="User not found")
        if db_item.password != user.password:
            raise HTTPException(status_code=404, detail="Password not match")
        return UserRepo.fetch_info(db = db, id = db_item.id)

class CategoryInventory:
    def fetch_all(db : Session):
        return db.query(models.CategoryInventory).all()
    
    def fetch_all_distinct(db : Session):
        distinc = db.query(models.CategoryInventory).distinct(models.CategoryInventory.name_category).all()
        item = [x.name_category for x in distinc]
        return item

    async def create(db :Session, item : schema.CategoryInventory):
        if CategoryInventory.fetch_all(db = db) is None:
            ids = 1
        else:
            ids = len(CategoryInventory.fetch_all(db = db)) + 1

        if item.name_category in CategoryInventory.fetch_all_distinct(db):
            raise HTTPException(status_code=400, detail="Category already exist")

        db_item = models.CategoryInventory(
            id = ids,
            name_category = item.name_category
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return "Category has created"

class Inventory:

    def fetch_id(db : Session, name_inventory:str):
        name_inventory = name_inventory.lower()
        db_item = db.query(models.Inventory).filter(models.Inventory.name_ingredient == name_inventory).first()
        return db_item.id

    def fetch_all(db : Session):
        return db.query(models.Inventory).options(joinedload(models.Inventory.relation_category)).all()

    def fetch_ingredient(db : Session, ingredient_id : int):
        db_item = db.query(models.Inventory).filter(models.Inventory.id == ingredient_id).first()
        return db_item
    
    def counting_all(item : List[schema.Ingredient], jumlah : int,db:Session):
        for i in item:
            db_item = Inventory.fetch_id(db = db, name_inventory = i.name_ingredient)
            db_item = Inventory.fetch_ingredient(db = db, ingredient_id = db_item)
            print(i)
            if i[1] * jumlah > db_item.jumlah_inventory:
                raise HTTPException(status_code=404, detail="Jumlah ingredient tidak cukup")

    async def create(db : Session, invent : schema.Inventory):
        if Inventory.fetch_all(db = db) is None:
            id = 1
        else:
            id = len(Inventory.fetch_all(db = db)) + 1

        name_ingredient = invent.name_ingredient.lower()
        db_item = models.Inventory(
            id = id,
            name_ingredient = name_ingredient,
            jumlah_inventory = invent.jumlah_inventory,
            satuan_inventory = invent.satuan_inventory,
            jenis_inventory = invent.jenis_inventory,
            category_inventory = invent.category_inventory,
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    async def update_item(db : Session, invent_id : int, item : schema.InventoryUpdate):
        db_item = db.query(models.Inventory)\
            .filter(models.Inventory.id == invent_id).first()
        db_item.jumlah_inventory += item.jumlah_inventory
        db.commit()
        db.refresh(db_item)
        return db_item

class Menu:

    def fetch_all(db : Session):
        return db.query(models.Menu)\
            .options(joinedload(models.Menu.inventorys)\
                .options(joinedload(models.Ingredients.inventory)))\
            .all()

    def fetch_name(db : Session, name_menu : str):
        db_item = db.query(models.Menu).filter(models.Menu.name_menu == name_menu).first()
        return db_item

    def fetch_ingredients(db : Session, id_menu : int):
        db_item = db.query(models.Ingredients.id_inventory,
                    models.Ingredients.jumlah_ingredient,
                    models.Ingredients.satuan_ingredient,
                    models.Inventory.name_ingredient).join(models.Inventory)\
            .filter(models.Ingredients.id_menu == id_menu).all()
        # slicing = int(len(db_item) / 2)
        # db_item = db_item[:slicing]
        return db_item

    def fetch_info(menu_id : int, db :Session):
        db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        db_menu.inventory = Menu.fetch_ingredients(db = db, id_menu = menu_id)
        return db_menu

    def counting_ingredient(item : List[schema.MenuBase], db : Session, jumlah : int):
        for i in item:
            db_item = Menu.fetch_name(db = db, name_menu = i.name_menu)
            menu = Menu.fetch_info(db = db, menu_id = db_item.id)
            Inventory.counting_all(item = menu.inventory, db = db, jumlah = jumlah)
            
    async def create(db : Session, menu : schema.Menu):
        if Menu.fetch_all(db = db) is None:
            menu.id = 1
        else:
            menu.id = len(Menu.fetch_all(db = db)) + 1

        for i in menu.inventory:
            ids = Inventory.fetch_id(db = db, name_inventory = i.name_ingredient)
            if ids is None:
                raise HTTPException(status_code=404, detail="Ingredient not in inventory")
            i.id_inventory = ids

        menu.name_menu = menu.name_menu.lower()

        db_menu = models.Menu(
            id = menu.id,
            name_menu = menu.name_menu
        )

        db.add(db_menu)
        db.commit()

        for i in menu.inventory:
            db_item = models.Ingredients(
                id_inventory = i.id_inventory,
                id_menu = menu.id,
                jumlah_ingredient = i.jumlah_ingredient,
                satuan_ingredient = i.satuan_ingredient
            )
            db.add(db_item)
            db.commit()

        return "Menu has created"

    async def update(db : Session, menu_id : int, menu : schema.MenuUpdate):
        db_item = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
        db_item.name_menu = menu.name_menu
        db_item.last_updated = datetime.datetime.now().date()
        
        for i in menu.inventory:
            db_invent = db.query(models.Ingredients)\
                .filter(models.Ingredients.id_menu == menu_id)\
                .all()
            invent_id = Inventory.fetch_id(db = db, name_inventory = i.name_ingredient)
            for j in db_invent:
                if j.id_inventory == invent_id:
                    j.jumlah_ingredient = i.jumlah_ingredient
                    db.commit()
        db_item = Menu.fetch_info(menu_id = db_item.id, db = db)
        db.refresh(db_item)
        return db_item

class PesananRepo:

    def fetch_all(db : Session):
        db_item = db.query(models.Pesanan).options(joinedload(models.Pesanan.menu)).all()
        return db_item
        
    def fetch_by_id(db : Session, id : int):
        return db.query(models.Pesanan).options(joinedload(models.Pesanan.menu)).filter(models.Pesanan.id == id).first()

    async def delete(db: Session, pesanan_id : int):
        if PesananRepo.fetch_by_id(db = db, id = pesanan_id) is None:
            return HTTPException(status_code = 404, detail = "Pesanan tidak ada di database")
        db.query(models.PesananMenu).filter(models.PesananMenu.id_pesanan == pesanan_id).delete()
        db.query(models.Pesanan).filter(models.Pesanan.id == pesanan_id).delete()
        db.commit()
        return "pesanan has been deleted"

    async def create(db : Session, item : schema.PesananCreate):
        if PesananRepo.fetch_all(db = db) is None:
            ids = 1
        else:
            ids = len(PesananRepo.fetch_all(db = db)) + 1

        # Checking all ingredient
        Menu.counting_ingredient(item = item.menu, db = db, jumlah = item.jumlah_pesanan)

        db_item = models.Pesanan(
            id = ids,
            nama_PT = item.nama_PT,
            alamat = item.alamat,
            shift = item.shift,
            jumlah_pesanan = item.jumlah_pesanan
        )

        db.add(db_item)
        db.commit()

        for i in item.menu:
            db_pesanan = models.PesananMenu(
                id_menu = Menu.fetch_name(db = db, name_menu = i.name_menu).id,
                id_pesanan = ids,
            )
            db.add(db_pesanan)
            db.commit()

        return db_item

    async def update_menu(id : int,item : schema.PesananUpdate, db : Session):
        db_item = PesananRepo.fetch_by_id(db = db, id = id)
        db_item.update = datetime.datetime.now().date()
        if db_item is None:
            raise HTTPException(status_code = 404, detail = "Pesanan tidak ada di database")
        for menu in db_item.menu:
            if menu.name_menu == item.menu_before:
                id_menu = Menu.fetch_name(db = db, name_menu = item.menu_after).id
                update_db = db.query(models.PesananMenu).filter(models.PesananMenu.id_pesanan == id, models.PesananMenu.id_menu == menu.id).first()
                update_db.id_menu = id_menu
                db.commit()
        db.refresh(db_item)
        db_response = PesananRepo.fetch_by_id(db = db, id = id)
        return db_response

    async def update_status(id : int, item :schema.PesananStatusUpdate, db : Session):
        db_item = PesananRepo.fetch_by_id(db = db, id = id)
        db_item.update = datetime.datetime.now().date()
        if db_item is None:
            raise HTTPException(status_code = 404, detail = "Pesanan tidak ada di database")
        db_item.status_pesanan = item.status_pesanan
        db.commit()
        db.refresh(db_item)
        return db_item

    async def update_jumlah_pesanan(id : int, item : schema.PesananJumlahUpdate, db : Session):
        db_item = PesananRepo.fetch_by_id(db = db, id = id)
        if db_item is None:
            raise HTTPException(status_code = 404, detail = "Pesanan tidak ada di database")
        db_item.jumlah_pesanan = item.jumlah_pesanan
        db.commit()
        db.refresh(db_item)
        return db_item

# class KeuanganRepo:

