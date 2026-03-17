
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
load_dotenv()
uri=f"mongodb+srv://eninam:{os.environ.get("mango_db_password")}@financialreport.o0ragtc.mongodb.net/?appName=financialReport"
client = MongoClient(uri,tlsCAFile=certifi.where())
db = client["financialReport"]
collection = db["categories"]

CATEGORY_RULES = [
    ("Transportation", [
        r"MTA\*NYCT",
        r"UBER",
        r"LYFT",
    ]),
    ("Dining", [
        r"MCDONALD",
        r"SHAKE SHACK",
        r"POKE BOWL",
        r"PIZZA",
        r"BAKERY",
        r"CAFE",
        r"SQ \*",
        r"TST\*",
        r"RESTAURANT",
        r"BRULEE",
        r"HEYTEA",
        r"PANINERIA",
        r"LADUREE",
        r"XI'AN",
        r"ORWASHERS",
        r"CHEF TAN",
    ]),
    ("Groceries", [
        r"KEY FOOD",
        r"H MART",
        r"CVS",
    ]),
    ("Shopping", [
        r"TARGET",
        r"TESO MINI",
        r"SUNRISE GIFT",
    ]),
    ("Subscriptions", [
        r"SPOTIFY",
    ]),
    ("Health", [
        r"USLIFE INSURANCE",
        r"PHARMACY",
    ]),
    ("P2P Transfers", [
        r"VENMO",
        r"ZELLE",
    ]),
    ("Savings", [
        r"TRANSFER TO SAV",
        r"SAV",
    ]),
    ("Investments", [
        r"VANGUARD",
    ]),
    ("Debt Payments", [
        r"PAYMENT TO CRD",
    ]),
    ("Rounding Transfers", [
        r"KEEP THE CHANGE",
    ]),
    ("Checks", [
        r"CHECK",
        r"Check number",
    ]),
]


def seed_categories():

    for category, patterns in CATEGORY_RULES:
        for pattern in patterns:
            cat_object = {
                "merchant": pattern,
                "category": category
            }
            collection.update_one(
                {"merchant": pattern}, 
                {"$set": {"category": category}}, 
                upsert=True)
            print(f"cat object {cat_object} inserted")

    collection.create_index("merchant")
    print(f"Inserted  category rules")


if __name__ == "__main__":
    seed_categories()