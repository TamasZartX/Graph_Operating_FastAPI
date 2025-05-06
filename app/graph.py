from fastapi import APIRouter, Depends

from app.database import create_graph, delete_node, read_graph
from app.schemas import GraphCreate, GraphCreateResponse, AdjacencyListResponse, ErrorResponse, GraphReadResponse

router = APIRouter(prefix="/api/graph")


@router.post("/", status_code=201, response_model=GraphCreateResponse, responses={201: {"description": "Successful response"} ,400: {"description": "Failed to add graph", "model": ErrorResponse}}, summary="Create Graph", description="Ручка для создания графа, принимает граф в виде списка вершин и списка ребер.", operation_id="create_graph_api_graph__post")
def post_graph(graph: GraphCreate):
    new_graph = create_graph(graph)
    return {"id": new_graph.id}


@router.get("/{graph_id}/", response_model=GraphReadResponse, responses={404: {"description": "Graph entity not found", "model": ErrorResponse}}, summary="Read Graph", description="Ручка для чтения графа в виде списка вершин и списка ребер.", operation_id="read_graph_api_graph__graph_id___get")
def get_graph(graph_id: int):
    [nodes, edge_schemas] = read_graph(graph_id, "default_list")
    return {"id": graph_id, "nodes": nodes, "edges": edge_schemas}


@router.get("/{graph_id}/adjacency_list", response_model=AdjacencyListResponse, responses={404: {"description": "Graph entity not found", "model": ErrorResponse}}, summary="Get Adjacency List", description="Ручка для чтения графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех потомков ключа).", operation_id="get_adjacency_list_api_graph__graph_id__adjacency_list_get")
def get_adj_list(graph_id: int):
    adj_list = read_graph(graph_id, "adjacency_list")
    return {"adjacency_list": adj_list}


@router.get("/{graph_id}/reverse_adjacency_list", response_model=AdjacencyListResponse, responses={404: {"description": "Graph entity not found", "model": ErrorResponse}}, summary="Get Reverse Adjacency List", description="Ручка для чтения транспонированного графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех предков ключа в исходном графе).", operation_id="get_reverse_adjacency_list_api_graph__graph_id__reverse_adjacency_list_get")
def get_rev_adj_list(graph_id: int):
    adj_list = read_graph(graph_id, "reverse_adjacency_list")
    return {"adjacency_list": adj_list}


@router.delete("/{graph_id}/node/{node_name}", status_code=204, responses={404: {"description": "Graph entity not found", "model": ErrorResponse}}, summary="Delete Node", description="Ручка для удаления вершины из графа по ее имени.", operation_id="delete_node_api_graph__graph_id__node__node_name__delete")
def del_node(graph_id: int, node_name: str):
    delete_node(graph_id, node_name)
    return {"success": True}
