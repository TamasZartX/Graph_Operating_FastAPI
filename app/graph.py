from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import GraphCreate

router = APIRouter(prefix="/api/graph")


@router.post("/")
def post_graph(graph: GraphCreate):
    pass


@router.get("/{graph_id}")
def get_graph(graph_id: int, db: Session = Depends(get_db)):
    pass


@router.get("/{graph_id}/adjacency_list")
def get_adj_list(graph_id: int, db: Session = Depends(get_db)):
    pass


@router.get("/{graph_id}/reverse_adjacency_list")
def get_rev_adj_list(graph_id: int, db: Session = Depends(get_db)):
    pass


@router.delete("/{graph_id}/node/{node_id}")
def delete_node(graph_id: int, node_id: int, db: Session = Depends(get_db)):
    pass
