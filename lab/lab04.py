import math

def logarithm(x, base=math.e):
    """Calculate the logarithm of x with a given base."""
    if base == 0:
        return math.log(x)
    else:
        return math.log(x, base)

input_x = float(input("Enter number: "))
input_base = float(input("Enter base (default e, enter 0 for e): "))
result = logarithm(input_x, input_base)
print(f"log base {input_base if input_base != 0 else 'e'} of {input_x}: {result}")