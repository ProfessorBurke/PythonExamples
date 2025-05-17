"""
    Write a program that obtains the day and time of the
    appointment that the person wants.

    Validate the appointment.
    
    An appointment is only valid if it is not on a weekend,
    and if it is between 8 am and 4 pm.  (It is okay if the
    appointment begins at 4 pm.)

    Let the user know if their appointment is valid or not.

    Here are four examples of the program running:

    What is the day for the desired appointment?: Monday
    What is the hour for the desired appointment? (8-4): 1
    We'll see you on Monday at 1.

    What is the day for the desired appointment? Monday
    What is the hour for the desired appointment? (8-4): 7
    Please schedule your appointment between 8 am and 4 pm.

    What is the day for the desired appointment?: Saturday
    What is the hour for the desired appointment? (8-4): 8
    Please schedule your appointment for a weekday.

    What is the day for the desired appointment? Saturday
    What is the hour for the desired appointment? (8-4): 7
    Please schedule your appointment between 8 am and 4 pm.
    Please schedule your appointment for a weekday.

"""
# Annotate variables.
day: str
hour: int
status_message: str

# Obtain the appointment the user wants to make.
day = input("What is the day for the desired appointment? ")
hour = int(input("What is the hour for the desired appointment? (8-4): "))

# Check if the appointment is valid and set the status message.
if (hour >= 8 and hour <= 12) or (hour >= 1 and hour < 5):
    if day != "Saturday" and day != "Sunday":
        status_message = "We'll see you on {} at {}.".format(day, hour)
    else:
        status_message = "Please schedule your appointment for a weekday."
else:
    status_message = "Please schedule your appointment between 8 am and 4 pm.\n"
    if day == "Saturday" or day == "Sunday":
        status_message += "Please schedule your appointment for a weekday."
        

# Display the appointment status.
print(status_message)









