from fastapi import status, HTTPException

class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")

class TokenNoFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден")

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")

PasswordMismatchException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пароли не совпадают!")

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль")

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный")

NoUserException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя")

NoEmailsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден пользователь с таким email")

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

UserNotFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User не найден")

PasswordNotFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пароль не найден")