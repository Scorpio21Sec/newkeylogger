import math
def factorial(n):
    """Calculate the factorial of n."""
    if n < 0:
        return "Factorial is not defined for negative numbers."
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    n = int(input("enter a number: "))
    print("Factorial:", factorial(n))
    result = factorial(n)
    print("Factorial:", result)
    
    