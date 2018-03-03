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


    def test_api_can_get_bucketlist_by_id(self):
        #test if the api can get buckelist based on id
        
        #make a post request with the url
        rv=self.client().post('/bucketlists', data=self.bucketlist)
        #check status of the post request
        self.assertEqual(rv.status_code, 201)
        #convert response to json

        #this allows us to access the id
        result_in_json=json.loads(rv.data.decode('utf-8').replace("'", "\""))

        #make the get request using the id
        result=self.client().get('/bucketlists/{}'.format(result_in_json["id"]))


    def test_api_can_be_edited(self):
        #test if the api can edit the data

        #make a post request
        rv=self.client().post('/bucketlists/', data={"name":"Eat, pray and love"})
        #assert the status of the post request
        self.assertEqual(rv.status_code, 201)

        #put request to edit the data
        rv=self.client().put('/bucketlists/1', data={"name":"Dont just eat,but pray and love"})
        #assert the status of the put request
        self.assertEqual(rv.status_code, 200)

        results=self.client().get('/bucketlists/1')

        self.assertIn("Dont just eat", str(results.data))    

        #check status of get request
        self.assertEqual(result.status_code,200)

        #verify content of get request
        self.assertIn("Get into andela",str(result.data))



    def test_bucketlist_deletion(self):
        #make a post request
        rv=self.client().post('/bucketlists/', data={"name", "Eat pray and love"})
        #check status of the request
        self.assertEqual(rv.status_code,201)

        res=self.client().delete('/bucketlisys/1')
        #check status of the delete request
        self.assertEqual(res.status_code,200)

        #test to see if it exists, it should return 404
        results=self.client.get('/bucketlists/1')
        #status should be 404
        self.assertEqual(results.status_code,404)    
