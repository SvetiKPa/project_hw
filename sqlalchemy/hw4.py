# Задача 2: Чтение данных
# Задача 3: Обновление данных
# # Задача 4: Агрегация и группировка
# Задача 5: Группировка с фильтрацией

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Integer, String, Float, Boolean, ForeignKey, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, joinedload
from pathlib import Path

BASE_DIR: Path = Path(__file__).parent.parent
load_dotenv()
DB_NAME = os.getenv("DB_NAME_HW4")
DB_PATH: Path = BASE_DIR / DB_NAME

engine = create_engine(
    url=f"sqlite:///{DB_PATH}",
    #    echo=True  #!!! ТОЛЬКО В РЕЖИМЕ ОТЛАДКИ!!
)


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

    products: Mapped[list["Product"]] = relationship(
        'Product',
        back_populates='category'
    )


all_categories = [Category(name="Электроника", description="Гаджеты и устройства"),
                  Category(name="Книги", description="Печатные книги и электронные книги"),
                  Category(name="Одежда", description="Одежда для мужчин и женщин"),
                  Category(name="Детская одежда", description="Одежда для детей и подростков")
                  ]
all_products = [Product(name="Смартфон", price=299.99, in_stock=True, category_id=1),
                Product(name="Ноутбук", price=499.99, in_stock=True, category_id=1),
                Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=2),
                Product(name="Джинсы", price=40.50, in_stock=True, category_id=3),
                Product(name="Футболка", price=20.00, in_stock=True, category_id=3)
                ]

Base.metadata.create_all(bind=engine)  #

Session = sessionmaker(bind=engine)
session = Session()
#
for category in all_categories:
    session.add(category)  # add_all(category)

for product in all_products:
    session.add(product)

session.commit()

# Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные
# с ней продукты, включая их названия и цены.
# проблема n+1   #options(joinedload(Category.products))
# классич ничего не присоединяет (нужен только для фильтрации) или перечислять в select(Cat.name)
stmt = (
    select(Category).join(
        Product,
        Product.category_id == Category.id
    ).where(
        Product.price > 30
    ).options(
        joinedload(Category.products)
    )
)
result = session.execute(stmt).scalars().unique().all()

for category in result:
    print(f"Категория: {category.name}")
    for product in category.products:
        print(f"  - Продукт: {product.name}, Цена: {product.price}")

# Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
# filter_by(name="Смартфон")
stmt = select(Product).where(Product.name == "Смартфон")
result = session.execute(stmt).scalar()
if result:
    result.price = 349.99
    session.commit()

# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
stmt = (select(Category.name, func.count(Product.id))
        .join(Product, Category.id == Product.category_id)
        .group_by(Category.name))
result = session.execute(stmt).all()
for row in result:
    print(f"{row.name:<20} - {row.count}")

# Отфильтруйте и выведите только те категории, в которых более одного продукта.
stmt = (select(Category.name, func.count(Product.id))
        .join(Product, Category.id == Product.category_id)
        .group_by(Category.name)
        .having(func.count(Product.id) > 1)
        .order_by(func.count(Product.id).desc())
        )
result = session.execute(stmt).all()
for row in result:
    print(f"Более одного продукта в категории: {row.name:<20} - {row.count}")

session.close()
