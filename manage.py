import os
import unittest
from flask_script import Manager#class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

#initialize the app with all configurations
app=create_app(config_name=os.getenv("APP_SETTINGS"))

#CREATE MIGRATE OBJECT
migrate=Migrate(app,db)

#create manager object that will handle our commands
manager=Manager(app)

#add migration command that will be preceded by db
#eg python manage.py db init
manager.add_command("db", MigrateCommand)



#define a method to run tests called test
#usage: python manage.py test
@manager.command#this decorator allows us to run  a command called test
def test():
    #first load the test from the test folder
    tests=unittest.TestLoader().discover('./tests', pattern='test*.py')
    #run the test using the TextTestRunner
    result=unittest.TextTestRunner(verbosity=2).run(tests)

    #if it is successful it will return 0
    if result.wasSuccessful():
        return 0
    return 1    


if __name__ == '__main__':
    manager.run()