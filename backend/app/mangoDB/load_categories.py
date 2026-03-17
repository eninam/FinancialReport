import constants
import certifi
from pymongo import MongoClient


client = MongoClient(constants.MONGO_URI,tlsCAFile=certifi.where())
db = client[constants.DATABASE]
merchant_collection = db[constants.CAT_COLLECTION]

MERCHANT_RULES = None


def load_rules():
    global MERCHANT_RULES
    MERCHANT_RULES = list(merchant_collection.find({}, {"_id": 0}))


def get_rules():
    global MERCHANT_RULES

    if MERCHANT_RULES is None:
        load_rules()
    return MERCHANT_RULES