import numpy as np

# Create an array of Celsius temperatures (0 to 90, step 10)
# Note: np.arange(0, 100, 10) excludes 100
celsius = np.arange(0, 100, 10)

# Apply the conversion formula element-wise: (C * 9/5) + 32
fahrenheit = (celsius * 9/5) + 32

print("Celsius temperatures:", celsius)
print("Fahrenheit temperatures:", fahrenheit)