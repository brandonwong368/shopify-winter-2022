from app import app
from flask import request, render_template
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util
import json
import stripe
import app.validate as validate

# connect to MongoDB
load_dotenv()
API_KEY = os.getenv("API_KEY")
cluster = MongoClient(API_KEY)
db = cluster["images"]
image_collection = db["images"]

# load stripe keys
stripe_keys = {
    "secret_key": os.environ["SECRET_KEY"],
    "publishable_key": os.environ["PUBLISHABLE_KEY"],
}
stripe.api_key = stripe_keys["secret_key"]

# TODO: add validation/error handling of request bodies

# insert a document into the database
# pass in JSON body with document details
@app.route("/add", methods=["POST"])
def add():
    body = request.get_json(force=True)
    error = validate.validateAdd(body)
    if error:
        return error
    else:
        document = image_collection.find_one(body)
        if document:
            # if image exists in repository, increment inventory
            image_collection.update_one(
                body, {"$set": {"inventory": document["inventory"] + 1}}
            )
            return "Image exists and inventory was increased!"
        else:
            # else, add a new image document with inventory = 1
            body["inventory"] = 1
            image_collection.insert_one(body)
            return "New image created successfully!"


# delete a document into the database matching JSON body
@app.route("/delete", methods=["DELETE"])
def delete():
    body = request.get_json(force=True)
    document = image_collection.find_one(body)
    if not document:
        return "Image does not exist!"
    else:
        image_collection.delete_one(body)
        return "Image deleted successfully!"


# return a document matching JSON body
@app.route("/search", methods=["GET"])
def search():
    body = request.get_json(force=True)
    document = image_collection.find_one(body)
    if not document:
        return "Image does not exist!"
    else:
        return json.loads(json_util.dumps(document))


@app.route("/buy", methods=["POST"])
def buy():
    # receive image link name and reduce inventory
    body = request.get_json(force=True)
    document = image_collection.find_one(body)

    if document:
        inventory = document["inventory"]
        if inventory > 0:
            image_collection.update_one(body, {"$set": {"inventory": inventory - 1}})
            amount = document["cost"] / 100
            return render_template(
                "index.html", amount=amount, key=stripe_keys["publishable_key"]
            )
        else:
            return "Image is not in stock!"
    else:
        return "Image does not exist in repository"


# confirm that the transaction was completed
@app.route("/confirm", methods=["POST"])
def charge():
    return render_template("confirm.html")
