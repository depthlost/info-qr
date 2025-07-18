
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import db

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

class Contact(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    relation: Mapped[str] = mapped_column(String(64))
    address: Mapped[str] = mapped_column(String(256))
    phone: Mapped[str] = mapped_column(String(20))

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
