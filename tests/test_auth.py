import unittest
import json
import os
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

        res = self.client().post('/auth/register', data=self.user_data)
        # get the results returned in json format
        # result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        # # assert that the request contains a success message and a 201 status code
        # self.assertEqual(result['message'], "You registered successfully.")
        self.assertEqual(res.status_code, 201)


    def test_already_registered_user(self):
        #test that a user cannot be registered twice
        # 
        # make post request
        res=self.client().post('/auth/register', data=self.user_data)
        #assert the request is successful
        self.assertEqual(res.status_code,201)

        #make second post request with same user data
        second_res=self.client().post('/auth/register', data=self.user_data)

        #assert the status code of the second post request
        self.assertEqual(second_res.status_code,202)

        #get result from second request in json
        result=json.loads(second_res.data.decode())

        self.assertEqual(result['message'], 'User already exists')            