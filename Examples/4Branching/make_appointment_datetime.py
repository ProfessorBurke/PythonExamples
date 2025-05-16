"""
    Write a program that obtains the date and time that a person
    wants to make an appointment.

    Create a datetime object with that information.
    
    Confirm that the appointment is in the future.

    Confirm that the appointment is not on a weekend,
    and if it is between 8 am and 5 pm.  (It must begin before
    5 pm.)

    Let the user know if their appointment is valid or not.    

"""
import PySimpleGUI as sg
from datetime import datetime, date, time

# Annotate variables.
# GUI variables.
layout: list
window: sg.Window
# Event loop variables.
event: str
values: dict[str, str]
user_quit: bool = False
# Date and time variables.
hour: int
minute: int
am_pm: str
selected_date: date
now: datetime
appointment: datetime
# Validation and output variables.
message: str
valid: bool

# Create the layout for the interface.
layout = [
    [sg.Text("Select Date:"), sg.Input(key="-DATE-", size=(20, 1), readonly=True),
     sg.CalendarButton("Pick Date", target="-DATE-", format="%Y-%m-%d")],
    [sg.Text("Select Time:")],
    [
        sg.Spin([f"{i:02d}" for i in range(1, 13)], initial_value="08", key="-HOUR-", size=(3, 1)),
        sg.Text(":"),
        sg.Spin([f"{i:02d}" for i in range(0, 60)], initial_value="00", key="-MINUTE-", size=(3, 1)),
        sg.Combo(["AM", "PM"], default_value="AM", key="-AMPM-", readonly=True)
    ],
    [sg.Button("Make Appointment")],
    [sg.Multiline(key="-OUTPUT-", size=(40, 5), disabled=True)]
]

window = sg.Window("Appointment Scheduler", layout)

# Run in a loop until the user closes the window.  When the user presses the Make Appointment button,
# validate the appointment and display the appropriate message.
while not user_quit:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        user_quit = True
    elif event == "Make Appointment":
        # Validate the appointment.
        # Create a date object for the date.
        selected_date = datetime.strptime(values["-DATE-"], '%Y-%m-%d').date()

        # Convert the time to 24-hour time.
        hour = int(values["-HOUR-"])
        minute = int(values["-MINUTE-"])
        am_pm = values["-AMPM-"]
        if  hour != 12 and am_pm == "PM":
            hour += 12
        elif hour == 12 and am_pm == "AM":
            hour = 0
            
        # Combine the date and time.
        appointment = datetime.combine(selected_date, time(hour, minute))

        # Validate the appointment date and time.
        message = ""
        valid = True
        
        # Check that the appointment is not in the past (or exactly now).
        now = datetime.now()
        if appointment <= now:
            message = "Appointments cannot be in the past.\n"
            valid = False

        # Check that the time is within 8:00 to 16:00 inclusive.
        if not (8 <= appointment.hour and appointment.hour <= 16):
            message += "Appointments must be between 8:00 AM and 4:00 PM.\n"
            valid = False

        # Check that the day is not a weekend day.
        if appointment.weekday() >= 5:
            message += "Appointments cannot be on Saturday or Sunday."
            valid = False

        if valid:
            message = "We'll see you on {}.".format(appointment.ctime())
                
        # Display a message based on the appointment.
        window["-OUTPUT-"].update(message)

window.close()





