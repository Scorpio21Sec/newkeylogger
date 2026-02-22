import math
import numpy as np

A = np.array([1, 2, 3])
B = np.array([7, 8, 9])

# 2. Addition of arrays
C = A + B
print("Addition  ",C)

D = A - B
print("Sub",D)

E = A * B
print("Mult",E)

print("Dot product result")
dot_val = np.dot(A, B)
print(dot_val)

print("Reshaped array result")
arr = np.arange(12)
reshaped = arr.reshape(3, 4)
print(reshaped)

print("Matrix multiplication result")
M1 = np.array([[1, 2],
               [3, 4]])

M2 = np.array([[5, 6],
               [7, 8]])

E = M1 @ M2
print(E)

print("1D array slicing result")
nums = np.array([10, 20, 30, 40, 50])

print(nums[1:4])
print(nums[::2])
print(nums[:3])
print(nums[3:])

nums1 = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9,10,11,12]])
print("2D matrix result")
print(nums1[1, :])
print(nums1[0:2, 1:3])
