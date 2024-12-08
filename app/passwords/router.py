from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from app.passwords.dao import PasswordDAO
from app.passwords.schemas import PasswordCreate, PasswordUpdate, PasswordList,  PasswordDelete
from app.users.dependencies import get_current_user
from app.users.models import User
from app.utils import encrypt, decrypt
from app.exceptions import PasswordNotFound

router = APIRouter(prefix='/homepass', tags=['Password'])
templates = Jinja2Templates(directory='app/templates')

# Главная страница
@router.get("/", response_class=HTMLResponse, summary="Passwords Page")
async def get_password_page(request: Request, user_data: User = Depends(get_current_user)):
    return templates.TemplateResponse("homepass.html",
                                      {"request": request , "user": user_data})

@router.get("/get_passwords", response_model=List[PasswordList])
async def get_password(request: Request, user_data: User = Depends(get_current_user)):
    password_all = await PasswordDAO.get_list(user_data.id) or []
    for p in password_all:
        p.login = decrypt(p.login)
        p.url = decrypt(p.url)
        p.password = decrypt(p.password)
    return password_all


@router.post("/add_password", response_model=PasswordCreate)
async def add_password(password: PasswordCreate, current_user: User = Depends(get_current_user)):
    # Add new message to the database
    e_password = encrypt(password.password)
    e_login = encrypt(password.login)
    e_url = encrypt(password.url)
    await PasswordDAO.add(
        user_id=current_user.id,
        password=e_password,
        login=e_login,
        name=password.name,
        url=e_url
    )
    return {'password': '*****' ,'name': password.name, 'login':password.login ,'url':password.url, 'status': 'ok', 'msg': 'Password data saved!'}

@router.put("/update_password_data", response_model=PasswordUpdate)
async def update_password_data(password: PasswordUpdate, current_user: User = Depends(get_current_user)):
    # Add new message to the database
    e_password = encrypt(password.password)
    e_login = encrypt(password.login)
    e_url = encrypt(password.url)
    result = await PasswordDAO.update(
        id=password.id,
        password=e_password,
        login=e_login,
        name=password.name,
        url=e_url
    )
    
    if result['status'] == 'error':
        return {'id':password.id,'password': "*****" ,'name': password.name, 'login':password.login ,'url':password.url, 'status': '400', 'msg': result['message']}
    return {'id':password.id,'password': "*****" ,'name': password.name, 'login':password.login ,'url':password.url, 'status': 'ok', 'msg': 'Password data updated!'}


@router.delete("/delete_password", response_model=PasswordDelete)
async def delete_password(password: PasswordDelete, current_user: User = Depends(get_current_user)):
    # Add new message to the database
    result = await PasswordDAO.delete(
        id=password.id,
        user_id=current_user.id,
    )
    
    if result['status'] == 'error':
        return {'id':password.id, 'status': '400', 'msg': result['message']}
    return {'id':password.id, 'status': 'ok', 'msg': 'Password data updated!'}