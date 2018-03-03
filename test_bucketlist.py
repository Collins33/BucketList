import unittest
import os
import json

from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    #this class rep the bucketlist tests

    def setUp(self):
        #define the test variables and initialize the app
        self.app=create_app(config_name="testing")
        #test client
        self.client=self.app.test_client

        self.bucketlist={"name":"Get into andela"}

        #bind the app to the current context
        with self.app.app_context():
            #create all the tables
            db.create_all()


    def test_bucketlist_creation(self):
        #make a post request to the bucketlist url
        res=self.client().post('/bucketlists/', data=self.bucketlist)

        #assert the request status
        self.assertEqual(res.status_code, 201)

        #check the response value
        self.assertIn("Get into andela",str(res.data))


    def test_api_can_get_all_bucketlists(self):
         #test if the api can get all the bucketlists

         #make a post request
        res=self.client().post('/bucketlists/', data=self.bucketlist)

        #ensure the post request was successful
        self.assertEqual(res.status_code, 201)

        #make get request to get all saved bucketlists
        results=self.client.get('/bucketlists/')
        #ensure the get request was successful
        self.assertEqual(results.status_code,200)

        self.assertIn('Get into andela', str(results.data))
