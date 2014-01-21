from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    name = Column(String)

    def __repr__(self):
        return "<node(id=%d, key='%s', name='%s')>" % (self.id, self.key, self.name)