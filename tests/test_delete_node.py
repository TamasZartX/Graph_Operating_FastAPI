def test_delete_node_success(client):
    request_body = {
        "nodes": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"}
        ]
    }
    create_resp = client.post("/api/graph/", json=request_body)
    graph_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/graph/{graph_id}/node/B")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/graph/{graph_id}/")
    data = get_resp.json()
    node_names = [node["name"] for node in data["nodes"]]
    assert "B" not in node_names
    assert set(node_names) == {"A", "C"}, "Graph should contain only A and C after deletion"
    edges = data["edges"]
    for edge in edges:
        assert edge["source"] != "B" and edge["target"] != "B"

    adj_resp = client.get(f"/api/graph/{graph_id}/adjacency_list")
    adj = adj_resp.json()["adjacency_list"]
    assert "B" not in adj
    assert adj == {'A': [], 'C': []}

    rev_adj_resp = client.get(f"/api/graph/{graph_id}/reverse_adjacency_list")
    rev_adj = rev_adj_resp.json()["adjacency_list"]
    assert "B" not in rev_adj
    assert rev_adj == {'A': [], 'C': []}


def test_delete_node_node_not_found(client):
    request_body = {"nodes": [{"name": "X"}], "edges": []}
    graph_id = client.post("/api/graph/", json=request_body).json()["id"]
    response = client.delete(f"/api/graph/{graph_id}/node/YaUstalPomogite")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"]["message"] == "Node 'Y' not found"


def test_delete_node_graph_not_found(client):
    response = client.delete("/api/graph/99999/node/AnyNode")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"]["message"] == "Graph graph_id=99999 not found"


def test_delete_last_node(client):
    request_body = {"nodes": [{"name": "last"}], "edges": []}
    graph_id = client.post("/api/graph/", json=request_body).json()["id"]
    response = client.delete(f"/api/graph/{graph_id}/node/last")
    assert response.status_code == 204
    response2 = client.get(f"/api/graph/{graph_id}/")
    assert response2.status_code == 404
    error = response2.json()
    assert error["detail"]["message"] == f"Graph graph_id={graph_id} not found"