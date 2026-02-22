import math

while True:
    print("\n===== PYTHON MATH CALCULATOR =====")
    print("1. Power (x^y)")
    print("2. Factorial (n!)")
    print("3. Area of Circle")
    print("4. Trigonometry (sin, cos, tan)")
    print("5. Logarithm (log base)")
    print("6. Exit")
    
    choice = int(input("Enter your choice (1-6): "))

    if choice == 1:
        x = float(input("Enter base (x): "))
        y = float(input("Enter exponent (y): "))
        print("Result:", math.pow(x, y))

    elif choice == 2:
        n = int(input("Enter a number: "))
        print("Factorial:", math.factorial(n))

    elif choice == 3:
        r = float(input("Enter radius: "))
        area = math.pi * math.pow(r, 2)
        print("Area of Circle:", area)

    elif choice == 4:
        angle = float(input("Enter angle in degrees: "))
        rad = math.radians(angle)  # convert to radians
        print(f"sin({angle}) = {math.sin(rad)}")
        print(f"cos({angle}) = {math.cos(rad)}")
        print(f"tan({angle}) = {math.tan(rad)}")

    elif choice == 5:
        x = float(input("Enter number: "))
        base = float(input("Enter base (default e, enter 0 for e): "))
        if base == 0:
            print("Natural log:", math.log(x))
        else:
            print(f"log base {int(base)} of {x}:", math.log(x, base))

    elif choice == 6:
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid choice! Please try again.")
