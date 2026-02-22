a = int(input("Enter a number between 1 & 10: "))
match a:
    case 4:
        print("You won car.")
    case 7:
        print("You won Book.")
    case 3:
        print("You won $100.")
    case _:
        print("Better luck next time.")
# This code is a simple game where the user inputs a number between 1 and 10,