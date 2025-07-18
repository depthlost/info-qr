
import uuid
from datetime import date
from typing import Optional, List

from sqlalchemy import String, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import db

from app.models import Contact, Medication
from app.models.contact import support_persons_association, other_professionals_association

class User(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(256))

    name: Mapped[str] = mapped_column(String(64))
    surname: Mapped[str] = mapped_column(String(64))
    preferred_name: Mapped[Optional[str]] = mapped_column(String(64))
    insurance_number: Mapped[Optional[str]] = mapped_column(String(64))
    birthdate: Mapped[Optional[date]] = mapped_column(Date)
    address: Mapped[Optional[str]] = mapped_column(String(256))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    nationality: Mapped[Optional[str]] = mapped_column(String(64))

    spoken_language: Mapped[Optional[str]] = mapped_column(String(64))
    communication_method: Mapped[Optional[str]] = mapped_column(String(64))
    needs_communication_assistant: Mapped[Optional[bool]] = mapped_column(Boolean)
    needs_continuous_support: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    emergency_contact_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('contact.id', ondelete='SET NULL')
    )
    emergency_contact: Mapped[Optional[Contact]] = relationship(
        'Contact',
        foreign_keys=[emergency_contact_id],
        cascade='all, delete'
    )
    support_persons: Mapped[List[Contact]] = relationship(
        'Contact',
        secondary=support_persons_association,
        back_populates='supported_user',
        cascade='all, delete'
    )

    religion: Mapped[Optional[str]] = mapped_column(String(64))
    spiritual_needs: Mapped[Optional[str]] = mapped_column(String(256))

    primary_care_physician_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('contact.id', ondelete='SET NULL')
    )
    primary_care_physician: Mapped[Optional[Contact]] = relationship(
        'Contact',
        foreign_keys=[primary_care_physician_id],
        cascade='all, delete'
    )
    other_professionals: Mapped[List[Contact]] = relationship(
        'Contact',
        secondary=other_professionals_association,
        back_populates='professional_user',
        cascade='all, delete'
    )
    
    allergies: Mapped[Optional[str]] = mapped_column(String(256))
    medical_procedure_instructions: Mapped[Optional[str]] = mapped_column(String(512))
    feeding_instructions: Mapped[Optional[str]] = mapped_column(String(256))
    medications: Mapped[List[Medication]] = relationship(
        'Medication',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    how_to_take_medication: Mapped[Optional[str]] = mapped_column(String(256))
    position_for_medication: Mapped[Optional[str]] = mapped_column(String(64))
    take_medication_with: Mapped[Optional[str]] = mapped_column(String(64))
    
    has_epilepsy: Mapped[Optional[bool]] = mapped_column(Boolean)
    convulsive_crisis_description: Mapped[Optional[str]] = mapped_column(String(512))
    non_convulsive_crisis_description: Mapped[Optional[str]] = mapped_column(String(512))
    other_relevant_info: Mapped[Optional[str]] = mapped_column(String(512))

    anxiety_care_instructions: Mapped[Optional[str]] = mapped_column(String(512))
    pain_detection_cues: Mapped[Optional[str]] = mapped_column(String(512))
    fear_detection_cues: Mapped[Optional[str]] = mapped_column(String(512))
    anger_detection_cues: Mapped[Optional[str]] = mapped_column(String(512))
    communication_instructions: Mapped[Optional[str]] = mapped_column(String(512))
    mobility: Mapped[Optional[str]] = mapped_column(String(256))
    personal_care: Mapped[Optional[str]] = mapped_column(String(256))
    vision_hearing: Mapped[Optional[str]] = mapped_column(String(256))
    eating_instructions: Mapped[Optional[str]] = mapped_column(String(256))
    drinking_instructions: Mapped[Optional[str]] = mapped_column(String(256))
    safety_measures: Mapped[Optional[str]] = mapped_column(String(512))
    toileting: Mapped[Optional[str]] = mapped_column(String(256))
    sleep_rest_routine: Mapped[Optional[str]] = mapped_column(String(256))

    likes: Mapped[Optional[str]] = mapped_column(String(256))
    dislikes: Mapped[Optional[str]] = mapped_column(String(256))
    notes: Mapped[Optional[str]] = mapped_column(String(512))
    useful_contacts_and_sites: Mapped[Optional[str]] = mapped_column(String(256))

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for attribute_name, attribute_value in kwargs.items():
            if not hasattr(self, attribute_name):
                raise AttributeError("'{}' object has no attribute '{}'".format(
                    self.__class__.__name__,
                    attribute_name
                ))

            setattr(self, attribute_name, attribute_value)
        
        db.session.commit()
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(self, id):
        return self.query.get(id)
    
    @classmethod
    def get_by_email(self, email):
        return self.query.filter_by(email=email).first()
    