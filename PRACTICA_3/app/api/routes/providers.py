from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.provider import ProviderCreate, ProviderUpdate, ProviderRead
from app.services.provider_service import ProviderService

router = APIRouter(prefix="/providers", tags=["providers"])


@router.post("", response_model=ProviderRead, status_code=status.HTTP_201_CREATED)
def create_provider(
    data: ProviderCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        return ProviderService(db).create(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[ProviderRead])
def list_providers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return ProviderService(db).list(skip=skip, limit=limit)


@router.get("/{provider_id}", response_model=ProviderRead)
def get_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    provider = ProviderService(db).get(provider_id)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return provider


@router.put("/{provider_id}", response_model=ProviderRead)
def update_provider(
    provider_id: int,
    data: ProviderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    provider = ProviderService(db).update(provider_id, data)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return provider


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if not ProviderService(db).delete(provider_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
