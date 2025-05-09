"""
    Write a program that obtains a single lowercase letter from the user
    and returns an uppercase version of the letter.

    Hint:  You can use the ord function and pass your single
    character to it.  That will give you the decimal Unicode
    value of the character.  Use the chr function to convert
    a decimal Unicode value back to a character.

    The program will only work on basic latin lowercase letters
    ("a"-"z").

    Here are examples of the program running:
    Enter a lowercase letter: a
    The uppercase letter is A.

    Enter a lowercase letter: z
    The uppercase letter is Z.

    (Example of this not working on bad input.)
    Enter a lowercase letter: A
    The uppercase letter is !.

"""
# Variable annotations.
CASE_SHIFT: int =  ord("A") - ord("a")
lowercase_letter: str
uppercase_letter: str
numeric_letter: int

# Obtain the letter from the user.
lowercase_letter = input("Enter a lowercase letter: ")

# Convert the character to its numeric value and add CASE_SHIFT.
numeric_letter = ord(lowercase_letter) + CASE_SHIFT
# Convert that back to a character.
uppercase_letter = chr(numeric_letter)

# Display the lowercase character.
print("The uppercase letter is {}.".format(uppercase_letter))

### The output, but with an f-string.
##print(f"The uppercase letter is {uppercase_letter}.")






