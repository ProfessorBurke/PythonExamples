import PySimpleGUI as sg
from datetime import date
import calendar
import re

def get_file_contents(path: str) -> list:
    """Open the file at path and read the contents
       into a list and return.  If there's a file error, return an
       empty list."""
    contents: list = []
    in_file: "file"
    
    try:
        with open(path) as in_file:
            contents = in_file.readlines()
            in_file.close()
    except:
        print("I'm sorry, there was an error with the file.")
    return contents

def convert_date(old_start: date, new_start: date, old_assignment: date) -> date:
    """Convert the old assignment date to the date for the new semester."""
    return new_start + (old_assignment - old_start)

def convert_calendar(old_semester_start: date, new_semester_start: date,
                     old_calendar: list) -> None:
    """ Given the start and end dates of the semester and a list of
        calendar lines, convert the calendar from old_semester_start to
        new_semester_start.  Changes the old_calendar in place."""
    # Annotate variables
    i: int
    match: re.Match
    m: str
    d: str
    new_date: date
    # Convert the calendar
    for i in range(len(old_calendar)):
        # Find each date in the line and process it.
        for match in re.finditer(r'(\d+/\d+)', old_calendar[i]):
            # Update the date to the equivalent new semester date.
            m, d = match.group(1).split("/")
            new_date = convert_date(old_semester_start, new_semester_start,
                                    date(old_semester_start.year, int(m), int(d)))
            # Replace the old date with the new date in the calendar.
            old_calendar[i] = (old_calendar[i][:match.start()] +
                           str(new_date.month) + "/" +
                           str(new_date.day) + old_calendar[i][match.end():])

def write_file(contents: list, file_name: str) -> None:
    """Get a file name from the user, open the file and write contents
       to the file, one element to a line."""
    out_file: "file"
    try:
        with open(file_name, "w") as out_file:
            for line in contents:
                out_file.write(line)
            out_file.close()
    except:
        print("I'm sorry, there was an error with the file.")

def date_from_box(key: str, window: sg.Window) -> date:
    """Get the date string of the format d/m/y from the interface
       element with key, split and convert to a date and return."""
    m: int
    d: int
    y: int
    date_string: str = window[key].get()
    m,d,y = old_date_string.split("/")
    return date(int(y),int(m),int(d))

def main() -> None:
    """ Allow the user to choose a date."""

    # Annotate variables and initialize constants.
    MONTHS: list = ["January", "February", "March", "April", "May",
                    "June", "July", "August", "September", "October",
                    "November", "December"]
    layout: list
    running: bool = True
    values: dict
    event: str
    old_date: date
    new_date: date
    file_path: str
    new_calendar_file_name: str
    calendar: list

    # Build the interface.
    sg.theme('DarkAmber')
    layout = [  [sg.CalendarButton("Old semester start date:",
                                   default_date_m_d_y = (1, 1, 2019),
                                   key = "OLD_SEMESTER_CHOOSER",
                                   format = "%m / %d / %Y",
                                   target = "OLD_SEMESTER_DATE"),
                 sg.Input("1 / 1 / 2019", key = "OLD_SEMESTER_DATE",
                          disabled = True)
                 ],
                [sg.CalendarButton("New semester start date:",
                                   default_date_m_d_y = (1, 1, 2020),
                                   key = "NEW_SEMESTER_CHOOSER",
                                   format = "%m / %d / %Y",
                                   target = "NEW_SEMESTER_DATE"),
                 sg.Input("1 / 1 / 2020", key = "NEW_SEMESTER_DATE",
                          disabled = True)
                 ],
                [sg.FileBrowse("Choose the old calendar file",
                               target = "OLD_CALENDAR_FILE",
                               key = "OLD_CALENDAR_CHOOSER"),
                 sg.Input("file", key = "OLD_CALENDAR_FILE",
                          disabled = True)
                 ],
                [sg.Text("New file name: "),
                 sg.Input("file", key = "NEW_FILE_NAME")],
                [sg.Button("Convert", key = "CONVERT")]
                ]

    # Create the Window
    window = sg.Window('Calendar Updater', layout)

    # Event Loop to process events and get the values of the inputs
    while running:
        # Get the current event and dictionary of values off the queue:
        event, values = window.read()

        # Handle a quit event.
        if event == sg.WIN_CLOSED: 
            running = False

        # Handle a change to one of the old semester date combo boxes.
        elif event == "CONVERT":
            # Get the old and new date strings and convert to date object.
            old_date = date_from_box("OLD_SEMESTER_DATE", window)
            new_date = date_from_box("NEW_SEMESTER_DATE", window)
            # Get the file path and read in the old calendar.
            file_path = window["OLD_CALENDAR_FILE"].get()
            calendar = get_file_contents(file_path)
            # Convert the old calendar and write to the file.
            convert_calendar(old_date, new_date, calendar)
            new_calendar_file_name = window["NEW_FILE_NAME"].get()
            write_file(calendar, new_calendar_file_name)
            
  

    window.close()

if __name__ == "__main__":
    main()
