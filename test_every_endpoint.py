import json
import pytest
import unittest
from entries_functions_combined import app
from datetime import datetime

#pytest.fixture provide a fixed baseline upon which tests can reliably and repeatedly executed
@pytest.fixture
def client(request):
    test_client = app.test_client()
    return test_client

def post_json(client, url, json_dict):
    return client.post(url, data = json.dumps(json_dict),
                       content_type='application/json')

def json_reply(reponse):
    return json.loads(reponse.data.decode('utf8'))

def test_get_all_entries(client):
    reponse = client.get('http://127.0.0.1:8080/api/v1/entries')
    assert reponse.status_code == 200

def test_add_entry(client):
    response = post_json(client, 'http://127.0.0.1:8080/api/v1/entries',
                        {"title":'Vivian In Andela',"content": 'New content added'})
    assert response.status_code == 200
    assert json_reply(response) == {"entry": {"content": "New content added", "date": "Wednesday.September.2018", "id": 3, "title": "Vivian In Andela"}}
    # client.delete('http://127.0.0.1:8080/api/v1/entries')

def test_get_entry(client):
    '''Create entry that has an id of one, changing previous content id to 2'''
    post_response = post_json(client, 'http://127.0.0.1:8080/api/v1/entries', 
             {"content": "Funny moments","title": "Funny moments"})
    id = 1
    get_response = client.get('http://127.0.0.1:8080/api/v1/entries/1')
    print(get_response)
    assert post_response.status_code == 200
    assert get_response.status_code == 200
    # client.delete('http://127.0.0.1:8080/api/v1/entries/1')

def test_modifiy_entry(client):
    post_json(client, 'http://127.0.0.1:8080/api/v1/entries', 
             {"content": "Funny moments","title": "Funny moments"})
    response_to_change = client.put('http://127.0.0.1:8080/api/v1/entries/1', data=
                                    json.dumps({"content": "Funny momenModify Data","title": "Funny moments moments"}), 
                                    content_type = 'application/json')
    assert response_to_change.status_code == 200

def test_delete_entry(client):
    '''Create entry that has an id of one, changing previous content id to 2'''
    post_response = post_json(client, 'http://127.0.0.1:8080/api/v1/entries', 
             {"content": "Funny moments","title": "Funny moments"})
    id = 1
    get_response = client.get('http://127.0.0.1:8080/api/v1/entries/1')
    assert post_response.status_code == 200
    assert get_response.status_code == 200
    response = client.delete('http://127.0.0.1:8080/api/v1/entries/1')
    assert json_reply(response) == {"Result": 'entry successfully deleted'}

if __name__ == '__main__':
    unittest.main()
    

