import re


# CATEGORY_MAP = {
#     "STARBUCKS": "Coffee/Food",
#     "UBER": "Transport",
#     "NETFLIX": "Entertainment",
#     "AMAZON": "Shopping",
# }

CATEGORY_RULES = [
    # --- Transportation ---
    ("Transportation", [
        r"MTA\*NYCT",
        r"UBER",
        r"LYFT",
    ]),

    # --- Dining ---
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

    # --- Groceries ---
    ("Groceries", [
        r"KEY FOOD",
        r"H MART",
        r"CVS",
    ]),

    # --- Shopping / Retail ---
    ("Shopping", [
        r"TARGET",
        r"TESO MINI",
        r"SUNRISE GIFT",
    ]),

    # --- Entertainment / Subscriptions ---
    ("Subscriptions", [
        r"SPOTIFY",
    ]),

    # --- Health ---
    ("Health", [
        r"USLIFE INSURANCE",
        r"PHARMACY",
    ]),

    # --- Peer-to-peer ---
    ("P2P Transfers", [
        r"VENMO",
        r"ZELLE",
    ]),

    # --- Savings ---
    ("Savings", [
        r"TRANSFER TO SAV",
        r"SAV",
    ]),

    # --- Investments ---
    ("Investments", [
        r"VANGUARD",
    ]),

    # --- Debt / Credit Cards ---
    ("Debt Payments", [
        r"PAYMENT TO CRD",
    ]),

    # --- Internal bank programs ---
    ("Rounding Transfers", [
        r"KEEP THE CHANGE",
    ]),

    # --- Checks ---
    ("Checks", [
        r"CHECK",
        r"Check number",
    ]),
]


SUGGESTED_PERCENTAGES = {
    "Housing": (25,30),
    "Savings": (10,20),
    "Food": (10,15),
    "Transportation": (10,15),
    "Insurance": (10,25),
    "Utilities": (5,10),
    "Medical": (5,10),
    "Personal/Recreation": (5,10),
    "Giving": (1,10),
    "Dining":(1,10),
    "Other":(1,10)
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

    for category, patterns in CATEGORY_RULES:
        for pattern in patterns:
            if re.search(pattern, desc):
                return category

    return "Other"