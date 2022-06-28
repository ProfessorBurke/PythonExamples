"""Obtain three numbers and report the sum.
"""

# Annotate and initialize variables.
i: int
num: int
total: int = 0

# Obtain three numbers and total them.
for i in range(3):
    num = int(input("Please enter a whole number: "))
    total += num

# Display the total.
print("The total of your values is {}.".format(total))
