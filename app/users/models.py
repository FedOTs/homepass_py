from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base
from app.passwords.models import Password

class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    passwords = relationship(
        "Password",
        back_populates="user",
        cascade="all, delete-orphan"
    )

