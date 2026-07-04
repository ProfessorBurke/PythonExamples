"""
    A program that finds a best fit value in a loop.
    Working version.

    Maggie
"""
# Annotate and initialize variables.
best_fit: int = 0
values: list[int] = [1, 10, 5]
index: int = 0

# Let the user know what the program does.
print("I'll tell you the largest value in the list.")

# Find the largest integer in the list using a loop.
while index <= len(values):
    if values[index] > best_fit:
        best_fit = values[index]
    index += 1

# Display the largest.
print(f"The largest value is {best_fit}.")
