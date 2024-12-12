from app.dao.base import BaseDAO
from app.users.models import User
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def updateIsVerification(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result =  await session.execute(query)
            db_user =  result.scalar_one_or_none()
            if db_user is None:
                return {
                    'message': f"Пользователь с ID {id} не найден.",
                    'status': 'error'
                }
            db_user.is_verified = True
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                return {
                    'message': f"Произошла ошибка при обновлении данных пользователя {str(e)}.",
                    'status': 'error'
                }
            return {
                'message': f"Пользователь с ID {id} успешно верифицирован.",
                'status': 'success'
            }