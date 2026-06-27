"""Consulting services showcase API."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import ServiceOffering
from app.repositories.json_store import services_store

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[ServiceOffering])
def list_services() -> list[ServiceOffering]:
    return [ServiceOffering.model_validate(i) for i in services_store.read_all()]


@router.get("/{service_id}", response_model=ServiceOffering)
def get_service(service_id: str) -> ServiceOffering:
    for item in services_store.read_all():
        if item["id"] == service_id:
            return ServiceOffering.model_validate(item)
    raise HTTPException(status_code=404, detail="Service not found")
