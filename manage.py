import os
from flask_script import Manager#class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

app=create_app(config_name=os.getenv("APP_SETTINGS"))

#CREATE MIGRATE OBJECT
migrate=Migrate(app,db)

#create manager object
manager=Manager(app)

#add migration commansd
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()