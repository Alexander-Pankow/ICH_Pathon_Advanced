from sqlalchemy import func
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

    def __str__(self):
        return f'{self.id=} {self.name=} {self.age=}'


with Session() as session:
    total_ages = session.query(User.name, func.sum(User.age), func.avg(User.age)).group_by(User.name)
    res = total_ages.all()

    for item in res:
        print(*item)

    res = session.query(func.count(User.id)).first()
    res, *_ = res
    print(res)

    res = session.query(func.count(User.id)).scalar()
    print(res)

    res = session.query(User.name, User.age).filter(User.id == 2)
    print(res)

    # Присвоение алиаса выражению подсчета количества пользователей в каждой возрастной группе
    age_groups = session.query(User.age,
                               func.count(User.id)).group_by(User.age)


    age_groups = session.query(User.age,
                               func.count(User.id).label('total_users')).group_by(User.age)

    print()



    # # Тот же запрос, но с обращением к таблице через алиас
    # age_groups = session.query(user_alias.age,
    #                            func.count(user_alias.id).label('total_users')).group_by(user_alias.age).all()
    # # Теперь можно обращаться к присвоенному имени
    # for group in age_groups:
    #     print(group.age, group.total_users)

# x = [1]
#
# a, *_ = x
#
# print(a, _)
#
#
# x = [(1, 2), (3, 4, 5, 6), (2, 3, 4, 5, 6)]
#
# for item, *_ in x:
#     print(item)

#1

# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
#
# engine = create_engine('sqlite:///test.db', echo=True)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
#     addresses = relationship("Address", back_populates="user", order_by="Address.id")
#
#     def __str__(self):
#         return f'{self.id=} {self.name=} {self.age=}'
#
#
# class Address(Base):
#     __tablename__ = 'addresses'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     description = Column(String)
#
#     user = relationship("User", back_populates="addresses")
#
#     def __str__(self):
#         return f'{self.id=} {self.description=}'
#
#
#
# with Session() as session:
#     # users = session.query(User).options(joinedload(User.addresses))
#     # for user in users.all():
#     #     print(user.id, user.name, user.age)
#     #     for address in user.addresses:
#     #         print("Address:", address.id, address.description)
#
#
#     rows = (session
#              .query(User, Address)
#              .join(Address)
#              )
#     for user, addr in rows.all():
#         print(user, addr)


# HW 3 end 4

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from faker import Faker
import random

engine = create_engine('sqlite:///hw_test.db')

Base = declarative_base()
Session = sessionmaker(bind=engine)

faker = Faker("ru_RU")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Numeric(10,2))
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')

    def __str__(self):
        return f'{self.id=}; {self.name=}; {self.price=}'


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))

    products = relationship('Product', back_populates='category')

    def __str__(self):
        return f'{self.id=}; {self.name=}; {self.description=}'


Base.metadata.create_all(engine)


categories = [Category(name=faker.company(), description=faker.sentence(nb_words=3)) for _ in range(5)]
print(*categories, sep='\n ')

session = Session()
session.add_all(categories)
session.commit()

for category in categories:
    for _ in range(random.randint(4, 10)):
        product = Product(
            name=faker.word().capitalize(),
            price=random.randint(1, 100),
            in_stock=random.choice([True, False]),
            category=category,
        )
        session.add(product)
session.commit()