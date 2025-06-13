"""Calculate the angle between stars in an aerial firework."""

# Annotate variables.
DEGREES_CIRCLE: int = 360
num_stars: int
angle: float

##Bad code here -- commented out
##angle: float = DEGREES_CIRCLE / num_stars

# Obtain the number of stars from the user.
num_stars = int(input("How many stars? "))

# Calculate the angle between stars (now that
# num_stars is defined with =)
angle = DEGREES_CIRCLE / num_stars

# Tell the user the angle between the stars.
print("You will need an angle of " + str(angle) + " degrees between "
      + str(num_stars) + " stars.")
