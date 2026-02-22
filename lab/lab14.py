import pandas as pd

# Step 1: Create Dataset
data = {
    "id": [1, 2, 3, 4, 5],
    "product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Charger"],
    "price": [70000, 500, 1500, 12000, 800],
    "quantity": [2, 10, 5, 3, 6]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# Step 2: Sort by single column (price - descending order)
df_sorted_price = df.sort_values(by="price", ascending=False)
print("\nSorted by Price (Descending):")
print(df_sorted_price)

# Step 3: Sort by multiple columns (first by quantity ascending, then by price descending)
df_sorted_multi = df.sort_values(by=["quantity", "price"], ascending=[True, False])
print("\nSorted by Quantity (Ascending) and Price (Descending):")
print(df_sorted_multi)

# Step 4: Export result to CSV file
df_sorted_multi.to_csv("file.csv", index=False)
print("\nCSV file 'file.csv' exported successfully!")


#a samll organization maintains a dataset of employee contain their name , age , and performance score, the management want to analyze data for decision 