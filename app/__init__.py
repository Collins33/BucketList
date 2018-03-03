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




    @app.route('/bucketlists/<int:id>', methods=['GET','PUT','DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        #this method takes an id as argument

        #first it retrieves a bucketlist based on the id
        #it queries the db based on id
        bucketlist=Bucketlist.query.filter_by(id=id).first()

        if not bucketlist:
            #if no bucket is found abort with 404
            abort(404)

        if request.method == "DELETE":
            #if the request method is delete
            #call the delete() on the bucketlist
            bucketlist.delete()

            return {"message":"bucketlist {} successfully deleted".format(bucketlist.id)},200

        elif request.method == "PUT":
            #IF THE REQUEST IS FOR UPDATING THE BUCKETLIST
            #GET THE NAME FROM THE REQUEST
            name=str(request.data.get('name',''))
            bucketlist.name = name
            bucketlist.save()

            response=jsonify({
                'id':bucketlist.id,
                'name':bucketlist.name,
                'date_created':bucketlist.date_created,
                'date_modified':bucketlist.date_modified
            })
            response.status_code=200
            return response

        else:
            response=jsonify({
                'id':bucketlist.id,
                'name':bucketlist.name,
                'date_created':bucketlist.date_created,
                'date_modified':bucketlist.date_modified
            })
            return response

                              
    
    #return app
    return app

    