from sqlalchemy import Column, Integer, String, ForeignKey, Numeric

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    owner = Column(String(50), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Numeric(10, 2))
    account = relationship("Account", back_populates="transactions")


                     #Practika

# Определите модель Product с различными
# типами колонок:
# ● id (числовой идентификатор)
# ● name (строковый)
# ● price (точный дробный)
# ● in_stock (логический)


# from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# engine = create_engine('sqlite:///test.db')
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
#
#
# class Product(Base):
#     __tablename__ = 'products'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     price = Column(Numeric(10,2))
#     in_stock = Column(Boolean, default=False)
#
#
# Base.metadata.create_all(engine)
# with Session() as session:
#     pr_1 = Product(name='Product 1', price=100, in_stock=True)
#     pr_2 = Product(name='Product 2', price=100, in_stock=True)
#     pr_3 = Product(name='Product 3', price=100, in_stock=True)
#     pr_4 = Product(name='Product 4', price=100, in_stock=True)
#
#     session.add(pr_1)
#     session.add(pr_2)
#     session.add(pr_3)
#     session.add(pr_4)
#     session.commit()