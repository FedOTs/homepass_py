# Простой "домашний" менеджер паролей

Разработан в связке FastAPI + sqlalchemy

## Настройка

Установите зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

После установки зависимостей сгенерируйте ключ шифрования и добавьте его в app/.env в строку PASSWORD_ENCRYPTION_KEY 

```
python generate_key.py
```

Заполните остальные данные в app/.env (данные БД, JWT токен), пример всех переменных находится а app/.env_example


В данном проекте используется СУБД [PostgreSQL](https://www.postgresql.org/).

Запустите проект

```
uvicorn app.main:app