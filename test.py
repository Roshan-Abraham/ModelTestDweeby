# app.py

# Required imports
from ModelIO import PredCluster
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from ModelIO import PredCluster
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('DummyMLAIHardik')

@app.route('/add', methods=['GET', 'POST'])
def create():

    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
def reader():

    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
            # return str(type(all_todos))
    except Exception as e:
        return str(e)

@app.route('/fire', methods=['GET'])
def fire():

    try:
        # Check if ID was passed to URL query
        

        todo_id = request.args.get('id')
        # if todo_id:
        todo = todo_ref.document(todo_id).stream()
        # print(todo)

                # self.users_ref = db.collection(u'DummyMLAIHardik').stream()
        # self.docs = self.users_ref.stream()
        tests = []
        for doc in todo:
            tests["Drinking"] = u'{}'.format(doc.to_dict()['d'])
            tests["Smoking"] = u'{}'.format(doc.to_dict()['s'])
            tests["Gender"] = u'{}'.format(doc.to_dict()['g'])
            tests["Name"] = u'{}'.format(doc.to_dict()['n'])
            tests["Id"] = u'{}'.format(doc.id)
        # return jsonify(todo.to_dict()), 200
        return str(tests), 200
        # else:
        #     all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        #     # return jsonify(all_todos), 200
        #     return str(type(all_todos))
    except Exception as e:
        return str(e)

@app.route('/update', methods=['GET', 'POST', 'PUT'])
def update():

    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return ("An Error Occured:")

@app.route('/model', methods=['GET'])
def read():
    def PushIt(todo_id, cluster):
        id = todo_id
        todo_ref.document(id).set(cluster)
        # return jsonify({"success": True}), 200
    try:

        todo_id = request.args.get('id')
        # if todo_id:
        todo = todo_ref.document(todo_id).get()
            # return jsonify(todo.to_dict()), 200

        all_todos = [todo.to_dict()]
        df = pd.DataFrame.from_dict(all_todos)
        cluster = PredCluster(df)
        out = cluster.to_json()
        # PushIt(todo_id, out)
        return str(out) #type(cluster), 200 #jsonify(todo.to_dict()), 200
        # else:
            # all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            # return type(all_todos) #, 200 #jsonify(all_todos), 200
    except Exception as e:
        return str(e)

@app.route('/multimodel', methods=['GET'])
def multiModel():
    def PushIt(todo_id, cluster):
        id = todo_id
        todo_ref.document(id).set(cluster)
        # return jsonify({"success": True}), 200
    try:

        todo_id = request.args.get('id')
        # if todo_id:
        todo = todo_ref.document(todo_id).get()
            # return jsonify(todo.to_dict()), 200

        all_todos = [todo.to_dict()]
        df = pd.DataFrame.from_dict(all_todos)
        cluster = PredCluster(df)
        out = cluster.to_json()
        PushIt(todo_id, out)
        return str(out) #type(cluster), 200 #jsonify(todo.to_dict()), 200
        # else:
            # all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            # return type(all_todos) #, 200 #jsonify(all_todos), 200
    except Exception as e:
        return str(e)

@app.route('/type', methods=['GET'])
def types():

    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            x = type(todo)
            return jsonify(x), 200 #jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return str(type(all_todos)) #, 200 #jsonify(all_todos), 200
    except Exception as e:
        return str(e)

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=port)