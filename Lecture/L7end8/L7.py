from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


Base.metadata.create_all(engine)
session = Session()

new_user = User(name="John", age=23)
session.add(new_user)

session.add_all(
    [
        User(name='Bob', age=22),
        User(name='David', age=27),
        User(name='Alice', age=30),
        User(name='Ann', age=17),
        User(name='Ann', age=27)
    ]
)
session.commit()


# with Session() as session:
#    ...

#2

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker
#
#
# engine = create_engine('sqlite:///test.db')
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
#     def __str__(self):
#         return f'{self.id=} {self.name=} {self.age=}'
#
#
# with Session() as session:
#     user = session.query(User).get(100)
#     if user:
#         print(user.name, user.age)
#     else:
#         print('No data')
#     print('-' * 20)
#     users = session.query(User).all()
#     print(*users, sep='\n')
#     print('-' * 20)
#     users = session.query(User).filter(User.age > 23).all()
#     print(*users, sep='\n')


#3

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker
#
#
# engine = create_engine('sqlite:///test.db')
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
#     def __str__(self):
#         return f'{self.id=} {self.name=} {self.age=}'
#
#
# with Session() as session:
#     user = session.query(User).get(1)
#     if user:
#         session.delete(user)
#         session.commit()
#
#         print('user deleted')
#
#     print('-' * 20)
#     users = session.query(User).all()
#     print(*users, sep='\n')


#4

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker
#
#
# engine = create_engine('sqlite:///test.db')
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
#     def __str__(self):
#         return f'{self.id=} {self.name=} {self.age=}'
#
#
# with Session() as session:
#     user = session.query(User).get(2)
#     if user:
#         user.age = 99
#         session.commit()
#
#         print('user updated')
#
#     print('-' * 20)
#     users = session.query(User).all()
#     print(*users, sep='\n')

#5

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker
#
#
# engine = create_engine('sqlite:///test.db')
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
#     def __str__(self):
#         return f'{self.id=} {self.name=} {self.age=}'
#
#
# with Session() as session:
#     # users = session.query(User).filter(User.age >= 20)
#     users = session.query(User).filter(User.name.like('%user%')).all()
#     print(users)
#
#     users = users.all()
#     print(*users, sep='\n')


#6

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker
#
#
# engine = create_engine('sqlite:///test.db')
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
#     def __str__(self):
#         return f'{self.id=} {self.name=} {self.age=}'
#
#
# with Session() as session:
#     # | = or, & = and, ~ - not
#
#     users = session.query(User).filter(
#         (User.name.like('J%')) |
#         (User.age == 17)
#     ).all()
#     print(*users, sep='\n')