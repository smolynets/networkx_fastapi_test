from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON


Base = declarative_base()


class Graph(Base):
    __tablename__ = "graph"
    id = Column(Integer, primary_key=True, nullable=False)
    node_data = Column(JSON)
