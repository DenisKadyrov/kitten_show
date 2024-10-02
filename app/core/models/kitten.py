from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Kitten(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    color: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    breed: Mapped[str] = mapped_column(nullable=False)