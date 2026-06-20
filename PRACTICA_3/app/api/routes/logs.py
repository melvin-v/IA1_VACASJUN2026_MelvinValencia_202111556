from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.processing_log import ProcessingLogRepository
from app.schemas.processing_log import ProcessingLogRead

router = APIRouter(prefix="/logs", tags=["bitacora"])


@router.get("", response_model=List[ProcessingLogRead])
def list_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return ProcessingLogRepository(db).list_recent(skip=skip, limit=limit)
