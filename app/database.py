import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schemas import GraphCreate
from models import Graph, Node, Edge

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def get_db():
    try:
        yield session
    finally:
        session.close()


def create_graph(graph: GraphCreate) -> Graph:
    new_graph = Graph()
    session.add(new_graph)
    session.flush()
    new_nodes = {}
    for node in graph.nodes:
        new_nodes[node.name] = Node(name=node.name, graph_id=new_graph.id)
    session.add_all(new_nodes.values())
    print(new_nodes)
    session.flush()
    new_edges = []
    for edge in graph.edges:
        new_edges.append(Edge(source_id=new_nodes[edge.source].id, target_id=new_nodes[edge.target].id))
    session.add_all(new_edges)
    session.commit()
    return new_graph


def delete_node():
    pass
