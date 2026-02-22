import math 
def calculate_circle_area(radius):
    """Calculate the area of a circle given its radius."""
    return math.pi * math.pow(radius, 2)
rasius = float(input("Enter radius: "))
area = calculate_circle_area(rasius)
print("Area of Circle:", area)