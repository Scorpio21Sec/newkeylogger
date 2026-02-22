import math
def power(x, y):
    """ Calculate x raised to the power of y."""
    return math.pow(x, y)
input_x = float(input("Enter base (x): "))
input_y = float(input("Enter exponent (y): "))
result = power(input_x, input_y)
print("Result:", result)