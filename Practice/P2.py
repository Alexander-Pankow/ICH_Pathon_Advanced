
                        #Практическая работа: Pydantic

"""
Задача 1: Определение модели события.
Создайте модель Event, которая включает поля:
● title (строка),
● date (дата и время события),
● location (строка).
Добавьте валидацию, чтобы дата события не была в прошлом.
"""

# from pydantic import BaseModel, field_validator
# from datetime import datetime, timedelta
#
# class Event(BaseModel):
#     title: str
#     date: datetime
#     location: str
#
#     @field_validator('date')
#     def date_must_be_future(cls, v):
#         if v < datetime.now():
#             raise ValueError("Event date must be in the future")
#         return v
#
# # Пример использования
# try:
#     future_event = Event(title="New Year Party", date=datetime.now() +
# timedelta(days=30), location="New York")
#     print(future_event)
# except ValueError as e:
#     print(e)

""" 
Задача 2: Создание модели для пользователя с настройками
Определите модель UserProfile с полями:
● username (строка),
● password (строка),
● email (строка с валидацией email).
Используйте Field для добавления описаний и настройки валидации пароля
(должен быть не менее 8 символов).
"""

# from pydantic import BaseModel, EmailStr, Field
#
# class UserProfile(BaseModel):
#     username: str = Field(..., description="Username")
#     password: str = Field(...,min_length=8, description="Password must be at least 8 characters long" )
#     email: EmailStr
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "username": "john_doe",
#                 "password": "securePassword123",
#                 "email": "join.doe@example.com"
#             }
#         }
#
# # Пример создания пользователя
# user_profile = UserProfile(username="john_doe", password="securePassword123", email="join.doe@example.com")

""" 
Задача 3: Модель для управления транзакциями
Разработайте модель Transaction для управления финансовыми операциями.
Модель должна содержать:
● amount (десятичное число),
● transaction_type (строка, принимает значения "debit" или "credit"),
● currency (строка).
"""
# from pydantic import BaseModel, constr, condecimal
#
# class Transaction(BaseModel):
#     amount: condecimal(gt=0)
#     transaction_type: constr(pattern="^(debit|credit)$")
#     currency: constr(min_length=3, max_length=3)
#
#     class Config:
#         strstrip_whitespace = True
#
# # Пример транзакции
# transaction = Transaction(amount=123, transaction_type="debit", currency="USD")
# print(transaction)




""" 
Задача 4: Модель с расширенной валидацией даты
Создайте модель Appointment для записи на прием, которая включает
patient_name (строка), appointment_date (дата и время) и проверку, что запись
не может быть установлена ранее, чем через 24 часа от текущего момента.
"""

# from pydantic import BaseModel, field_validator
# from datetime import datetime, timedelta
#
# class Appointment(BaseModel):
#     patient_name: str
#     appointment_date: datetime
#
#     @field_validator('appointment_date')
#     def check_appointment_date(cls, v):
#         if v < datetime.now() + timedelta(days=1):
#             raise ValueError("Appointment must be scheduled at least 24 hours in advance.")
#         return v
#
# # Пример использования
# try:
#     appointment = Appointment(patient_name="Alice Smith",
#     appointment_date=datetime.now() + timedelta(hours=25))
#     print(appointment)
# except ValueError as e:
#     print(e)



                     #Практическая работа: SQLAlchemy

"""
Задача 1: Создание движка подключения
Создайте экземпляр движка для подключения к MySQL базе данных.
"""

from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///test.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


Base.metadata.create_all(engine)
with Session() as session:
    new_user = User(name="John Doe", age=28)

    session.add(new_user)
    session.commit()

""" 
Задача 2: Настройка движка
Напишите код для создания движка SQLAlchemy с подключением к базе данных
SQLite, который будет располагаться в памяти, и настройте вывод логов всех
операций с базой данных на экран.
"""

# from sqlalchemy import create_engine
# import logging
#
# logging.basicConfig(level=logging.INFO)
# engine = create_engine('sqlite:///:memory:', echo=True)

""" 
Задача 3: Определение модели пользователя
Создайте модель User с полями:
● id (целочисленный тип, первичный ключ),
● name (строковый тип, длина до 50 символов),
● age (целочисленный тип).
"""

# from sqlalchemy.orm import declarative_base
# from sqlalchemy import Column, Integer, String
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)

""" 
Задача 4: Моделирование и связи
Определите две модели, User и Post, где пользователь может иметь много постов
(один ко многим). Используйте декларативный базовый класс.
"""

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
# class Post(Base):
#     __tablename__ = 'posts'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255))
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship("User", back_populates="posts")
#
# Base.metadata.create_all(engine)

""" 
Задача 5: Моделирование и связи
Определите две модели, User и Adress, где User может иметь множество Address.
Используйте декларативный базовый класс.
"""

# Class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#
# class Address(Base):
#     __tablename__ = 'addresses'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship("User", back_populates="addresses")
#
# Base.metadata.create_all(engine)

""" 
Задача 6: Работа с сессией для добавления и удаления записей
Используя ранее определённые модели User и Adress, создайте нового
пользователя и адрес, добавьте их в базу данных с помощью сессии, затем удалите
пользователя и проверьте изменения.
"""

# from sqlalchemy.orm import sessionmaker
#
# # Создание сессии
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Создание нового пользователя и адреса
# new_user = User(name="John Doe", age=28)
# new_address = Address(user=new_user, description="123 Elm Street")
#
# # Добавление в базу данных
# session.add(new_user)
# session.add(new_address)
# session.commit()
#
# # Удаление пользователя и проверка
# session.delete(new_user)
# session.commit()
#
# # Проверка, что пользователь удалён
# print(session.query(User).filter_by(name="John Doe").first())

"""
Задача 7: Анализ ошибок
Найдите и исправьте ошибки в коде ниже.
"""

# from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# engine = create_engine('sqlite:///example.db')
#
# class Person():
#     __tablename__ = 'persons'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     pets = relationship("Pet", back_populates="owner")
#
# class Pet():
#     __tablename__ = 'pets'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     owner_id = Column(Integer, ForeignKey('persons.id'))
#     owner = relationship("Person", back_populates="pets")
#
# Base.metadata.create_all(engine)
# Session = sessionmaker()
# session = Session()
#
# new_person = Person(name='Alice')
# new_pet = Pet(name='Fido', owner=new_person)
# session.add(new_person)
# session.add(new_pet)
# session.commit()
# session.close()



# Ошибки:
# ● в sessionmaker отсутствует параметр движка bind=engine
# ● не создан класс Base = declarative_base()
# ● модели не наследуются от класса Base
# ● не указан размер строки, например String(100)
