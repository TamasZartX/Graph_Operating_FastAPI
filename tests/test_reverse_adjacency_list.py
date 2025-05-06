def test_reverse_adjacency_list_no_edges(client):
    request_body = {"nodes": [{"name": "X"}], "edges": []}
    resp = client.post("/api/graph/", json=request_body)
    graph_id = resp.json()["id"]
    response = client.get(f"/api/graph/{graph_id}/reverse_adjacency_list")
    assert response.status_code == 200
    data = response.json()
    expected = {"X": []}
    assert data["adjacency_list"] == expected


def test_reverse_adjacency_list_with_edges(client):
    request_body = {
        "nodes": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"}
        ]
    }
    resp = client.post("/api/graph/", json=request_body)
    graph_id = resp.json()["id"]
    response = client.get(f"/api/graph/{graph_id}/reverse_adjacency_list")
    assert response.status_code == 200
    rev_adj = response.json()["adjacency_list"]
    assert rev_adj["A"] == []
    assert rev_adj["B"] == ["A"]
    assert rev_adj["C"] == ["B"]
    assert set(rev_adj.keys()) == {"A", "B", "C"}


def test_reverse_adjacency_list_not_found(client):
    response = client.get("/api/graph/54321/reverse_adjacency_list")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"]["message"] == "Graph graph_id=54321 not found"
