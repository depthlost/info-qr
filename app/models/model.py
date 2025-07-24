
from app.database import db

class Model(db.Model):
    __abstract__ = True
    
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
    def update_by_id(self, id, data):
        if self.query.filter_by(id=id).update(data) == 0:
            db.session.rollback()
            return False
        
        db.session.commit()
        return True
