"""
    A program that finds a best fit value in a loop.

    Maggie
"""
# Annotate and initialize variables.
best_fit: int 
value: int
num_values: int = 0

# Let the user know what the program does.
print("I'll tell you the smallest value you enter.")

# Obtain the first value and store it in best_fit
value = int(input("Enter a positive value or -1 to quit: "))
if value != -1:
    best_fit = value
    num_values += -1

    # Obtain positive values from the user until they enter -1,
    # finding the largest value they enter.
    value = int(input("Enter a positive value or -1 to quit: "))
    while value != -1:
        num_values += 1
        if value < best_fit:
            best_fit = value
        value = int(input("Enter a positive value or -1 to quit: "))

# If any values were entered, display the largest.
if num_values != 0:
    print(f"The smallest value entered was {best_fit}.")
