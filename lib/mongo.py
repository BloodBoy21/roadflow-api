import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")


client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[MONGO_DB]
