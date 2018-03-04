import unittest
import json
from app import create_app,db

class AuthTestCase(unittest.TestCase):
    #test case for authentication blueprint

    def setUp(self):
        #set up test variables
        self.app=create_app(config_name="testing")
        #initialize test client
        self.client=self.app.test_client

        #user data to be used for tests
        self.user_data={
            'email':'collins@example.com',
            'password':'test_password'
        }

        with self.app.app_context():
            #create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        #tests if user registers well

        #make a post request to the database
        res=self.client().post('/auth/register', data=self.user_data)

        #get result returned in json format
        result=json.loads(res.data.decode())

        #assert that the result contains a success message
        self.assertEqual(result['message'], 'you have registered')
        #assert the status code
        self.assertEqual(res.status_code,201)        