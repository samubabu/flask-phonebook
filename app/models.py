from datetime import datetime
from werkzeug.security import generate_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    first = db.Column(db.String(50), nullable=False, unique=True)
    last = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
      # Add and commit the new instance to the database
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.phone




