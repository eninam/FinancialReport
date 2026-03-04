import re

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

    for category, patterns in CATEGORY_RULES:
        for pattern in patterns:
            if re.search(pattern, desc):
                return category

    return "Other"