from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db , login


class Sign(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    users = db.relationship('User', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the password to the hashed version of the password
        self.password = self.set_password(kwargs.get('password', ''))
        # Add and commit the new instance to the database
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.username

    def set_password(self, plain_password):
        return generate_password_hash(plain_password)

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

@login.user_loader
def load_user(sign_id):
    return Sign.query.get(sign_id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    first = db.Column(db.String(50), nullable=False, unique=True)
    last = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id')) # SQL equivalent to FOREIGN KEY(user_id) REFERENCES user(id)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
      # Add and commit the new instance to the database
        db.session.add(self)
        db.session.commit()

    def __self__(self):
        return self.phone

    
    # Update method for the Post object
    def update(self, **kwargs):
        # for each key value that comes in as a keyword argument
        for key, value in kwargs.items():
            # if the key is 'first', 'last' etc
            if key in {'first', 'last', 'phone', 'address'}:
                # Then we will set that attribute on the instance e.g. user.phone = 'Updated Title'
                setattr(self, key, value)
        # Save the updates to the database
        db.session.commit()

    # Delete post from database
    def delete(self):
        db.session.delete(self)
        db.session.commit()



