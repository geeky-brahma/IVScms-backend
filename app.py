import json
from flask import Flask, request
import flask
from flask_cors import CORS
import pymongo
import sys
from bson.json_util import dumps, loads 
import os
from dotenv import load_dotenv



load_dotenv()

def connect_pymongo():
    
    # uri=
    uri = os.environ.get("MONGO_URI")
    try:
        client = pymongo.MongoClient(uri)
        db = client.IVSComplaints
        my_collection = db["complaints"]
        return db, my_collection
    
    # return a friendly error if a URI error is thrown 
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)

app = Flask(__name__)
CORS(app)
@app.route("/")
def hello():
    return "Hello, World!"
    # var = driver("hello")
    # return var

@app.route('/data', methods=["GET","POST"])
def data():
    print("summary endpoint reached...")
    if request.method == "GET":
        return "Hello"
    
    if request.method == "POST":
        json_data = request.get_json()
        print(f"received data: {json_data}")
        db, collection = connect_pymongo()
        result = collection.insert_one(json_data)

        
        return_data = {
            "status": "success",
            "summary": "data received"
        }
        
        return flask.Response(response=json.dumps(return_data), status=201)

@app.route('/status', methods=["POST"])
def status():
    if request.method == "POST":
        json_data = request.get_json()
        print(f"received data: {json_data}")
        searchBy = json_data['searchBy']
        db, collection = connect_pymongo()
        if searchBy == 'bankCode':
            result = collection.find({"bankNo":json_data["searchValue"]})
        else:
            result = collection.find({"complaint_id":json_data["searchValue"]})
        list_cur = list(result) 
        js_data = json.loads(dumps(list_cur)) 
        print(js_data)

        
        
        return_data = {
            "status": "success",
            "summary": "data received",
            "data": js_data
        }
        
        return flask.Response(response=json.dumps(return_data), status=201)

@app.route('/all_complaints', methods=["GET"])  
def all_complaints():
    db, collection = connect_pymongo()
    query = "SELECT * FROM complaints order by id desc"
    # cursor.execute(query)
    result = collection.find()
    list_cur = list(result) 
    js_data = json.loads(dumps(list_cur)) 
    print(js_data)
    
    data_json = {
        "data": js_data
    }
    return flask.Response(response=json.dumps(data_json), status=200)

@app.route('/edit_complaint', methods=["GET","POST"])
def edit_complaints():
    if request.method == "GET":
        search_type = request.args.get('searchType')
        searchValue = request.args.get('searchValue')
        db, collection = connect_pymongo()
        result = collection.find({"complaint_id":searchValue})
        list_cur = list(result) 
        js_data = json.loads(dumps(list_cur)) 
        print(js_data)
        return_data = {
            "status": "success",
            "summary": "data received",
            "data": js_data
        }
        return flask.Response(response=json.dumps(return_data), status=201)
    if request.method == "POST":
        json_data = request.get_json()
        print(f"received data: {json_data}")
        complaintID = json_data['complaintID']
        
        option = json_data['option']
        db, collection = connect_pymongo()
        if (option == 'markAsComplete'):
            status = json_data['status']
            result = collection.find({"complaint_id":complaintID})
            docID = result[0]['_id']
            filter = { "_id": docID }  # Filter for the document to update
            update = { "$set": { "status": "Completed" } }  # The update operation
            result = collection.update_one(filter, update)
        else:
            actionTaken = json_data['actionTaken']
            print(actionTaken)
            result = collection.find({"complaint_id":complaintID})
            docID = result[0]['_id']
            filter = { "_id": docID }  # Filter for the document to update
            update = { "$set": { "action-taken": actionTaken } }  # The update operation
            result = collection.update_one(filter, update)
        result = collection.find({"complaint_id":complaintID})
        list_cur = list(result) 
        js_data = json.loads(dumps(list_cur)) 
        print(js_data)
        return_data = {
            "status": "success",
            "summary": "data received",
            "data": js_data
        }
        return flask.Response(response=json.dumps(return_data), status=201)

if __name__ == '__main__':
    app.run()
    
    
    