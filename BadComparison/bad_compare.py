"""
    Example of a bad way to write a compound Boolean
    expression and the remedy.
"""

# Annotate and initialize constants and variables.
THRESHOLD: int = 100
num1: int
num2: int

# Obtain two values from the user.
num1 = int(input("Please enter a number: "))
num2 = int(input("Please enter another number: "))

### Compare to threshold (bad code)
##if num1 and num2 > THRESHOLD:
##    print("Both numbers are greater than the threshold.")

# Compare to threshold (good code)
if num1 > THRESHOLD and num2 > THRESHOLD:
    print("Both numbers are greater than the threshold.")
