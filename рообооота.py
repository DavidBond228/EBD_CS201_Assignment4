import json
import csv
import pandas as pd
import matplotlib.pyplot as plt

with open("regional_tariffs.json", "r") as f:
    tariffs = json.load(f)

with open("global_sales.csv", "r") as f:
    sales = list(csv.DictReader(f))

for sale in sales:
    if sale["quantity"] == "N/A":
        sale["quantity"] = 0
    else:
        sale["quantity"] = float(sale["quantity"])

    if sale["revenue"] == "N/A":
        sale["revenue"] = 0
    else:
        sale["revenue"] = float(sale["revenue"])

for region, tariff in tariffs.items():
    if tariff == "N/A":
        tariffs[region] = 0
    else:
        tariffs[region] = float(tariff)

for sale in sales:
    tariff = tariffs[sale["region"]]
    sale["net_profit"] = sale["revenue"] - (sale["revenue"] * tariff / 100)
with open("cleaned_sales_updated.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=sales[0].keys())
    writer.writeheader()
    writer.writerows(sales)
category_profit = {}
for sale in sales:
    category = sale["product_category"]
    profit = sale["net_profit"]
    if category in category_profit:
        category_profit[category] += profit
    else:
        category_profit[category] = profit
average = sum(category_profit.values()) / len(category_profit)
top_categories = dict(filter(
    lambda pair: pair[1] > average,
    category_profit.items()
))
sorted_categories = sorted(top_categories.items(), key=lambda pair: pair[1], reverse=True)
with open("top_categories.json", "w") as f:
    json.dump(dict(sorted_categories), f, indent=2)
df = pd.DataFrame(sorted_categories, columns=["Category", "Net Profit"])
print(df)
plt.figure(figsize=(10, 6))
plt.bar(df["Category"], df["Net Profit"])
plt.title("Top Categories by Net Profit")
plt.xlabel("Category")
plt.ylabel("Net Profit")
plt.show()