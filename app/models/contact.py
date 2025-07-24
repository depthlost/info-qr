
from typing import Optional

from sqlalchemy import Text, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import db
from app.models import Model

support_persons_association = Table(
    'support_persons',
    db.Model.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('contact_id', ForeignKey('contact.id'), primary_key=True)
)

other_professionals_association = Table(
    'other_professionals',
    db.Model.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('contact_id', ForeignKey('contact.id'), primary_key=True)
)

class Contact(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    relation: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(Text)

    supported_user: Mapped["User"] = relationship(
        "User",
        secondary=support_persons_association,
        back_populates="support_persons"
    )

    professional_user: Mapped["User"] = relationship(
        "User",
        secondary=other_professionals_association,
        back_populates="other_professionals"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "relation": self.relation,
            "address": self.address,
            "phone": self.phone
        }
