from app import db#import the db
from flask_bcrypt import Bcrypt


#create the user model
#the bucketlists will belong to a user
class User(db.Model):
    __tablename__ = 'users'#name of the table in the database

    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(256),nullable=False,unique=True)
    password=db.Column(db.String(256),nullable=False)
    #relationship with bucketlist
    bucketlists=db.relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")


    def __init__(self,email,password):
        #initializes user with password and email
        self.email=email
        self.password=Bcrypt().generate_password_hash(password).decode()#this hashes the password


    def password_is_valid(self,password):
        #checks password against its hash to validate user password
        return Bcrypt().check_password_hash(self.password,password)

    def save(self):
        #save a user to the database
        db.session.add()
        db.session.commit()    




#create a class that inherits from db.Model

class Bucketlist(db.Model):

    #initialize a table name
    __tablename__ = 'bucketlists'#the name of the table in the db

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(300))
    date_created=db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    created_by = db.Column(db.Integer, db.ForeignKey(User.id))   


    def __init__(self,name):
        #initilizes with a name
        self.name=name


    def save(self):
        #saves the bucketlist into a database
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        #will query the database for all the bucketlists of a user
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        #will delete a bucketlist from the db
        db.session.delete(self)
        db.session.commit() 


    def __repr__(self):
        return "<Bucketlist:{}>".format(self.name)  










