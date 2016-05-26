# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

from werkzeug import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'users'

    # User Name
    username  	= db.Column(db.String(128),  nullable=False, unique=True)
	
    # Real Name
    fullname    = db.Column(db.String(128),  nullable=False)
    
    # Identification Data: email
    email    = db.Column(db.String(128),  nullable=False, unique=True)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    def check_password(self, password):
    	return check_password_hash(self.password, password)
	
    def set_password(self, password):
    	self.password = generate_password_hash(password)


    # New instance instantiation procedure
    def __init__(self, id, username, fullname,  email, role = 0, status = 1):

	self.id	      = id
        self.username = username
        self.fullname = fullname
        self.email    = email.lower()
	self.role     = role
	self.status   = status

    def __repr__(self):
        return '<User %r>' % (self.name) 


class Deposit(Base):

	__tablename__ = "deposit"

	user_id  = db.Column(db.Integer, ForeignKey('users.id'))

	admin_id = db.Column(db.Integer, ForeignKey('users.id'))

	amount   = db.Column(db.Integer, nullable=False)

	user = relationship("User", primaryjoin = "Deposit.user_id == User.id")
	admin = relationship("User", primaryjoin = "Deposit.admin_id == User.id")


   	def __init__(self, user_id, admin_id, amount):

        	self.user_id  = user_id
        	self.admin_id = admin_id
        	self.amount   = amount

	#def __repr__(self):
	#	return '<Deposit %r>' % (self.amount)

	def to_dict(self):
		return {'id':self.id, 'date': self.date_created.strftime("%Y-%m-%d %H:%M:%S"), 'user':self.user.fullname, 'admin':self.admin.fullname, 'amount':self.amount}


class Coffee(Base):

	__tablename__ = "coffee"

		
	user_id	 = db.Column(db.Integer, ForeignKey('users.id'))
	price	 = db.Column(db.Integer, nullable=False)

	user = relationship("User", primaryjoin = "Coffee.user_id == User.id")

	def __init__(self, user_id, price):
		
		self.user_id = user_id
		self.price   = price

	def __repr__(self):
		return '<User %d, price %d>' % (self.user_id, self.price)


	def to_dict(self):
		return {'id':self.id, 'date': self.date_created.strftime("%Y-%m-%d %H:%M:%S"),'price':self.price}
