from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Registros1(Base):
    __tablename__ = 'registros1'

    id = Column(Integer, primary_key=True)
    time = Column(String, nullable=False)
    status = Column(String, nullable=False)
    count = Column(String, nullable=False)
    acao = Column(String, nullable=True)
