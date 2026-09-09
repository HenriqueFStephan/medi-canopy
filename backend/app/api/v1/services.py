"""Consulting services showcase API."""

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.models.schemas import (
    ConsultingRequestCreate,
    ConsultingRequestResponse,
    ServiceOffering,
)
from app.repositories.json_store import consulting_store, new_id, services_store
from app.services.consulting_email import (
    consulting_html_body,
    consulting_subject,
    consulting_text_body,
)
from app.services.mailer import send_html_email

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[ServiceOffering])
def list_services() -> list[ServiceOffering]:
    return [ServiceOffering.model_validate(i) for i in services_store.read_all()]


@router.post("/consulting-request", response_model=ConsultingRequestResponse)
def submit_consulting_request(payload: ConsultingRequestCreate) -> ConsultingRequestResponse:
    """Persist a consulting inquiry and send a branded HTML email to the author."""
    offerings = {
        item["id"]: ServiceOffering.model_validate(item)
        for item in services_store.read_all()
    }
    unknown = [sid for sid in payload.service_ids if sid not in offerings]
    if unknown:
        raise HTTPException(status_code=422, detail=f"Unknown service ids: {unknown}")

    selected = [offerings[sid] for sid in payload.service_ids]
    service_titles = [svc.title for svc in selected]
    received_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html_body = consulting_html_body(
        name=payload.name,
        email=str(payload.email),
        company=payload.company,
        phone=payload.phone,
        services=service_titles,
        message=payload.message,
        received_at=received_at,
    )
    text_body = consulting_text_body(
        name=payload.name,
        email=str(payload.email),
        company=payload.company,
        phone=payload.phone,
        services=service_titles,
        message=payload.message,
        received_at=received_at,
    )

    settings = get_settings()
    # TODO: change CONSULTING_NOTIFY_TO to adm@medicanopy.com.br (self-test Gmail for now).
    recipient = settings.consulting_notify_to or settings.author_email
    mail = send_html_email(
        to=recipient,
        subject=consulting_subject(payload.name),
        html_body=html_body,
        text_body=text_body,
        reply_to=str(payload.email),
        slug="consulting-request",
    )

    record = {
        "id": new_id(),
        "received_at": received_at,
        "notified_to": recipient,
        "email_sent": mail.sent,
        "email_error": mail.error,
        "placeholder_file": mail.placeholder_file,
        **payload.model_dump(mode="json"),
        "service_titles": service_titles,
    }
    consulting_store.append(record)

    message = (
        "Solicitação enviada. Retornaremos em breve."
        if mail.sent
        else "Solicitação registrada. Retornaremos em breve."
    )
    return ConsultingRequestResponse(
        success=True,
        message=message,
        email_sent=mail.sent,
        email_error=mail.error,
    )


@router.get("/{service_id}", response_model=ServiceOffering)
def get_service(service_id: str) -> ServiceOffering:
    for item in services_store.read_all():
        if item["id"] == service_id:
            return ServiceOffering.model_validate(item)
    raise HTTPException(status_code=404, detail="Service not found")
