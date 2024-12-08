from pydantic import BaseModel, Field

class PasswordRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пароля")
    user_id: int = Field(..., description="ID пользователя")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль от 5 до 50 символов")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    login: str = Field(..., description="Имя пользователя")
    url: str = Field(..., description="URL портала для пароля")

class PasswordList(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пароля")
    user_id: int = Field(..., description="ID пользователя")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    login: str = Field(..., description="Имя пользователя")
    url: str = Field(..., description="URL портала для пароля")

class PasswordCreate(BaseModel):
    password: str = Field(..., min_length=5, max_length=50, description="Пароль от 5 до 50 символов")
    login: str = Field(..., description="Имя пользователя")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    url: str = Field(..., description="URL портала для пароля")


class PasswordUpdate(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пароля")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль от 5 до 50 символов")
    login: str = Field(..., description="Имя пользователя")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    url: str = Field(..., description="URL портала для пароля")
