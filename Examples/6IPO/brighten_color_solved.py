"""
    Obtain red, green, and blue values between 0 and 205 for
    a single color.  Brighten the color by adding 50 to each
    component.

    The program running should look like (for inputs of red and green):
    What is the red component of the color? (0-205) 100
    What is the green component of the color? (0-205) 50
    What is the blue component of the color? (0-205) 0
    The brightened color is (150, 100, 50).

"""
# Annotate variables
BRIGHTEN_VALUE: int = 50
red: int
green: int
blue: int
brighter_red: int
brighter_green: int
brighter_blue: int

# Obtain the color to be brightened from the user.
red = int(input("What is the red component of the color? (0-205) "))
green = int(input("What is the green component of the color? (0-205) "))
blue = int(input("What is the blue component of the color? (0-205) "))

# Brighten the color.
brighter_red = red + BRIGHTEN_VALUE
brighter_green = green + BRIGHTEN_VALUE
brighter_blue = blue + BRIGHTEN_VALUE

# Display the new color.
print("The brightened color is ({}, {}, {})."
      .format(brighter_red, brighter_green, brighter_blue))

### Output in f-string form.
##print(f"The brightened color is ({brighter_red}, {brighter_green}, {brighter_blue}).")

