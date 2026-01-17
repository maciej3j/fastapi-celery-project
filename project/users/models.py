from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from project.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    def __init__(self, username, email, *args, **kwargs) -> None:
        self.username = username
        self.email = email
