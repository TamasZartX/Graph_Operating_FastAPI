from pydantic import BaseModel


class Node(BaseModel):
  name: str


class Edge(BaseModel):
  source: str
  target: str


class GraphCreate(BaseModel):
  nodes: list[Node]
  edges: list[Edge]

class GraphCreateResponse(BaseModel):
  id: int


class GraphReadResponse(BaseModel):
  id: int
  nodes: list[Node]
  edges: list[Edge]


class AdjacencyListResponse(BaseModel):


      "AdjacencyListResponse": {
        "properties": {
          "adjacency_list": {
            "additionalProperties": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "type": "object",
            "title": "Adjacency List"
          }
        },
        "type": "object",
        "required": [
          "adjacency_list"
        ],
        "title": "AdjacencyListResponse"
      },
      "ErrorResponse": {
        "properties": {
          "message": {
            "type": "string",
            "title": "Message"
          }
        },
        "type": "object",
        "required": [
          "message"
        ],
        "title": "ErrorResponse"
      },
      "HTTPValidationError": {
        "properties": {
          "detail": {
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            },
            "type": "array",
            "title": "Detail"
          }
        },
        "type": "object",
        "title": "HTTPValidationError"
      },
      "ValidationError": {
        "properties": {
          "loc": {
            "items": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "integer"
                }
              ]
            },
            "type": "array",
            "title": "Location"
          },
          "msg": {
            "type": "string",
            "title": "Message"
          },
          "type": {
            "type": "string",
            "title": "Error Type"
          }
        },
        "type": "object",
        "required": [
          "loc",
          "msg",
          "type"
        ],
        "title": "ValidationError"
      }
