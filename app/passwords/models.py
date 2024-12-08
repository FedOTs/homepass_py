from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base

class Password(Base):
    __tablename__ = 'passwords'
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User",
        back_populates="passwords"
    )
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    login: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=True)

