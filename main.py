from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database import get_db, engine
import models
import schema
from repo import *
from sqlalchemy.orm import Session
import uvicorn
from fastapi.encoders import jsonable_encoder

from typing import List, Optional

import string
import random

import func

app = FastAPI(title="Abygail Catering",
              description="Abygail Catering API",
              version="1.0.0")

models.Base.metadata.create_all(bind = engine)

@app.exception_handler(Exception)
def validation_exception(request, err):
    base_error_message = f"Failed to execute : {request.method} : {request.url}"
    return JSONResponse(status_code = 400, content = {"message" : f"{base_error_message}. Detail : {err}"})

# User

@app.post("/user/", tags = ["User"], response_model = schema.User)
async def create_user(item_request : schema.UserCreate, db : Session = Depends(get_db)):
    item_request.password = func.encrypt(item_request.password)
    return await UserRepo.create(db = db, user = item_request)

@app.get("/user/", tags = ["User"], response_model = schema.User)
def get_user(user_id : int, db : Session = Depends(get_db)):
    return UserRepo.fetch_info(db = db, id = user_id)

@app.post("/user/login/", tags = ["User"], response_model = schema.User)
async def login_user(item : schema.UserLogin, db : Session = Depends(get_db)):
    return UserRepo.user_login(db = db, user = item)

# Inventory

@app.post("/inventory/category/", tags = ["Inventory"])
async def category_inventory(item : schema.CategoryInventory, db :Session = Depends(get_db)):
    return await CategoryInventory.create(db = db, item = item)

@app.post("/inventory/" , tags = ["Inventory"], response_model = schema.InventoryPost)
async def create_inventory(item : schema.InventoryPost, db : Session = Depends(get_db)):
    return await Inventory.create(db = db, invent = item)

@app.get("/inventory/", tags = ["Inventory"], response_model = List[schema.Inventory])
def fetch_inventory(db : Session = Depends(get_db)):
    return Inventory.fetch_all(db = db)

@app.patch("/inventory/edit/{id}", tags = ["Inventory"])
async def update_inventory(id : int, item : schema.InventoryUpdate,db : Session = Depends(get_db)):
    # values = {"jumlah_inventory" : jumlah_inventory, "satuan_inventory" : satuan_inventory}
    return await Inventory.update_item(db = db, invent_id=id, item = item)

# Menu

@app.post("/menu/" , tags = ["Menu"])
async def create_menu(item_request : schema.Menu, db : Session = Depends(get_db)):
    if Menu.fetch_name(db = db, name_menu = item_request.name_menu) is not None:
            raise HTTPException(status_code=404, detail="Menu has been created")
    return await Menu.create(db = db, menu = item_request)

@app.get("/menu/{menu_id}", tags = ["Menu"])
def fetch_menu(menu_id : int, db : Session = Depends(get_db)):
    return Menu.fetch_info(db = db, menu_id = menu_id)

@app.get("/menu/", tags = ["Menu"])
def fetch_all_menu(db : Session = Depends(get_db)):
    return Menu.fetch_all(db = db)

@app.patch("/menu/edit/{menu_id}", tags = ["Menu"], response_model = schema.Menu)
async def edit_menu(menu_id : int,  item : schema.MenuUpdate, db : Session = Depends(get_db)):
    return await Menu.update(db = db, menu_id = menu_id, menu = item)

# Pesanan
@app.post("/pesanan/", tags = ["Pesanan"], response_model = schema.Pesanan)
async def create_pesanan(item_request : schema.PesananCreate, db : Session = Depends(get_db)):
    return await PesananRepo.create(db = db, item = item_request)

@app.get("/pesanan/", tags = ['Pesanan'])
def fetch_all(db : Session = Depends(get_db)):
    return PesananRepo.fetch_all(db = db)

@app.delete("/pesanan/{pesanan_id}", tags = ["Pesanan"])
async def delete_pesanan(pesanan_id : int, db : Session = Depends(get_db)):
    return await PesananRepo.delete(db = db, pesanan_id = pesanan_id)

@app.patch("/pesanan/edit/menu/{pesanan_id}", tags = ["Pesanan"])
async def update_menu(pesanan_id : int, item : schema.PesananUpdate, db : Session = Depends(get_db)):
    return await PesananRepo.update_menu(db = db, id = pesanan_id, item = item)

@app.patch("/pesanan/edit/status/{pesanan_id}", tags = ["Pesanan"])
async def update_status(pesanan_id : int, status : schema.PesananStatusUpdate, db : Session = Depends(get_db)):
    return await PesananRepo.update_status(db = db, id = pesanan_id, item = status)

@app.patch("/pesanan/edit/pesanan/{pesanan_id}", tags = ["Pesanan"])
async def update_pesanan(pesanan_id : int, item : schema.PesananJumlahUpdate, db : Session = Depends(get_db)):
    return await PesananRepo.update_jumlah_pesanan(db = db, id = pesanan_id, item = item)


