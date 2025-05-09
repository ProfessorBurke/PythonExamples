"""
    Write a program that obtains two single-digit numbers from
    the user as strings.  Add the numbers together and report the
    total using the ord() function, not the int() function.

    Hint:  Subtract the ord of zero from your numbers.

    Here are examples of the program running:
    Enter the first number: 9
    Enter the second number: 9
    The total of 9 and 9 is 18.

    Enter the first number: 0
    Enter the second number: 6
    The total of 0 and 6 is 6.

    Enter the first number: 5
    Enter the second number: 2
    The total of 5 and 2 is 7.

"""
# Variable annotations.
DIGIT_SHIFT: int =  ord("0")
digit1: str
digit2: str
total: int

# Obtain the numbers from the user as strings.
digit1 = input("Enter the first number: ")
digit2 = input("Enter the second number: ")

# Convert the numbers to numeric values and add them.
total = ord(digit1) + ord(digit2) - 2*DIGIT_SHIFT

# Display the total.
print("The total of {} and {} is {}.".format(digit1, digit2, total))

### The output, but with an f-string.
##print(f"The total of {digit1} and {digit2} is {total}.")






