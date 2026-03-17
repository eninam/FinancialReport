import re
from pymongo import MongoClient
import constants
import certifi
from mangoDB.load_categories import get_rules, MERCHANT_RULES
from LLM.unknown_merchant_cat import ai_classify



client = MongoClient(constants.MONGO_URI,tlsCAFile=certifi.where())
db = client[constants.DATABASE]
merchant_collection = db[constants.CAT_COLLECTION]

SUGGESTED_PERCENTAGES = {
    "Transportation": (10, 15),
    "Dining": (5, 10),
    "Groceries": (8, 15),
    "Shopping": (5, 15),
    "Subscriptions": (1, 5),
    "Health": (5, 10),
    "P2P Transfers": (0, 10),
    "Savings": (10, 20),
    "Investments": (5, 20),
    "Debt Payments": (5, 20),
    "Rounding Transfers": (0, 5),
    "Checks": (0, 10),
}


def normalize_description(transaction: dict) -> str:
    """
    Normalize transaction description for reliable matching.
    """
    desc = transaction["description"].upper()
    desc = re.sub(r"\s+", " ", desc)
    return desc


def categorize(transaction: dict) -> str:
    desc = normalize_description(transaction)

    for rule in get_rules():
        merchant = rule["merchant"]

        if merchant is not None and merchant in desc:
            print('in merchant rule ', merchant, ' category ', rule["category"])
            return rule["category"]

    return categorize_with_ai(desc)

def categorize_with_ai(description):
    try:
        merchant, category = ai_classify(description)
        print(f'categorize_with_ai  category {category}, merchant {merchant}')
        merchant_collection.update_one(
            {"merchant": merchant}, 
            {"$set": {"category": category}}, 
            upsert=True
        )
        if MERCHANT_RULES is not None:
            MERCHANT_RULES.append({
                "merchant": merchant,
                "category": category
            })

        return category
    except Exception as e:

        print(f"AI categorization failed: {e}")

        return "Other"