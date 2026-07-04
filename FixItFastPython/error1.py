"""
    A program that finds a best fit value in a loop.

    Maggie
"""
# Annotate and initialize variables.
best_fit: int = 0
value: int

# Let the user know what the program does.
print("I'll tell you the largest value you enter.")

# Obtain positive values from the user until they enter -1,
# finding the largest value they enter.
value = int(input("Enter a positive value or -1 to quit: "))
while value != -1:
    if value > best_fit:
        best_fit = value
    value = int(input("Enter a positive value or -1 to quit: "))

# Display the largest.
print(f"The largest value entered was {best_fit}.")
