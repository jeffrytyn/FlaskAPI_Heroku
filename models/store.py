
from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores' #required for flask-sqlAlc

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # finds items with foriegn key same as store id/many to one relationship
    # lazy is dynamic means the Item objects are not created for each item
    items = db.relationship("ItemModel", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # .all() then creates Item objects for the things in items
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  #SELECT * FROM tablename WHERE name=name LIMIT 1