from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProviderCreate(BaseModel):
    name: str
    nit: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    nit: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class ProviderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    nit: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool
