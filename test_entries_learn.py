import unittest
from entries_functions_combined import app, date, index
from flask import json

class MyTestClass(unittest.TestCase):
    entry = {
        "content":"Funny moments",
        "date":"Fri, 28 Sep 2018 00:00:00 GMT",
        "id":1,
        "title":"Funny moments"
    }
    def setUp(self):
        self.app = app.test_client()
    
    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome To myDiary', response.data.decode())
    
    def test_get_entries(self):
        response = self.app.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_single_entry(self):
        # response = self.app.post('/api/v1/entries/{}'.format(self.data[1]['entry_id']))
        response = self.app.post('/api/v1/entries',
                            content_type='application/json',
                            data=json.dumps(self.entry)
                            )
        get_response = self.app.get('/api/v1/entries/1')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_response.status_code, 200)
        # self.aseerti(get_response.data.decode(), {"entry": {"content": "New content added", "date": "Thursday.September.2018", "id": 3, "title": "Vivian In Andela"}})
    
    def test_post_entry(self):
        response = self.app.post('/api/v1/entries',
                            content_type='application/json',
                            data=json.dumps(self.entry)
                            )
        self.assertEqual(response.status_code, 201)
        #self.assertIn(response.data.decode(), {"entry":{"content":"Funny moments","date":"Friday.September.2018","id":3,"title":"Funny moments"}})
# def test_update_entry(self):
#     '''should return the modified entry'''
#     self.app.post('/api/v1/entries',
#                             content_type='application/json',
#                             data=json.dumps(self.entry)
#                             )
#     response_to_change = self.app.put('/api/v1/entries/1', data=
#                                     json.dumps({"content": "Funny momenModify Data","title": "Funny moments moments"}), 
#                                     content_type = 'application/json')
#     self.assertEqual(response_to_change.status_code, 200)




