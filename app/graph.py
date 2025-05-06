import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Graph, Node, Edge
from database import get_db, create_graph, delete_node
from schemas import GraphCreate, GraphCreateResponse

router = APIRouter(prefix="/api/graph")


@router.post("/")
def post_graph(graph: GraphCreate):
    new_graph = create_graph(graph)
    return new_graph.id


@router.get("/{graph_id}", response_model=GraphCreate)
def get_graph(graph_id: int, db: Session = Depends(get_db)):
    nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
    node_ids = [nd.id for nd in nodes]
    node_names = {node.id: node.name for node in nodes}
    edges = db.query(Edge).filter(Edge.source_id.in_(node_ids), Edge.target_id.in_(node_ids)).all()
    edge_schemas = [{"id": edge.id, "source": node_names[edge.source_id], "target": node_names[edge.target_id]} for edge in edges]

    return {"nodes": nodes, "edges": edge_schemas}


@router.get("/{graph_id}/adjacency_list")
def get_adj_list(graph_id: int, db: Session = Depends(get_db)):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
    node_ids = [nd.id for nd in nodes]
    node_names = {node.id: node.name for node in nodes}
    edges = db.query(Edge).filter(Edge.source_id.in_(node_ids), Edge.target_id.in_(node_ids)).all()
    adj_list: dict[str, list[str]] = {node_names[node.id]: [] for node in nodes}
    logging.info(adj_list)
    for edge in edges:
        adj_list[node_names[edge.source_id]].append(node_names[edge.target_id])

    return {"adjasency_list": adj_list}


@router.get("/{graph_id}/reverse_adjacency_list")
def get_rev_adj_list(graph_id: int, db: Session = Depends(get_db)):
    graph = db.query(Graph).filter(Graph.id == graph_id).first()
    nodes = db.query(Node).filter(Node.graph_id == graph_id).all()
    node_ids = [nd.id for nd in nodes]
    node_names = {node.id: node.name for node in nodes}
    edges = db.query(Edge).filter(Edge.source_id.in_(node_ids), Edge.target_id.in_(node_ids)).all()
    adj_list: dict[str, list[str]] = {node_names[node.id]: [] for node in nodes}
    logging.info(adj_list)
    for edge in edges:
        adj_list[node_names[edge.target_id]].append(node_names[edge.source_id])

    return {"adjasency_list": adj_list}


@router.delete("/{graph_id}/node/{node_name}")
def del_node(graph_id: int, node_name: str):
    delete_node(graph_id, node_name)
    return {"success": True}
