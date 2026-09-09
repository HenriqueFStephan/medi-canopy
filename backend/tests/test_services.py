"""Consulting services showcase API."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

EXPECTED_TITLES = [
    "Viabilidade & Investimentos",
    "Engenharia & Desenvolvimento",
    "Cultivo & Operações",
    "Regulatório & Qualidade",
    "Implantação & Performance",
]


def test_list_services_returns_five_offerings():
    response = client.get("/api/v1/services")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert [item["title"] for item in data] == EXPECTED_TITLES


def test_get_service_by_id():
    response = client.get("/api/v1/services/svc-viability")
    assert response.status_code == 200
    assert response.json()["title"] == EXPECTED_TITLES[0]
    assert "CAPEX" in response.json()["description"]
