"""SMTP mailer fallback and send path."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services.mailer import send_html_email


def test_mailer_writes_placeholder_without_smtp(monkeypatch, tmp_path):
    monkeypatch.setattr("app.services.mailer.OUTBOUND_DIR", tmp_path)
    monkeypatch.setattr(
        "app.services.mailer.get_settings",
        lambda: SimpleNamespace(smtp_host=""),
    )

    result = send_html_email(
        to="author@example.com",
        subject="Teste",
        html_body="<p>Olá</p>",
        text_body="Olá",
        slug="consulting-request",
    )

    assert result.sent is False
    assert result.error == "SMTP_HOST is not set"
    assert result.placeholder_file is not None
    saved = Path(result.placeholder_file)
    assert saved.exists()
    assert "Olá" in saved.read_text(encoding="utf-8")


def test_mailer_sends_via_smtp(monkeypatch):
    settings = SimpleNamespace(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_username="user@example.com",
        smtp_password="secret",
        author_email="author@example.com",
    )
    monkeypatch.setattr("app.services.mailer.get_settings", lambda: settings)

    smtp_instance = MagicMock()
    smtp_instance.__enter__.return_value = smtp_instance
    smtp_instance.__exit__.return_value = False
    monkeypatch.setattr("app.services.mailer.smtplib.SMTP", lambda *_args, **_kwargs: smtp_instance)

    result = send_html_email(
        to="author@example.com",
        subject="Solicitação de consultoria — Ana",
        html_body="<p>Pedido</p>",
        text_body="Pedido",
        reply_to="ana@example.com",
    )

    assert result.sent is True
    smtp_instance.starttls.assert_called()
    smtp_instance.login.assert_called_once_with("user@example.com", "secret")
    smtp_instance.send_message.assert_called_once()


def test_mailer_uses_smtp_from_header(monkeypatch):
    settings = SimpleNamespace(
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        smtp_username="henrique.f.stephan@gmail.com",
        smtp_password="secret",
        smtp_from="henrique.f.stephan@gmail.com",
        author_email="adm@medicanopy.com.br",
        author_name="Medi Canopy",
    )
    monkeypatch.setattr("app.services.mailer.get_settings", lambda: settings)

    smtp_instance = MagicMock()
    smtp_instance.__enter__.return_value = smtp_instance
    smtp_instance.__exit__.return_value = False
    monkeypatch.setattr("app.services.mailer.smtplib.SMTP", lambda *_args, **_kwargs: smtp_instance)

    send_html_email(
        to="adm@medicanopy.com.br",
        subject="Teste",
        html_body="<p>Pedido</p>",
        text_body="Pedido",
        reply_to="cliente@example.com",
    )

    sent_msg = smtp_instance.send_message.call_args[0][0]
    assert "henrique.f.stephan@gmail.com" in sent_msg["From"]
    assert sent_msg["To"] == "adm@medicanopy.com.br"
    assert sent_msg["Reply-To"] == "cliente@example.com"


def test_mailer_saves_html_when_smtp_fails(monkeypatch, tmp_path):
    settings = SimpleNamespace(
        smtp_host="smtp.invalid",
        smtp_port=587,
        smtp_username="user@example.com",
        smtp_password="secret",
        author_email="author@example.com",
    )
    monkeypatch.setattr("app.services.mailer.get_settings", lambda: settings)
    monkeypatch.setattr("app.services.mailer.OUTBOUND_DIR", tmp_path)
    monkeypatch.setattr(
        "app.services.mailer.smtplib.SMTP",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("getaddrinfo failed")),
    )

    result = send_html_email(
        to="author@example.com",
        subject="Solicitação",
        html_body="<p>Pedido</p>",
        text_body="Pedido",
        slug="consulting-request",
    )

    assert result.sent is False
    assert result.error
    assert result.placeholder_file is not None
    assert Path(result.placeholder_file).exists()
