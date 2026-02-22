import pandas as pd

# Step 1: Create sales data
data = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8],
    "product": ["Laptop", "Phone", "Tablet", "Headphones", "Monitor", "Keyboard", "Mouse", "Smartwatch"],
    "region": ["US", "India", "US", "UK", "US", "India", "UK", "US"],
    "city": ["New York", "Mumbai", "San Francisco", "London", "Chicago", "Delhi", "Manchester", "Los Angeles"],
    "quantity": [10, 5, 20, 7, 15, 3, 12, 8],
    "price": [1000, 500, 300, 100, 200, 50, 25, 150],  # All prices in INR
    "currency": [
        "INR",    # All prices are in INR initially
        "INR",
        "INR",
        "INR",
        "INR",
        "INR",
        "INR",
        "INR"
    ]
}

# Conversion rates from INR to other currencies
conversion_rates = {
    "US": 0.012,   # INR to USD
    "UK": 0.0095,  # INR to GBP
    "India": 1     # INR to INR
}

# Convert price and currency for each region
for i in range(len(data["region"])):
    region = data["region"][i]
    rate = conversion_rates[region]
    data["price"][i] = round(data["price"][i] * rate, 2)
    if region == "US":
        data["currency"][i] = "USD"
    elif region == "UK":
        data["currency"][i] = "GBP"
    else:
        data["currency"][i] = "INR"

df = pd.DataFrame(data)

print("      Sales Data     ")
print(df)

# 1️ Select orders from US region only
us_orders = df[df["region"] == "US"]
print("\n     Orders from US     ")
print(us_orders)

# 2️ Select product and price where quantity is greater than 10
high_quantity = df[df["quantity"] > 10][["product", "price"]]
print("\n    Products with Quantity > 10     ")
print(high_quantity)

# 3 Adding a new product (row)
new_row = {
    "id": 9,
    "product": "Charger",
    "region": "India",
    "city": "Bangalore",
    "quantity": 6,
    "price": 80,
    "currency": "INR",
}
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
print("\n    DataFrame After Adding New Product    ")
print(df)



df = pd.DataFrame(data)
print("Product from US region : ")
print(df.iloc[0])

print("Product and Price where quantity is greater than 2 : ")
ans = df[df["quantity"] > 2][["product", "price"]]
print(ans)

