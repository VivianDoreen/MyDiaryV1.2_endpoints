from flask import Flask, jsonify, abort,  make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

#__name__ is set to the name of the current class, function, method, descriptor, or generator instance.
#Flask  is the prototype used to create instances of web application or web applications if you want to put it simple.
#__name__ is a special variable that gets as value the string "__main__"
app = Flask(__name__)
date = datetime.now().date()
auth = HTTPBasicAuth()


entries = [
    {
        'id' : 1,
        'date':date,
        'title': "Funny moments",
        'content':'Funny moments'
    },
    {
    'id' : 2,
    'date':date,
    'title': "Funny moments",
    'content':'Funny moments'
    }
]

def make_public_entry(entry):
    new_entry = {}
    for field in entry:
        if field == 'id':
            new_entry['uri'] = url_for('get_entry', entry_id=entry['id'], _external=True)
        else:
            new_entry[field] = entry[field]
    return new_entry

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'entry not found':' please check id'}), 404)

@app.errorhandler(400)
def wrong_param(error):
    return make_response(jsonify({'entry not found':' Wrong params for json'}), 400)

@app.route('/')
def index():
    return 'Welcome To myDiary'

@app.route('/api/v1/entries', methods = ['GET'])
def get_entries():
    return jsonify({'Entries' : [make_public_entry(entry) for entry in entries]})

@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    entry = [each_entry for each_entry in entries if each_entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry':entry[0]})
@app.route('/api/v1/entries', methods=['POST'])
def create_entry():
    if not request.json or not 'title' in request.json or not 'content' in request.json:
        abort(400)
    entry = {
        'id' : entries[-1]['id']+1,
        'date':date.strftime('%A.%B.%Y'),
        'title': request.json["title"],
        'content':request.json['content']
    }
    entry_title = [each_entry for each_entry in entries if each_entry['title'] == entry['title']]
    entry_content = [each_entry for each_entry in entries if each_entry['content'] == entry['content']]

    if len(entry_title) == 1 or len(entry_content) == 1:
        return "Entry already exists"
    entries.append(entry)
    return jsonify({'entry':entry}), 200

@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    entry[0]['title'] = request.json.get('title', entry[0]['title'])
    entry[0]['content'] = request.json.get('content', entry[0]['content'])
    return jsonify({'entry':entry[0]})

@app.route('/api/v1/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({"Result": 'entry successfully deleted'})
    
if __name__ == '__main__':
    #Debug will print out possible Python errors on the web page helping us trace the errors
    app.run(debug=True, port=8080)