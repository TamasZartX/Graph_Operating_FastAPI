from pydantic import BaseModel, Field


class Node(BaseModel):
    name: str = Field(...,min_length=1, max_length=255, pattern="^[A-Za-z]+$")

    class Config:
        from_attributes = True


class Edge(BaseModel):
    source: str
    target: str

    class Config:
        from_attributes = True


class GraphCreate(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

    class Config:
        from_attributes = True


class GraphCreateResponse(BaseModel):
    id: int


class GraphReadResponse(BaseModel):
    id: int
    nodes: list[Node]
    edges: list[Edge]


class AdjacencyListResponse(BaseModel):
    adjacency_list: dict[str, list[str]]


class ErrorResponse(BaseModel):
    message: str
