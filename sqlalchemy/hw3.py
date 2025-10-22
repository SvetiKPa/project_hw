# Задача 3: Определите модель продукта Product со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# price: числовое значение с фиксированной точностью
# in_stock: логическое значение
# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# description: строка (макс. 255 символов

from sqlalchemy import create_engine, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
# from typing import Optional


engine = create_engine("sqlite:///:memory:",  echo=True)

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

class Product(Base):
    __tablename__ = 'products'
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('categories.id'))

    category: Mapped["Category"] = relationship(
        'Category',
        back_populates='products'
    )


class Category(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    product: Mapped[list["Product"]] = relationship(
        'Product',
        back_populates='category'
    )



Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()



