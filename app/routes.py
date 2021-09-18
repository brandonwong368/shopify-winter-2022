from app import app
from flask import request
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

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
@app.route('/add ' , methods=["POST"])
def add():
    body = request.get_json(force=True)
    image_collection.insert_one(body)

    return "Document uploaded successfully"


@app.route("/delete_one" , methods = ["DELETE"])
def delete():

    return
