from app import app
from flask import request
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util
import json


# connect to MongoDB
load_dotenv()
API_KEY = os.getenv('API_KEY')
cluster = MongoClient (API_KEY)
db = cluster["images"]
image_collection = db["images"]

# TODO: add validation of request bodies
# document structure: 
# {
#     link: string,
#     tags: [string],
#     cost : float,
#     inventory: int,
# }

# add error handling

# insert a document into the database
# pass in JSON body with document details
@app.route('/add' , methods=["POST"])
def add(): 
    body = request.get_json(force=True)
    document = image_collection.find_one(body)
    if document:
        # if image exists in repository, increment inventory
        image_collection.update_one(body, { "$set": { "inventory": document["inventory"]+1 } })
        return "Image exists and inventory was increased"
    else:
        # else, add a new image document with inventory = 1
        body["inventory"] = 1
        image_collection.insert_one(body)
        return "New image created successfully"
    
# delete a document into the database matching JSON body
@app.route("/delete" , methods = ["DELETE"])
def delete():
    body = request.get_json(force=True)
    image_collection.delete_one(body)

    return "Document deleted successfully"

# return a document matching JSON body
@app.route("/search", methods = ["GET"])
def search():
    body = request.get_json(force=True)
    document = image_collection.find_one(body)
    return json.loads(json_util.dumps(document))

@app.route("/buy" , methods = ["POST"])
def buy():
    # receive image link name and reduce inventory
    body = request.get_json(force=True)
    document = image_collection.find_one(body)
    if document:
        inventory = document["inventory"]
        if inventory > 0:
            image_collection.update_one(body, { "$set": { "inventory": inventory-1 } })
            return "Image succesfully bought!"
        else:
            return "Image is not in stock!"
    else:
        return "Image does not exist in repository"