from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from app.passwords.dao import PasswordDAO
from app.passwords.schemas import PasswordCreate, PasswordRead, PasswordUpdate, PasswordList
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix='/homepass', tags=['Password'])
templates = Jinja2Templates(directory='app/templates')

# Главная страница
@router.get("/", response_class=HTMLResponse, summary="Passwords Page")
async def get_password_page(request: Request, user_data: User = Depends(get_current_user)):
    return templates.TemplateResponse("homepass.html",
                                      {"request": request , "user": user_data})

@router.get("/get_passwords", response_model=List[PasswordList])
async def get_password(request: Request, user_data: User = Depends(get_current_user)):
    return await PasswordDAO.get_list(user_data.id) or []


@router.post("/add_password", response_model=PasswordCreate)
async def add_password(password: PasswordCreate, current_user: User = Depends(get_current_user)):
    # Add new message to the database
    await PasswordDAO.add(
        user_id=current_user.id,
        password=password.password,
        login=password.login,
        name=password.name,
        url=password.url
    )
    
    return {'password': '*****' ,'name': password.name, 'login':password.login ,'url':password.url, 'status': 'ok', 'msg': 'Password data saved!'}

@router.put("/update_password_data", response_model=PasswordUpdate)
async def update_password_data(password: PasswordUpdate, current_user: User = Depends(get_current_user)):
    # Add new message to the database
    print(password)
    result = await PasswordDAO.update(
        id=password.id,
        password=password.password,
        login=password.login,
        name=password.name,
        url=password.url
    )
    
    if result['status'] == 'error':
        return {'id':password.id,'password': password.password ,'name': password.name, 'login':password.login ,'url':password.url, 'status': '400', 'msg': result['message']}
    return {'id':password.id,'password': password.password ,'name': password.name, 'login':password.login ,'url':password.url, 'status': 'ok', 'msg': 'Password data updated!'}