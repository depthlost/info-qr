
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import db

class User(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]

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
    