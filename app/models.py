from app import db#import the db

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


    def __init__(self,name):
        #initilizes with a name
        self.name=name


    def save(self):
        #saves the bucketlist into a database
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        #will query the database for all the bucketlists
        return Bucketlist.query.all()

    def delete(self):
        #will delete a bucketlist from the db
        db.session.delete(self)
        db.session.commit() 


    def __repr__(self):
        return "<Bucketlist:{}>".format(self.name)           




