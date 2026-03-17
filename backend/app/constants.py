import os
from dotenv import load_dotenv

load_dotenv()
BOFA_BEGINING_BALANCE = "Beginning balance"
BOFA_DEPOSITS = "Deposits and other additions"
TOTAL = "Total"
MONGO_URI = f"mongodb+srv://eninam:{os.environ.get("mango_db_password")}@financialreport.o0ragtc.mongodb.net/?appName=financialReport"
DATABASE = "financialReport"
CAT_COLLECTION = "categories"