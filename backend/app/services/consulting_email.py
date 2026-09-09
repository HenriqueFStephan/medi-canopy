"""Branded HTML + plain-text email for consulting requests."""

from __future__ import annotations

from html import escape
from typing import Sequence

# Email clients ignore stylesheets — inline Forest Canopy tokens from docs/BRAND.md.
_PRIMARY = "#1B4332"
_PRIMARY_MID = "#2D6A4F"
_ACCENT = "#D4A574"
_BG = "#F8FAF7"
_SURFACE = "#FFFFFF"
_TEXT = "#1A1A1A"
_MUTED = "#5A6B62"
_BORDER = "#E2E8E4"
_FOOTER_BG = "#0D1F17"


def consulting_subject(name: str) -> str:
    return f"Solicitação de consultoria — {name}"


def consulting_text_body(
    *,
    name: str,
    email: str,
    company: str,
    phone: str,
    services: Sequence[str],
    message: str,
    received_at: str,
) -> str:
    service_lines = "\n".join(f"- {title}" for title in services) or "- (não informado)"
    company_line = company or "(não informado)"
    phone_line = phone or "(não informado)"
    return (
        "Nova solicitação de consultoria — Medi Canopy\n\n"
        f"Recebida em: {received_at}\n"
        f"Nome: {name}\n"
        f"E-mail: {email}\n"
        f"Empresa: {company_line}\n"
        f"Telefone: {phone_line}\n\n"
        "Áreas de interesse:\n"
        f"{service_lines}\n\n"
        "Mensagem:\n"
        f"{message}\n"
    )


def consulting_html_body(
    *,
    name: str,
    email: str,
    company: str,
    phone: str,
    services: Sequence[str],
    message: str,
    received_at: str,
) -> str:
    service_items = (
        "".join(
            f'<li style="margin:0 0 6px;color:{_TEXT};">{escape(title)}</li>'
            for title in services
        )
        or f'<li style="margin:0;color:{_MUTED};">Não informado</li>'
    )
    rows = [
        ("Nome", name),
        ("E-mail", email),
        ("Empresa", company or "Não informado"),
        ("Telefone", phone or "Não informado"),
        ("Recebida em", received_at),
    ]
    row_html = "".join(
        f"""
        <tr>
          <td style="padding:10px 12px;border-bottom:1px solid {_BORDER};color:{_MUTED};font-size:13px;width:140px;vertical-align:top;">{escape(label)}</td>
          <td style="padding:10px 12px;border-bottom:1px solid {_BORDER};color:{_TEXT};font-size:15px;">{escape(value)}</td>
        </tr>
        """
        for label, value in rows
    )
    safe_message = escape(message).replace("\n", "<br />")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Solicitação de consultoria</title>
</head>
<body style="margin:0;padding:0;background:{_BG};color:{_TEXT};font-family:'Source Sans 3',Arial,Helvetica,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BG};padding:24px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="640" cellpadding="0" cellspacing="0" style="max-width:640px;width:100%;background:{_SURFACE};border:1px solid {_BORDER};border-radius:8px;overflow:hidden;">
          <tr>
            <td style="background:{_PRIMARY};padding:28px 32px;">
              <p style="margin:0 0 6px;color:{_ACCENT};font-size:11px;letter-spacing:0.14em;text-transform:uppercase;font-weight:700;">Medi Canopy</p>
              <h1 style="margin:0;color:{_SURFACE};font-family:Georgia,'Times New Roman',serif;font-size:26px;font-weight:400;line-height:1.25;">
                Solicitação de consultoria
              </h1>
            </td>
          </tr>
          <tr>
            <td style="height:4px;background:{_ACCENT};font-size:0;line-height:0;">&nbsp;</td>
          </tr>
          <tr>
            <td style="padding:28px 32px 8px;">
              <p style="margin:0 0 20px;color:{_MUTED};font-size:15px;line-height:1.6;">
                Novo pedido pela página <strong style="color:{_PRIMARY_MID};">Serviços</strong>.
                Responda a este e-mail para falar com o solicitante.
              </p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {_BORDER};border-radius:8px;overflow:hidden;">
                {row_html}
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:20px 32px 8px;">
              <h2 style="margin:0 0 10px;color:{_PRIMARY};font-family:Georgia,'Times New Roman',serif;font-size:18px;font-weight:400;">
                Áreas de interesse
              </h2>
              <ul style="margin:0;padding:0 0 0 18px;">
                {service_items}
              </ul>
            </td>
          </tr>
          <tr>
            <td style="padding:20px 32px 32px;">
              <h2 style="margin:0 0 10px;color:{_PRIMARY};font-family:Georgia,'Times New Roman',serif;font-size:18px;font-weight:400;">
                Mensagem
              </h2>
              <div style="padding:16px 18px;background:{_BG};border-left:3px solid {_ACCENT};color:{_TEXT};font-size:15px;line-height:1.65;">
                {safe_message}
              </div>
            </td>
          </tr>
          <tr>
            <td style="background:{_FOOTER_BG};padding:16px 32px;color:#95D5B2;font-size:12px;">
              Medi Canopy — consultoria técnica e estratégica em cannabis medicinal.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
