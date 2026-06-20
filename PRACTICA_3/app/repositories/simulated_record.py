from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.simulated_record import SimulatedRecord
from app.repositories.base import BaseRepository


class SimulatedRecordRepository(BaseRepository[SimulatedRecord]):
    def __init__(self, db: Session):
        super().__init__(SimulatedRecord, db)

    def list_recent(self, skip: int = 0, limit: int = 100) -> Sequence[SimulatedRecord]:
        stmt = select(SimulatedRecord).order_by(SimulatedRecord.id.desc()).offset(skip).limit(limit)
        return self.db.execute(stmt).scalars().all()
