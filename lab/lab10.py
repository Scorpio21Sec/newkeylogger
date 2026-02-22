# Upgraded import for numpy with an alias
import numpy as np

# Create a 2D array (4x4) with numbers 1 to 16
arr = np.arange(1, 17).reshape(4, 4)
print("Original Array:\n", arr)

# Extract the first 2 rows and 2 columns
first_block = arr[:2, :2]
print("\nFirst 2 rows and 2 columns:\n", first_block)

# Extract the last 2 rows and 2 columns
last_block = arr[2:, 2:]
print("\nLast 2 rows and 2 columns:\n", last_block)

# Extract the 2nd column only
second_column = arr[:, 1]
print("\nSecond column only:\n", second_column)

#Consider the array of boards marks , extract marks of all students in the 2nd subject, extract marks of last 2 students
