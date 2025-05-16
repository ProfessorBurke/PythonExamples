"""
    Obtain a month, day, and year value from the user.
    Using constants for today's date, determine if the
    date provided by the user is in the future.

    Here are examples of the program running on 2025-5-16

    Enter a date and I'll tell you if it's in the future.
    Enter the year: 2025
    Enter the month: 5
    Enter the day: 16
    Not in the future!

    Enter a date and I'll tell you if it's in the future.
    Enter the year: 2025
    Enter the month: 5
    Enter the day: 17
    Back to the future!
    
    Enter a date and I'll tell you if it's in the future.
    Enter the year: 2024
    Enter the month: 5
    Enter the day: 16
    Not in the future!

    Enter a date and I'll tell you if it's in the future.
    Enter the year: 2025
    Enter the month: 4
    Enter the day: 17
    Not in the future!
"""

# Annotate and initialize constants representing today's date.
YEAR: int = 2025
MONTH: int = 5
DAY: int = 16

# Annotate variables for the user-entered date and result.
user_year: int
user_month: int
user_day: int
in_future: bool

# Obtain the month, day, and year from the user.
print("Enter a date and I'll tell you if it's in the future.")
user_year = int(input("Enter the year: "))
user_month = int(input("Enter the month: "))
user_day = int(input("Enter the day: "))

# Determine if the date is in the future.
in_future = True
# If the year is in the past, we're in the past
if user_year < YEAR:
    in_future = False
# If it's the current year, check month:
elif user_year == YEAR:
    # If the month is in the past, we're in the past:
    if user_month < MONTH:
        in_future = False
    # If it's the current month, check day:
    elif user_month == MONTH:
        # If the day is in the past or is the current day, it's not the future:
        if user_day <= DAY:
            in_future= False

# Let the user know if their date is in the future.
if in_future:
    print("Back to the future!")
else:
    print("Not in the future!")






        
