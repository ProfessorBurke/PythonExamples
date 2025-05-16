"""
    Write a program that obtains a time from the user
    as a number between 1 and 12 and either "am" or "pm."
    Convert that to a 24-hour clock time and display
    the new time.

    Here are four examples of the program running:
    What is the hour (1-12): 12
    Is that am or pm? pm
    12 pm is 12 on a twenty-four hour clock.

    What is the hour (1-12): 12
    Is that am or pm? am
    12 am is 00 on a twenty-four hour clock.

    What is the hour (1-12): 1
    Is that am or pm? am
    1 am is 01 on a twenty-four hour clock.

    What is the hour (1-12): 1
    Is that am or pm? pm
    1 pm is 13 on a twenty-four hour clock.

"""

# Annotate variables
twelve_hour: int
twenty_four_hour: int
am_pm: str

# Obtain the hour and "am" or "pm" from the user.
twelve_hour = int(input("What is the hour (1-12): "))
am_pm = input("Is that am or pm? ")

# Change the hour to 24-hour time using am_pm.
# Afternoon, but not twelve noon.
if twelve_hour != 12 and am_pm.lower() == "pm":
    twenty_four_hour = twelve_hour + 12
# Twelve midnight.
elif twelve_hour == 12 and am_pm.lower() == "am":
        twenty_four_hour = 0
# Morning and twelve noon.
else:
    twenty_four_hour = twelve_hour

# Display the converted time.
print("{} {} is {:02} on a twenty-four hour clock."
      .format(twelve_hour, am_pm, twenty_four_hour))
