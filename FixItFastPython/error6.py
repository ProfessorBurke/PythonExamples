"""
    A program that finds a best fit value in a loop.

    Maggie
"""
# Annotate and initialize variables.
best_fit: int = 2000000000
value: int = 0
num_values: int = 0

# Let the user know what the program does.
print("I'll tell you the smallest value you enter.")

# Obtain positive values from the user until they enter -1,
# finding the largest value they enter.
while value != -1:
    value = int(input("Enter a positive value or -1 to quit: "))
    num_values += 1
    if value < best_fit:
        best_fit = value

# If any values were entered, display the largest.
if num_values != 0:
    print(f"The smallest value entered was {best_fit}.")
