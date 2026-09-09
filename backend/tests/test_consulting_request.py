"""Consulting request email formatting and API."""

from pathlib import Path
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import ConsultingRequestCreate
from app.services.consulting_email import consulting_html_body, consulting_subject

client = TestClient(app)

VALID_PAYLOAD = {
    "name": "Ana Silva",
    "email": "ana@example.com",
    "company": "Verde Labs",
    "phone": "+55 11 99999-0000",
    "service_ids": ["svc-cultivation", "svc-regulatory"],
    "message": "Precisamos de apoio em CEA e GACP para uma unidade no interior de SP.",
}


def test_consulting_html_uses_brand_and_escapes_content():
    html = consulting_html_body(
        name='Ana <script>alert("x")</script>',
        email="ana@example.com",
        company="Verde Labs",
        phone="",
        services=["Cultivo & Operações"],
        message="Linha 1\nLinha 2",
        received_at="2026-09-09 20:00 UTC",
    )

    assert "#1B4332" in html
    assert "#D4A574" in html
    assert "Medi Canopy" in html
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "Linha 1<br />Linha 2" in html
    assert consulting_subject("Ana Silva") == "Solicitação de consultoria — Ana Silva"


def test_consulting_request_persists_and_formats_email(monkeypatch, tmp_path: Path):
    captured: dict = {}

    def fake_send(**kwargs):
        captured.update(kwargs)
        result = MagicMock()
        result.sent = False
        result.error = None
        result.placeholder_file = str(tmp_path / "mail.html")
        return result

    stored: list[dict] = []
    monkeypatch.setattr("app.api.v1.services.send_html_email", fake_send)
    monkeypatch.setattr(
        "app.api.v1.services.consulting_store.append",
        lambda record: stored.append(record) or record,
    )

    response = client.post("/api/v1/services/consulting-request", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["email_sent"] is False
    assert "html_body" in captured
    assert "Ana Silva" in captured["html_body"]
    assert "Cultivo" in captured["html_body"]
    assert "GACP" in captured["html_body"]
    assert captured["reply_to"] == "ana@example.com"
    assert captured["subject"].startswith("Solicitação de consultoria")
    assert stored[0]["email"] == "ana@example.com"
    assert stored[0]["service_titles"] == ["Cultivo & Operações", "Regulatório & Qualidade"]


def test_consulting_request_rejects_unknown_service():
    payload = {**VALID_PAYLOAD, "service_ids": ["svc-does-not-exist"]}
    response = client.post("/api/v1/services/consulting-request", json=payload)
    assert response.status_code == 422


def test_consulting_request_requires_message():
    payload = {**VALID_PAYLOAD, "message": "curto"}
    response = client.post("/api/v1/services/consulting-request", json=payload)
    assert response.status_code == 422


def test_consulting_request_schema_strips_and_dedupes():
    item = ConsultingRequestCreate.model_validate(
        {
            "name": "  Ana  ",
            "email": "ana@example.com",
            "service_ids": ["svc-cultivation", "svc-cultivation", ""],
            "message": "  Precisamos de apoio técnico no cultivo indoor.  ",
        }
    )
    assert item.name == "Ana"
    assert item.service_ids == ["svc-cultivation"]
    assert item.message.startswith("Precisamos")


def test_consulting_request_succeeds_when_smtp_unavailable(monkeypatch):
    result = MagicMock()
    result.sent = False
    result.error = "connection refused"
    result.placeholder_file = "/tmp/consulting.html"
    monkeypatch.setattr("app.api.v1.services.send_html_email", lambda **_kwargs: result)
    monkeypatch.setattr("app.api.v1.services.consulting_store.append", lambda record: record)

    response = client.post("/api/v1/services/consulting-request", json=VALID_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["email_sent"] is False
