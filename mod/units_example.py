"""
    A program that will distribute small units correctly
    into larger buckets.
"""

# Constants for time conversions
SECONDS_IN_MINUTE: int = 60
MINUTES_IN_HOUR: int = 60

# Constants for unit conversions
INCHES_IN_FOOT: int = 12
FEET_IN_MILE: int = 5280

# Constants for metric conversions
MM_IN_CM: int = 10
CM_IN_M: int = 100

# Constants for currency conversions
PENNIES_IN_NICKEL: int = 5
PENNIES_IN_DIME: int = 10

# Break a number of seconds into hours, minutes, seconds.
seconds: int = 5000
minutes: int = seconds // SECONDS_IN_MINUTE
seconds_left: int = seconds % SECONDS_IN_MINUTE
hours: int = minutes // MINUTES_IN_HOUR
minutes_left: int = minutes % MINUTES_IN_HOUR

print("{} h {} m {} s".format(hours, minutes_left, seconds_left))

# Break a number of inches into miles, feet, inches.
inches: int = 50000
feet: int = inches // INCHES_IN_FOOT
inches_left: int = inches % INCHES_IN_FOOT
miles: int = feet // FEET_IN_MILE
feet_left: int = feet % FEET_IN_MILE

print("{} miles {} feet {} inches".format(miles, feet_left, inches_left))

# Break a number of millimeters into meters, centimeters, and millimeters.
millimeters: int = 123456
centimeters: int = millimeters // MM_IN_CM
millimeters_left: int = millimeters % MM_IN_CM
meters: int = centimeters // CM_IN_M
centimeters_left: int = centimeters % CM_IN_M

print("{} m {} cm {} mm".format(meters, centimeters_left, millimeters_left))

# Break a number of pennies into dimes, nickels, and pennies.
pennies: int = 289
dimes: int = pennies // PENNIES_IN_DIME
pennies_left: int = pennies % PENNIES_IN_DIME
nickels: int = pennies_left // PENNIES_IN_NICKEL
pennies_left = pennies_left % PENNIES_IN_NICKEL

print("{} dimes {} nickels {} pennies".format(dimes, nickels, pennies_left))
