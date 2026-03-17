import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import json
import re
load_dotenv()


client = Groq(api_key=os.getenv("grok_api_key"),)

CATEGORIES = [
    "Transportation",
    "Dining",
    "Groceries",
    "Shopping",
    "Subscriptions",
    "Health",
    "P2P Transfers",
    "Savings",
    "Investments",
    "Debt Payments",
    "Checks"
]

def ai_classify(description):
    prompt = f"""
        You are a financial transaction classifier.

        From the transaction description, determine:

        1. The best normalized merchant name.
        2. The correct category.

        The category MUST be exactly one of the following:

        Transportation
        Dining
        Groceries
        Shopping
        Subscriptions
        Health
        P2P Transfers
        Savings
        Investments
        Debt Payments
        Checks

        Transaction description:
        {description}

        Return ONLY valid JSON in this format:

        {{
        "merchant": "merchant name",
        "category": "one category from the list above"
        }}
        """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    content = completion.choices[0].message.content

    try:
        content = re.sub(r"```json|```", "", content).strip()
        result = json.loads(content)
        merchant = result["merchant"]
        category = result["category"]
        return merchant, category

    except Exception as e:
        print(f'ai_classify exception {e}')
        return None, "Other"