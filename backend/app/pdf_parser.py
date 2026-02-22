import pdfplumber
from typing import List, Dict
import re
import constants

# extracts transactions and income
# only checking and savings



def extract_statement_data(pdf_bytes: bytes) -> Dict:
    transactions = []
    income = 0

    with pdfplumber.open(pdf_bytes) as pdf:
        first_page_text = pdf.pages[0].extract_text()

        for line in first_page_text.split("\n"):
            if constants.BOFA_BEGINING_BALANCE in line or constants.BOFA_DEPOSITS in line:
                income = income + contains_float(line)


        for page in pdf.pages[3:]:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                if line.startswith(constants.TOTAL):
                    continue
                amount = contains_float(line)
                if amount > 0:
                    transactions.append({
                        "description": line,
                        "amount": amount
                    })
 

    return {
        "income": income,
        "transactions": transactions
    }


def contains_float(line):
    # Regex to match a standard floating-point number pattern
    float_pattern = r"\b\d+(?:,\d{3})*\.\d{2}\b(?!\.\d)"
    # re.search returns a match object (truthy) if found, otherwise None (falsy)
    match = re.search(float_pattern, line)
    if match:
        # Return the matched substring, converted to a float
        num =  float(match.group(0).replace(",", ""))
        return num
    else:
        # Return None or raise an error if no number is found
        return 0.00
    

