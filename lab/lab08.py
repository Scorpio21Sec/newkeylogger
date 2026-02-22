import numpy as np

# ---------------------------------------------------------
# PART 1: Student Marks (3 students, 4 subjects)
# ---------------------------------------------------------

# Array of student marks (3 students, 4 subjects)
marks = np.array([
    [75, 80, 85, 90],  # Student 1
    [60, 65, 70, 75],  # Student 2
    [88, 92, 96, 100]  # Student 3
])

print("--- Student Marks (3 students, 4 subjects) ---")
print(marks)

# a) Extract marks of all students in the 2nd subject
print("\na) Marks of all students in the 2nd subject (marks[:, 1]):")
print(marks[:, 1])

# b) Extract marks of last 2 students in last 2 subjects
print("\nb) Marks of last 2 students in last 2 subjects (marks[-2:, -2:]):")
print(marks[-2:, -2:])

# c) Extract all marks greater than 85 (Boolean Masking)
print("\nc) Marks greater than 85 (marks[marks > 85]):")
boolean_mask = marks > 85
print("Boolean Mask:\n", boolean_mask)
extracted_marks = marks[boolean_mask]
print("Extracted Values:", extracted_marks)


# ---------------------------------------------------------
# PART 2: 4x4 Array Slicing
# ---------------------------------------------------------

# Create a 4x4 array of numbers 1–16
arr = np.arange(1, 17)
arr_2d = arr.reshape(4, 4)

print("\n--- Original 4x4 Array ---")
print(arr_2d)

# a) Extract first 2 rows and first 2 columns
print("\na) First 2 rows and first 2 columns (arr_2d[:2, :2]):")
print(arr_2d[:2, :2])

# b) Extract last 2 rows and last 2 columns
print("\nb) Last 2 rows and last 2 columns (arr_2d[-2:, -2:]):")
print(arr_2d[-2:, -2:])

# c) Extract 2nd column only
print("\nc) Second column only (arr_2d[:, 1]):")
print(arr_2d[:, 1])
