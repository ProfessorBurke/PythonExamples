"""
    A clock that displays a reminder every four hours.
    (Or every four seconds if you're not feeling patient.)
"""

import PySimpleGUI as sg
import time
from typing import Tuple

# Variable annotations
layout: list[list[sg.Text]]  # Layout for the window
window: sg.Window            # The PySimpleGUI window
event: str                   # Event from window interaction
values: dict                 # Dictionary of window values
current_time: time.struct_time  # Holds the system time
time_display: str            # String for formatted time display
hours: int                   # Current hour from system time
minutes: int                 # Current minute from system time
seconds: int                 # Current second from system time

# Create the window layout
layout = [[sg.Text('', size=(10, 2), font=('Helvetica', 48), key='clock')],
          [sg.Text('', size=(30, 1), font=('Helvetica', 16), key='reminder')]]

# Create the window
window = sg.Window('Clock with Medicine Reminder', layout, finalize=True)

# Initial event and values
event, values = window.read(timeout=1000)  

# Event loop
while event != sg.WIN_CLOSED:
    # Get the current system time
    current_time = time.localtime()
    
    # Extract hours, minutes, and seconds
    hours = current_time.tm_hour
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    
    # Update the clock display
    time_display = f'{hours:02}:{minutes:02}:{seconds:02}'
    window['clock'].update(time_display)
    
    # Reminder: every 4 hours
    # If current time mod 4 equals 0 and minutes and seconds are 0, show the reminder
    #if hours % 4 == 0 and minutes == 0 and seconds == 0:
    if seconds % 4 == 0:
        window['reminder'].update("Time to take your medicine!")
    else:
        window['reminder'].update("")
    
    # Read event and values again at the end of the loop
    event, values = window.read(timeout=1000)  # Update event and values every second

# Close the window
window.close()
