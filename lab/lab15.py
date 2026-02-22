import pandas as pd

# Sample employee dataset with Indian names
data = {
    "name": ["Amit", "Priya", "Rahul", "Sneha", "Vikram", "Anjali"],
    "age": [34, 45, 29, 41, 38, 50],
    "performance_score": [88, 92, 85, 90, 87, 95]
}

df = pd.DataFrame(data)

# 1. Sort data by performance_score (descending), then by age (ascending)
sorted_df = df.sort_values(by=["performance_score", "age"], ascending=[False, True])
print("Sorted Data (by performance_score, then age):")
print(sorted_df)

# 2. Select name and score for employees above 40 years of age
filtered_df = df[df["age"] > 40][["name", "performance_score"]]
print("\nEmployees above 40 (name and performance_score):")
print(filtered_df)

# 3. Accessing individual rows for detailed review
print("\nDetailed review of each employee:")
for idx, row in df.iterrows():
    print(f"Employee {idx}: Name={row['name']}, Age={row['age']}, Score={row['performance_score']}")