from fastapi import APIRouter
from schemas import GraphCreate

router = APIRouter(prefix="/api/graph")


@router.post("/")
def post_graph(graph: GraphCreate):
    pass


@router.get("/{graph_id}")
def get_graph():
    pass


@router.get("/{graph_id}/adjacency_list")
def get_adj_list():
    pass


@router.get("/{graph_id}/reverse_adjacency_list")
def get_rev_adj_list():
    pass


@router.delete("/{graph_id}/node/{node_id}")
def delete_node():
    pass
