from config.db import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(1000))
    priority = Column(Integer)
    completed = Column(Boolean, default=False)