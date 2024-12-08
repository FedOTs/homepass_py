from sqlalchemy import select, and_, or_
from app.dao.base import BaseDAO
from app.passwords.models import Password
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError


class PasswordDAO(BaseDAO):
    model = Password

    @classmethod
    async def get_list(cls, user_id):
        pass_all = await PasswordDAO.find_all(user_id=user_id)
        return pass_all

    @classmethod
    async def update(cls, id, name, login, password, url):
         async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result =  await session.execute(query)
            db_pass =  result.scalar_one_or_none()
            if db_pass is None:
                return {
                    'message': f"Пароль с ID {id} не найден.",
                    'status': 'error'
                }
            db_pass.name = name
            db_pass.login = login
            db_pass.password = password
            db_pass.url = url
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                return {
                    'message': f"Произошла ошибка при обнавлении данных пароля {str(e)}.",
                    'status': 'error'
                }
            return {
                'message': f"Пароль с ID {id} успешно обновлен.",
                'status': 'success'
            }