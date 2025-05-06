import string
import pytest

def test_create_graph_success_no_edges(client):
    request_body = {"nodes": [{"name": "X"}], "edges": []}
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data and isinstance(data["id"], int), "Response should contain graph id"
    graph_id = data["id"]
    get_resp = client.get(f"/api/graph/{graph_id}/")
    assert get_resp.status_code == 200
    graph_data = get_resp.json()
    assert graph_data["id"] == graph_id
    assert graph_data["nodes"] == [{"name": "X"}]
    assert graph_data["edges"] == []


def test_create_graph_success_with_edges(client):
    request_body = {
        "nodes": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"}
        ]
    }
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 201
    graph_id = response.json()["id"]
    get_resp = client.get(f"/api/graph/{graph_id}/")
    data = get_resp.json()
    nodes = data["nodes"]
    edges = data["edges"]
    names_returned = sorted(node["name"] for node in nodes)
    names_expected = sorted(["A", "B", "C"])
    assert names_returned == names_expected
    edge_set = {(edge["source"], edge["target"]) for edge in edges}
    expected_edge_set = {("A", "B"), ("B", "C")}
    assert edge_set == expected_edge_set


def test_create_graph_invalid_empty_nodes(client):
    request_body = {"nodes": [], "edges": []}
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 400
    error = response.json()
    assert error["detail"]["message"] == "Graph must be not empty"


def test_create_graph_invalid_duplicate_nodes(client):
    request_body = {
        "nodes": [{"name": "A"}, {"name": "A"}],
        "edges": []
    }
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 400
    error = response.json()
    assert error["detail"]["message"] == "Nodes must be unique"


@pytest.mark.parametrize("invalid_name", ["Name1", "abc_d", "123", "A" * 256])
def test_create_graph_invalid_node_name(client, invalid_name):
    request_body = {"nodes": [{"name": invalid_name}], "edges": []}
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 400
    error_msg = error = response.json()["detail"]["message"]
    assert error_msg == "Node name must be made of only letters and length must be not more than 255 characters"


def test_create_graph_invalid_edge_unknown_node(client):
    request_body1 = {
        "nodes": [{"name": "A"}],
        "edges": [{"source": "B", "target": "A"}]
    }
    resp1 = client.post("/api/graph/", json=request_body1)
    assert resp1.status_code == 400
    error1 = resp1.json()
    assert error1["detail"]["message"] == "Edge nodes must be only from nodes list. Invalid node: B"

    request_body2 = {
        "nodes": [{"name": "A"}],
        "edges": [{"source": "A", "target": "C"}]
    }
    resp2 = client.post("/api/graph/", json=request_body2)
    assert resp2.status_code == 400
    error2 = resp2.json()
    assert error2["detail"]["message"] == "Edge nodes must be only from nodes list. Invalid node: C"


def test_create_graph_invalid_self_loop(client):
    request_body = {
        "nodes": [{"name": "X"}],
        "edges": [{"source": "X", "target": "X"}]
    }
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 400
    error = response.json()
    assert error["detail"]["message"] == "Edge source and target must be different"


def test_create_graph_invalid_duplicate_edge(client):
    request_body = {
        "nodes": [{"name": "A"}, {"name": "B"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "A", "target": "B"}
        ]
    }
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 400
    error = response.json()
    assert error["detail"]["message"] == "Edges must be unique"


def test_create_graph_invalid_cycle(client):
    request_body = {
        "nodes": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "A"}
        ]
    }
    response = client.post("/api/graph/", json=request_body)
    assert response.status_code == 400
    error = response.json()
    assert error["detail"]["message"] == "Graph must be acyclic"
