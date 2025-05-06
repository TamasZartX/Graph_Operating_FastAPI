import os
import dotenv
from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from exceptions import graph_not_found, invalid_graph, node_not_found
from schemas import GraphCreate
from models import Graph, Node, Edge

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)
if not database_exists(DATABASE_URL): create_database(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def _check_cycle(unique_edges: dict[str, list[str]]):
    used: dict[str, bool] = {edge: False for edge in unique_edges}
    checked: dict[str, bool] = {edge: False for edge in unique_edges}

    def dfs(node: str):
        if used[node]:
            raise invalid_graph("Graph must be acyclic")

        used[node] = True
        for next_node in unique_edges[node]:
            dfs(next_node)
        used[node] = False
        checked[node] = True

    for node in unique_edges:
        if not checked[node]:
            dfs(node)


def create_graph(graph: GraphCreate) -> Graph:
    try:
        if not graph.nodes:
            raise invalid_graph("Graph must be not empty")
        new_graph = Graph()
        session.add(new_graph)
        session.flush()
        new_nodes = {}
        for node in graph.nodes:
            new_nodes[node.name] = Node(name=node.name, graph_id=new_graph.id)
        if len(new_nodes) != len(graph.nodes):
            raise invalid_graph("Nodes must be unique")
        session.add_all(new_nodes.values())
        print(new_nodes)
        session.flush()
        new_edges = []
        unique_edges: dict[str, list[str]] = {node.name: [] for node in graph.nodes}
        for edge in graph.edges:
            if edge.target in unique_edges[edge.source] or edge.source in unique_edges[edge.target]:
                raise invalid_graph("Edges must be unique")
            if edge.source == edge.target:
                raise invalid_graph("Edge source and target must be different")
            if edge.source not in graph.nodes or edge.target not in graph.nodes:
                raise invalid_graph("Edge nodes must be in nodes list")
            unique_edges[edge.source].append(edge.target)
            new_edges.append(Edge(source_id=new_nodes[edge.source].id, target_id=new_nodes[edge.target].id))
        _check_cycle(unique_edges)
        session.add_all(new_edges)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail={"message": f"Database error: {str(e)}"}
        )
    return new_graph


def read_graph(graph_id: int, output_type: str) -> dict[str, list[str]] | tuple[list[dict[str, int],  list[dict[str, int]]]]:
    nodes = session.query(Node).filter(Node.graph_id == graph_id).all()
    if not nodes:
        raise graph_not_found(graph_id)
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
    if not nodes:
        raise graph_not_found(graph_id)
    node_ids = {node.name: node.id for node in nodes}
    node_to_delete = session.get(Node, node_ids[node_name])
    if not node_to_delete:
        raise node_not_found(node_name)
    session.delete(node_to_delete)
    session.commit()
