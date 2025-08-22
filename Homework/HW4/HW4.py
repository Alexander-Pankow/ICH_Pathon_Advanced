# то что было в HW3

from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///HW4.db')

Base = declarative_base()
Session = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="products")

    def __str__(self):
        return f'{self.id=}; {self.name=}; {self.price=}'

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")

    def __str__(self):
        return f'{self.id=}; {self.name=}; {self.description=}'

Base.metadata.create_all(engine)

#HW4

"""
Задача 1: Наполнение данными
Добавьте в базу данных следующие категории и продукты
Добавление категорий: Добавьте в таблицу categories следующие категории:

Название: "Электроника", Описание: "Гаджеты и устройства."
Название: "Книги", Описание: "Печатные книги и электронные книги."
Название: "Одежда", Описание: "Одежда для мужчин и женщин."

Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с соответствующей категорией:

Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда

Задача 2: Чтение данных
Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.

Задача 3: Обновление данных
Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.

Задача 4: Агрегация и группировка
Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.

Задача 5: Группировка с фильтрацией
Отфильтруйте и выведите только те категории, в которых более одного продукта.
"""

# хотел у вас уточнить по поводу записи "with Session.begin() as session:"
# нашел в интернете, что можно так писать что бы не прописывать комит в конце
# если требуется ни только чтение, это правильно или нет?

from sqlalchemy import func

#1

with Session.begin() as session:
    cat_electronics = Category(name="Электроника", description="Гаджеты и устройства.")
    cat_books = Category(name="Книги", description="Печатные книги и электронные книги.")
    cat_clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")

    session.add_all([cat_electronics, cat_books, cat_clothes])

    products = [
        Product(name="Смартфон", price=299.99, in_stock=True, category=cat_electronics),
        Product(name="Ноутбук", price=499.99, in_stock=True, category=cat_electronics),
        Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=cat_books),
        Product(name="Джинсы", price=40.50, in_stock=True, category=cat_clothes),
        Product(name="Футболка", price=20.00, in_stock=True, category=cat_clothes),
    ]

    session.add_all(products)

#2

with Session() as session:
    categories = session.query(Category).all()
    for category in categories:
        print(f"Category: {category.name}")
        for product in category.products:
            print(f"  - {product.name} : {product.price}")

#3

with Session.begin() as session:
    smartphone = session.query(Product).filter(Product.name == "Смартфон").first()
    if smartphone:
        print(f"Old price: {smartphone.price}")
        smartphone.price = 349.99
        print(f"New price: {smartphone.price}")


#4

with Session() as session:
    counts = session.query(
        Category.name, func.count(Product.id).label("total_products")
    ).join(Product).group_by(Category.name).all()

    for name, total in counts:
        print(f"Category: {name}, Products: {total}")

#5

with Session() as session:
    filtered = session.query(
        Category.name, func.count(Product.id).label("total_products")
    ).join(Product).group_by(Category.name).having(func.count(Product.id) > 1).all()

    for name, total in filtered:
        print(f"Category: {name}, Products: {total}")

