"""
    Write a loop that adds together every third number from
    1 through 100 and then prints the result.  So, the loop
    will add 1, 4, 7, etc. through 97.

    The result should be 1617.
"""

# Annotate the total and the loop control variable.
total: int
i: int

# Count from 1 to 100 in increments of 3 and total
# the values.
total = 0
for i in range(1, 100, 3):
    total += i

# Display the total.
print("The total of every third number from 1-100 is {}.".format(total))
