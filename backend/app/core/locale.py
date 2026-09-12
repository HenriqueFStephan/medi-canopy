"""Request-language helpers for public API payloads."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

Lang = str  # "pt-BR" | "en"

PT_TO_EN_HEADINGS = (
    ("## Por que importa", "## Why it matters"),
    ("## O que o estudo fez", "## What the study did"),
    ("## Principais achados", "## Key findings"),
    ("## Limitações", "## Limitations"),
    ("## Leitura crítica", "## Critical reading"),
    ("## Fonte", "## Source"),
    ("## Referência", "## Reference"),
    ("## Resumo", "## Summary"),
    ("**Publicado em:**", "**Published:**"),
    ("**Autores:**", "**Authors:**"),
    ("**Fonte:**", "**Source:**"),
    ("*Artigo científico curado para o blog Medi Canopy. Consulte a fonte original antes de decisões clínicas ou regulatórias.*",
     "*Scientific article curated for the Medi Canopy blog. Consult the original source before clinical or regulatory decisions.*"),
    ("Autores não informados", "Authors not provided"),
    ("Data não informada", "Date not provided"),
    ("Periódico não informado", "Journal not provided"),
    ("*Resumo em português pendente — ativar LLM em produção.*",
     "*Portuguese summary pending — enable the LLM in production.*"),
)

CONTACT_OK = {
    "pt-BR": "Mensagem recebida. Retornaremos em breve.",
    "en": "Message received. We will get back to you soon.",
}

CONSULTING_SENT = {
    "pt-BR": "Solicitação enviada. Retornaremos em breve.",
    "en": "Request sent. We will get back to you soon.",
}

CONSULTING_SAVED = {
    "pt-BR": "Solicitação registrada. Retornaremos em breve.",
    "en": "Request recorded. We will get back to you soon.",
}


def normalize_lang(value: str | None) -> Lang:
    """Map query/header values to the two supported site languages."""
    if not value:
        return "pt-BR"
    token = value.strip().lower().replace("_", "-").split(",")[0].split(";")[0]
    if token.startswith("en"):
        return "en"
    return "pt-BR"


def _translate_headings(markdown: str, lang: Lang) -> str:
    if lang != "en" or not markdown:
        return markdown
    out = markdown
    for src, dst in PT_TO_EN_HEADINGS:
        out = out.replace(src, dst)
    return out


def localize_item(item: dict[str, Any], lang: Lang) -> dict[str, Any]:
    """
    Return a copy of a stored record with translatable fields applied.

    Canonical fields stay in the original editorial language. Overlays live in
    `i18n.<lang>` and research posts may set `title_pt` for Portuguese titles.
    """
    out = deepcopy(item)
    overlay = (out.pop("i18n", None) or {}).get(lang) or {}

    if lang == "pt-BR" and out.get("title_pt"):
        out["title"] = out["title_pt"]

    for key, value in overlay.items():
        if key == "modules" and isinstance(value, list) and isinstance(out.get("modules"), list):
            merged: list[dict[str, Any]] = []
            for index, module in enumerate(out["modules"]):
                extra = value[index] if index < len(value) and isinstance(value[index], dict) else {}
                merged.append({**module, **{k: v for k, v in extra.items() if v not in (None, "")}})
            out["modules"] = merged
            continue
        if value not in (None, ""):
            out[key] = value

    if isinstance(out.get("content_markdown"), str):
        out["content_markdown"] = _translate_headings(out["content_markdown"], lang)

    return out


def localize_list(items: list[dict[str, Any]], lang: Lang) -> list[dict[str, Any]]:
    return [localize_item(item, lang) for item in items]
