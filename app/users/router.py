from fastapi import APIRouter, Response, status
from fastapi.requests import Request
from fastapi.responses import Response, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, PasswordMismatchException,NoEmailsException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth, SUserRegister, EmailModel
from app.email import mail, create_message
from app.config import settings
from app.utils import create_url_safe_token, decode_url_safe_token

"""
    Заметка: tags нужен для документации Swagger
"""
router = APIRouter(prefix="/auth", tags=['Auth'])

templates = Jinja2Templates(directory='app/templates')

@router.get("/", response_class=HTMLResponse, summary="Страница авторизации")
async def get_categories(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    
    if user_data.password != user_data.password_check:
        raise PasswordMismatchException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        name=user_data.name, 
        email=user_data.email,
        hashed_password=hashed_password
    )

    token = create_url_safe_token({"email":user_data.email})

    link = f"http://{settings.DOMAIN}/auth/verify/{token}"

    html_message = f"""
    <h1> Потвердите свой email </h1>
    <p> Пожалуйста перейдите по данной <a href="{link}">ссылке</a> чтобы потвердить свой email<.p>
    """
    message = create_message(
        recipients=[user_data.email],
        subject="Потвердите свой email",
        body=html_message
    )

    await mail.send_message(message)
    
    return {'message': 'Вы успешно зарегистрированы! Потвердите свой email'}

@router.post("/login/")
async def auth_user(response:Response, user_data:SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub":str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token':access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}  

@router.post("/logout/")
async def logout_user(response:Response):
    response.delete_cookie(key="users_access_token")
    return {'message':'Пользователь успешно вышел из системы'}

@router.post('/send_mail')
async def send_mail(emails:EmailModel):
    emails = emails.addresses
    html = "<h1>Добро пожаловать в homepass</h1>"
    message = create_message(
        recipients=emails,
        subject="Добро пожаловать",
        body=html
    )

    await mail.send_message(message)

    return {"message": "Email sent successfully"}

@router.get("/verify/{token}")
async def verify(token:str):
    print(token)
    token_data = decode_url_safe_token(token)
    print(token_data)
    user_email = token_data.get('token_data').get('email')
    print(user_email)
    result = {"error": "Неизвестная ошибка"}

    if user_email:
        user = await UsersDAO.find_one_or_none(email=user_email)
        if not user:
            raise NoEmailsException
    
        result = await UsersDAO.updateIsVerification(user.id)

        if result["status"] == "success":
            return RedirectResponse('/auth', status_code=status.HTTP_303_SEE_OTHER) 
        else:
            return result
        
    return result