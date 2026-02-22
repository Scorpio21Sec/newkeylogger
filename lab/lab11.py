import numpy as np

nums = np.array([[75, 85, 85, 90],
                 [60, 65, 70, 75],
                 [88, 92, 96, 100]])

print("Marks array:\n", nums)

# 1) Extract marks of all students in 2nd subject (column index 1)
second_subject = nums[:, 1]
print("Marks in 2nd subject:", second_subject)

# 2) Extract marks of last 2 students in last 2 subjects
last_block = nums[-2:, -2:]
print("Last 2 students in last 2 subjects:\n", last_block)

# 3) Extract all marks greater than 85
greater_85 = nums[nums > 85]
print("Marks greater than 85:", greater_85)
3
