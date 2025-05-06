from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Graph(Base):
    __tablename__ = 'graph'

    id = Column(Integer, primary_key=True)

    nodes = relationship("Node", back_populates="graph")


class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    graph_id = Column(Integer, ForeignKey('graph.id'), nullable=False)

    graph = relationship("Graph", back_populates="nodes")
    edges_out = relationship("Edge", foreign_keys="Edge.source_id", back_populates="source", cascade="all, delete-orphan")
    edges_in = relationship("Edge", foreign_keys="Edge.target_id", back_populates="target", cascade="all, delete-orphan")


class Edge(Base):
    __tablename__ = 'edge'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('node.id'), nullable=False)
    target_id = Column(Integer, ForeignKey('node.id'), nullable=False)

    source = relationship("Node", foreign_keys=[source_id], back_populates="edges_out")
    target = relationship("Node", foreign_keys=[target_id], back_populates="edges_in")
