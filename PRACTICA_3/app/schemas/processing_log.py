from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProcessingLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_name: Optional[str] = None
    status: str
    result: Optional[str] = None
    processed_at: Optional[datetime] = None
    invoice_id: Optional[int] = None
    user_id: Optional[int] = None
