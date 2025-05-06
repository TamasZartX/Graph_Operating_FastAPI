def test_get_graph_success(client):
    request_body = {
        "nodes": [{"name": "asdf"}, {"name": "qwre"}],
        "edges": [{"source": "asdf", "target": "qwre"}]
    }
    create_resp = client.post("/api/graph/", json=request_body)
    assert create_resp.status_code == 201
    graph_id = create_resp.json()["id"]

    response = client.get(f"/api/graph/{graph_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == graph_id
    names = sorted(node["name"] for node in data["nodes"])
    assert names == ["asdf", "qwre"]
    edge_pairs = {(edge["source"], edge["target"]) for edge in data["edges"]}
    assert edge_pairs == {("asdf", "qwre")}


def test_get_graph_not_found(client):
    response = client.get("/api/graph/9999/")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"]["message"] == "Graph graph_id=9999 not found"
