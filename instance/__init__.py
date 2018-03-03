from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config#dict with all the configurations

#initialize the sqlalchemy
db=SQLAlchemy()


def create_app(config_name):
    #create flaskapi instance
    app=FlaskAPI(__name__,instance_relative_config=True)
    
    #load up the configuration on the app
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #connect it to the db
    db.init_app(app)

    #return app
    return app