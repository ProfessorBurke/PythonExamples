"""
    A program that finds a best fit value in a loop.

    Maggie
"""
# Annotate and initialize variables.
best_fit: int = 0
value: int
num_values: int = 0

# Let the user know what the program does.
print("I'll tell you the largest value you enter.")

# Obtain positive values from the user until they enter -1,
# finding the largest value they enter.
value = int(input("Enter a positive value or -1 to quit: "))
while value != -1:
    num_values += 1
    if value > best_fit:
        value = best_fit
    value = int(input("Enter a positive value or -1 to quit: "))

# If any values were entered, display the largest.
if num_values != 0:
    print(f"The largest value entered was {best_fit}.")
