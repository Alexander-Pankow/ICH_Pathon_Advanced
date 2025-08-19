from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

Base = declarative_base()

engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
# session = Session()


# Настройка базового логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')

# Включение логирования SQL-запросов
logger.setLevel(logging.INFO)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    age = Column(Integer)


Base.metadata.create_all(engine)

# new_user = User(name="John Doe", age=30)
# session.add(new_user)
# session.commit()


with Session() as session:
    session.add(User(name='John', age=20))
    session.commit()


# from sqlalchemy import MetaData, create_engine
# from sqlalchemy.ext.automap import automap_base
#
# engine = create_engine('sqlite:///example.db')
#
# metadata = MetaData()
# metadata.reflect(bind=engine)
# Base = automap_base(metadata=metadata)
# Base.prepare()
#
#
# # print(metadata.tables)
#
#
# User = Base.classes.users
#
#
# user1 = User(name="Tom", age=20)
# print(user1)