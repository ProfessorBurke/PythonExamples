"""
    Check if a number is even or odd.
"""

# Annotate the input variable.
number: int

# Obtain the input variable from the user.
number = int(input("Please enter a whole number: "))

# Tell the user if their number is even or odd.
if number % 2 == 0:
    print("Your number is even.")
else:
    print("Your number is odd.")
