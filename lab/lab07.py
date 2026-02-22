import numpy as np

# Generate 100 points between 0 and 2π
x = np.linspace(0, 2 * np.pi, 100)

# Compute sine values for each point
y = np.sin(x)

# Print the results
for xi, yi in zip(x, y):
    print(f"sin({xi:.2f}) = {yi:.2f}")
print("Sine values computed for 100 points between 0 and 2π.")  