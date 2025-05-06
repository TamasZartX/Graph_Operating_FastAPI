import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from schemas import GraphCreate
from models import Graph, Node, Edge

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)
if not database_exists(DATABASE_URL): create_database(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


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


def read_graph(graph_id: int, output_type: str) -> dict[str, list[str]] | tuple[list[dict[str, int],  list[dict[str, int]]]]:
    nodes = session.query(Node).filter(Node.graph_id == graph_id).all()
    node_ids = [nd.id for nd in nodes]
    node_names = {node.id: node.name for node in nodes}
    edges = session.query(Edge).filter(Edge.source_id.in_(node_ids), Edge.target_id.in_(node_ids)).all()
    if output_type == "adjacency_list":
        adj_list: dict[str, list[str]] = {node_names[node.id]: [] for node in nodes}
        for edge in edges:
            adj_list[node_names[edge.source_id]].append(node_names[edge.target_id])
        return adj_list
    elif output_type == "reverse_adjacency_list":
        adj_list: dict[str, list[str]] = {node_names[node.id]: [] for node in nodes}
        for edge in edges:
            adj_list[node_names[edge.target_id]].append(node_names[edge.source_id])
        return adj_list
    elif output_type == "default_list":
        edge_schemas = [{"source": node_names[edge.source_id], "target": node_names[edge.target_id]} for edge in edges]
        return [nodes, edge_schemas]


def delete_node(graph_id: int, node_name: str):
    nodes = session.query(Node).filter(Node.graph_id == graph_id).all()
    node_ids = {node.name: node.id for node in nodes}
    node_to_delete = session.get(Node, node_ids[node_name])
    session.delete(node_to_delete)
