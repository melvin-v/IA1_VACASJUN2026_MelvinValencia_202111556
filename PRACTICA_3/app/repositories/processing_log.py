from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.processing_log import ProcessingLog
from app.repositories.base import BaseRepository


class ProcessingLogRepository(BaseRepository[ProcessingLog]):
    def __init__(self, db: Session):
        super().__init__(ProcessingLog, db)

    def list_recent(self, skip: int = 0, limit: int = 100) -> Sequence[ProcessingLog]:
        stmt = (
            select(ProcessingLog)
            .order_by(ProcessingLog.processed_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.db.execute(stmt).scalars().all()
