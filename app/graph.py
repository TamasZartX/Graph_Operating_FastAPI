from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Graph, Node, Edge
from database import create_graph, delete_node, read_graph
from schemas import GraphCreate, GraphCreateResponse, AdjacencyListResponse, ErrorResponse

router = APIRouter(prefix="/api/graph")


@router.post("/", response_model=GraphCreateResponse, responses={400: {"model": ErrorResponse}})
def post_graph(graph: GraphCreate):
    new_graph = create_graph(graph)
    return {"id": new_graph.id}


@router.get("/{graph_id}", response_model=GraphCreate, responses={404: {"model": ErrorResponse}})
def get_graph(graph_id: int):
    [nodes, edge_schemas] = read_graph(graph_id, "default_list")
    return {"nodes": nodes, "edges": edge_schemas}


@router.get("/{graph_id}/adjacency_list", response_model=AdjacencyListResponse, responses={404: {"model": ErrorResponse}})
def get_adj_list(graph_id: int):
    adj_list = read_graph(graph_id, "adjacency_list")
    return {"adjacency_list": adj_list}


@router.get("/{graph_id}/reverse_adjacency_list", response_model=AdjacencyListResponse, responses={404: {"model": ErrorResponse}})
def get_rev_adj_list(graph_id: int):
    adj_list = read_graph(graph_id, "reverse_adjacency_list")
    return {"adjacency_list": adj_list}


@router.delete("/{graph_id}/node/{node_name}", status_code=204, responses={404: {"model": ErrorResponse}})
def del_node(graph_id: int, node_name: str):
    delete_node(graph_id, node_name)
    return {"success": True}
