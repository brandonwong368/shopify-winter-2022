from app import app
from flask import request
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
from bson import json_util
import json

# connect to MongoDB
load_dotenv()
API_KEY = os.getenv('API_KEY')
cluster = MongoClient (API_KEY)
db = cluster["images"]
image_collection = db["images"]

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

# insert a document into the database
@app.route('/add' , methods=["POST"])
def add():
    body = request.get_json(force=True)
    image_collection.insert_one(body)

    return "Document uploaded successfully"

@app.route("/delete" , methods = ["DELETE"])
def delete():
    body = request.get_json(force=True)
    image_collection.delete_one(body)

    return "Document deleted successfully"

@app.route("/search", methods = ["GET"])
def search():
    body = request.get_json(force=True)
    document = image_collection.find_one(body)
    return json.loads(json_util.dumps(document))