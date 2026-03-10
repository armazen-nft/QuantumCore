from __future__ import annotations

from web_monitor.app import app


def test_api_peers_returns_expected_payload():
    client = app.test_client()
    response = client.get("/api/peers")
    assert response.status_code == 200
    payload = response.get_json()
    assert "peers" in payload
    assert "last_update" in payload
