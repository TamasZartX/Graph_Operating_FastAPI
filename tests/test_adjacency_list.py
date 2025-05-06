def test_adjacency_list_no_edges(client):
    request_body = {"nodes": [{"name": "Solo"}], "edges": []}
    resp = client.post("/api/graph/", json=request_body)
    graph_id = resp.json()["id"]
    response = client.get(f"/api/graph/{graph_id}/adjacency_list")
    assert response.status_code == 200
    data = response.json()
    expected = {"Solo": []}
    assert data["adjacency_list"] == expected


def test_adjacency_list_with_edges(client):
    request_body = {
        "nodes": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "A", "target": "C"},
            {"source": "B", "target": "C"}
        ]
    }
    resp = client.post("/api/graph/", json=request_body)
    graph_id = resp.json()["id"]
    response = client.get(f"/api/graph/{graph_id}/adjacency_list")
    assert response.status_code == 200
    adj_data = response.json()["adjacency_list"]
    assert set(adj_data["A"]) == {"B", "C"}
    assert adj_data["B"] == ["C"]
    assert adj_data["C"] == []
    assert set(adj_data.keys()) == {"A", "B", "C"}


def test_adjacency_list_not_found(client):
    response = client.get("/api/graph/12345/adjacency_list")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"]["message"] == "Graph graph_id=12345 not found"
