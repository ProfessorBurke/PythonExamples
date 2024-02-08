"""
    Illustrate working with the HTMLCalendar class.
"""
from calendar import HTMLCalendar


# Create an HTMLCalendar object and get an HTML
# string for the month of January.
cal = HTMLCalendar()
january = cal.formatmonth(2024, 1, True)

# Write the January string to a file. 
try:
    with open("january.html", "w") as january_file:
        january_file.write(january)
        january_file.close()
except:
    print("Something went wrong with writing the file.")

