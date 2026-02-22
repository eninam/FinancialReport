from collections import defaultdict
from rules import categorize, SUGGESTED_PERCENTAGES

def analyze_spending(statements: list):
    incomes = [s["income"] for s in statements if s["income"]] # return a list of incomes from each file [2,3,6]
    avg_income = sum(incomes) / len(incomes)

    category_totals = defaultdict(float)

    for s in statements:
        for tx in s["transactions"]:
            category = categorize(tx)
            category_totals[category] += tx["amount"] # will look like {"food":10.3}
    suggestions = []
    category_summary = {}
    alerts = []

    for category, spent in category_totals.items():
        # percentage = (spent / avg_income) * 100
        percentage = round((spent / avg_income) * 100, 2)
        # suggested = SUGGESTED_PERCENTAGES.get(category, 10)
        min_pct, max_pct = SUGGESTED_PERCENTAGES.get(category, (0, 100))

        if percentage > max_pct:
            status = "over"
            target_spend = (max_pct / 100) * avg_income
            delta = round(spent - target_spend, 2)

            alerts.append({
                "category": category,
                "message": f"Overspending in {category}",
                "over_by": delta
            })
            suggestions.append({
                "category": category,
                "action": "reduce",
                "message": (
                    f"Reduce {category} spending by approximately "
                    f"${delta} per month to fall within the recommended range."
                ),
                "amount": delta
            })
        elif percentage < min_pct:
            status = "under"
            delta = round(((min_pct / 100) * avg_income) - spent, 2)

        else:
            status = "within"
            delta = 0.0

        category_summary[category] = {
            "spent": round(spent, 2),
            "percentage_of_income": percentage,
            "suggested_range": {
                "min": min_pct,
                "max": max_pct
            },
            "status": status,
            "delta_to_range": delta
        }

    return avg_income, category_summary, alerts, suggestions