"""
    Illustrate working with the date class.
"""

from datetime import date
from datetime import timedelta

# Annotate variables
spring_2023_start: date
spring_2024_start: date
assignment_2023: date
new_date: date
difference: timedelta

# Find the difference between two semester starts.
spring_2023_start = date(2023, 1, 23)
spring_2024_start = date(2024, 1, 22)
difference = spring_2024_start - spring_2023_start
print(difference)

# Find the difference between semester start and a
# specific assignment due date.
assignment_2023 = date(2023, 2, 19)
difference = assignment_2023 - spring_2023_start
print(difference)

# What date would that be in 2024?
new_date = spring_2024_start + difference
print(new_date)

# Are they the same day of the week?
print(new_date.weekday() == assignment_2023.weekday())

