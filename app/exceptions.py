from fastapi import HTTPException


def graph_not_found(graph_id: int):
    return HTTPException(status_code=404, detail={"message": f"Graph graph_id={graph_id} not found"})


def node_not_found(name: str):
    return HTTPException(status_code=404, detail={"message": f"Node '{name}' not found"})


def invalid_graph(message: str):
    return HTTPException(status_code=400, detail={"message": message})
