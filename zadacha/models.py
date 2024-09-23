from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Item {self.name}>"

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        sqla_session = db.session
        include_fk = True
