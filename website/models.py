from . import db
from flask_login import UserMixin # Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users
                                  # Flask-login requires a User model with the following properties. UserMixin class provides the implementation of this properties
from sqlalchemy.sql import func   # this func auto add current date time against data save in DB.  


# The User will inherit database model and UserMixin . The UserMixin is for authentication purpose
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    # a sudo column in Note
    notes = db.relationship('Favourite_URL') # Telling ORM save data against user ID.
    note=db.relationship('Urls')             # Telling ORM save data against user ID.
    

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String())
    short = db.Column(db.String(6))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #Defult timezone func import used
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#foreign key relationship
# A foreign key is generally used to build a relationship between the two tables. The table allows only one primary key.


class Favourite_URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #Defult timezone func import used
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#foreign key relationship