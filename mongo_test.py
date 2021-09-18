import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')

cluster = MongoClient (API_KEY)

db = cluster["images"]
collection = db["images"]

post = {"_id" : 0, "link" : "test"}
x = collection.find_one()

print (x)
#collection.insert_one(post)