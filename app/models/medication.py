
import uuid
from typing import Optional

from sqlalchemy import func, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import db
from app.models import Model

class Medication(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="medications")
    name: Mapped[Optional[str]] = mapped_column(Text)
    dosage: Mapped[Optional[str]] = mapped_column(Text)
    schedule: Mapped[Optional[str]] = mapped_column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dosage": self.dosage,
            "schedule": self.schedule
        }

    @classmethod
    def get_count_by_user_id(self, user_id):
        return db.session.query(func.count()).select_from(self) \
            .filter_by(user_id=user_id).scalar()
    