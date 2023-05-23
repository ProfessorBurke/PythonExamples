"""
Public URL (for your students): https://codecheck.io/files/23052314475c9grhm2oyxghl4oto0r8idfa
"""

"""Find the largest value entered by the user."""
##IN 1\n2\n3\n4\n5\n
##IN 5\n2\n3\n4\n1\n
##IN 5\n2\n6\n4\n1\n

# Annotate variables.
largest: float
i: int
number: float

# Obtain the first value to initialize the most wanted holder.
largest = float(input("Please enter a value: "))

# Obtain four more values from the user in a loop
# and find the largest.
i = 0
while i < 4:
    ##TILE
    number = float(input("Please enter a value: "))
    if number > largest:
    ##OR if largest > number:
    ##OR if number < largest:
        largest = number
        ##OR number = largest
    i += 1

##FIXED
# Display the largest number entered to the user.
print("The largest number entered was {:.1f}.".format(largest))
