"""
    Obtain red, green, and blue values between 0 and 255 for
    two different colors and average the colors together.

    The program running should look like (for inputs of red and green):
    What is the red component of the first color? 255
    What is the green component of the first color? 0
    What is the blue component of the first color? 0
    What is the red component of the second color? 0
    What is the green component of the second color? 255
    What is the blue component of the second color? 0
    The average of (255, 0, 0) and (0, 255, 0) is (127, 127, 0).

"""

# Annotate variables
color1_red: int
color2_red: int
color1_green: int
color2_green: int
color1_blue: int
color2_blue: int
averaged_color_red: int
averaged_color_green: int
averaged_color_blue: int

# Obtain the two colors to be averaged from the user.
color1_red = int(input("What is the red component of the first color? "))
color1_green = int(input("What is the green component of the first color? "))
color1_blue = int(input("What is the blue component of the first color? "))
color2_red = int(input("What is the red component of the second color? "))
color2_green = int(input("What is the green component of the second color? "))
color2_blue = int(input("What is the blue component of the second color? "))

# Average the colors.
averaged_color_red = (color1_red + color2_red)// 2
averaged_color_green = (color1_green + color2_green) // 2
averaged_color_blue = (color1_blue + color2_blue) // 2

# Display the new color.
print("The average of ({}, {}, {}) and ({}, {}, {}) is ({}, {}, {})."
      .format(color1_red, color1_green, color1_blue,
              color2_red, color2_green, color2_blue,
              averaged_color_red, averaged_color_green, averaged_color_blue))

### Output in f-string form.
##print(f"The average of ({color1_red}, {color1_green}, {color1_blue}) and "
##      +f"({color2_red}, {color2_green}, {color2_blue}) "
##      +f"is ({averaged_color_red}, {averaged_color_green}, {averaged_color_blue}).")






