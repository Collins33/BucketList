from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config#dict with all the configurations

from flask import request,jsonify,abort

#initialize the sqlalchemy
db=SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist
    #create flaskapi instance
    app=FlaskAPI(__name__,instance_relative_config=True)
    
    #load up the configuration on the app
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #connect it to the db
    db.init_app(app)

    @app.route('/bucketlists/', methods=["POST", "GET"])
    def bucketlists():
        #check the type of request it receives
        if request.method == "POST":
            #CREATE BUCKETLIST OBJECT BY EXTRACTING NAME FROM THE REQUEST
            name=str(request.data.get('name',''))
            if name:
                bucketlist=Bucketlist(name=name)
                #save the created bucketlist
                bucketlist.save()
                response= jsonify({
                    'id':bucketlist.id,
                    'name':bucketlist.name,
                    'date_created':bucketlist.date_created,
                    'date_modified':bucketlist.date_modified
                })
                response.status_code= 201
                return response

        #if request method is get
        else:
            bucketlists=Bucketlist.get_all()#this returns a list

            results=[] 
            #iterate over the list of bucketlists
            for bucketlist in bucketlists:
                obj={
                    'id':bucketlist.id,
                    'name':bucketlist.name,
                    'date_created':bucketlist.date_created,
                    'date_modified':bucketlist.date_modified
                }
                results.append(obj)

            response=jsonify(results)
            response.status_code=200
            return response           
    

    #return app
    return app

    