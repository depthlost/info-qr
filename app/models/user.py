
import uuid
from datetime import date
from typing import Optional, List

from sqlalchemy import Text, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Model, Contact, Medication
from app.models.contact import support_persons_association, other_professionals_association

class User(Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    surname: Mapped[str] = mapped_column(String(64))

    name: Mapped[str] = mapped_column(Text)
    preferred_name: Mapped[Optional[str]] = mapped_column(Text)
    insurance_number: Mapped[Optional[str]] = mapped_column(Text)
    birthdate: Mapped[Optional[date]] = mapped_column(Date)
    address: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(Text)
    nationality: Mapped[Optional[str]] = mapped_column(Text)

    spoken_language: Mapped[Optional[str]] = mapped_column(Text)
    communication_method: Mapped[Optional[str]] = mapped_column(Text)
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

    religion: Mapped[Optional[str]] = mapped_column(Text)
    spiritual_needs: Mapped[Optional[str]] = mapped_column(Text)

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
    
    allergies: Mapped[Optional[str]] = mapped_column(Text)
    medical_procedure_instructions: Mapped[Optional[str]] = mapped_column(Text)
    feeding_instructions: Mapped[Optional[str]] = mapped_column(Text)
    medications: Mapped[List[Medication]] = relationship(
        'Medication',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    how_to_take_medication: Mapped[Optional[str]] = mapped_column(Text)
    position_for_medication: Mapped[Optional[str]] = mapped_column(Text)
    take_medication_with: Mapped[Optional[str]] = mapped_column(Text)
    
    has_epilepsy: Mapped[Optional[bool]] = mapped_column(Boolean)
    convulsive_crisis_description: Mapped[Optional[str]] = mapped_column(Text)
    non_convulsive_crisis_description: Mapped[Optional[str]] = mapped_column(Text)
    other_relevant_info: Mapped[Optional[str]] = mapped_column(Text)

    anxiety_care_instructions: Mapped[Optional[str]] = mapped_column(Text)
    pain_detection_cues: Mapped[Optional[str]] = mapped_column(Text)
    fear_detection_cues: Mapped[Optional[str]] = mapped_column(Text)
    anger_detection_cues: Mapped[Optional[str]] = mapped_column(Text)
    communication_instructions: Mapped[Optional[str]] = mapped_column(Text)
    mobility: Mapped[Optional[str]] = mapped_column(Text)
    personal_care: Mapped[Optional[str]] = mapped_column(Text)
    vision_hearing: Mapped[Optional[str]] = mapped_column(Text)
    eating_instructions: Mapped[Optional[str]] = mapped_column(Text)
    drinking_instructions: Mapped[Optional[str]] = mapped_column(Text)
    safety_measures: Mapped[Optional[str]] = mapped_column(Text)
    toileting: Mapped[Optional[str]] = mapped_column(Text)
    sleep_rest_routine: Mapped[Optional[str]] = mapped_column(Text)

    likes: Mapped[Optional[str]] = mapped_column(Text)
    dislikes: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    useful_contacts_and_sites: Mapped[Optional[str]] = mapped_column(Text)

    def __init__(self, *args, **kwargs):
        emergency_contact = kwargs.pop("emergency_contact", Contact())
        primary_care_physician = kwargs.pop("primary_care_physician", Contact())

        super().__init__(
            *args,
            emergency_contact=emergency_contact,
            primary_care_physician=primary_care_physician,
            **kwargs
        )

    def get_contact_by_id(self, contact_id, contact_type=None):
        if contact_type is None:
            contacts = [self.emergency_contact, self.primary_care_physician] + \
                self.support_persons + self.other_professionals
        else:
            contacts = [
                *([self.emergency_contact] if "emergency_contact" in contact_type else []),
                *([self.primary_care_physician] if "primary_care_physician" in contact_type else []),
                *(self.support_persons if "support_persons" in contact_type else []),
                *(self.other_professionals if "other_professionals" in contact_type else [])
            ]

        return next((each for each in contacts if each.id == contact_id), None)

    @classmethod
    def get_by_email(self, email):
        return self.query.filter_by(email=email).first()
    