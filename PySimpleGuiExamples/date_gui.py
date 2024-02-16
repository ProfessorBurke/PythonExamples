import PySimpleGUI as sg
import calendar


def update_date(window: sg.Window, values: dict, month_widget: str,
                day_widget: str, year_widget: str, text_widget: str) -> None:
    """Update the old semester date field with the values from the combo boxes
       and ensure the number of days is correct for the month and year."""
    # Get the current values of the interface components.
    new_days: list
    last_day_of_month: int
    month: str = values[month_widget]
    day: str = values[day_widget]
    year: str = values[year_widget]
    # Update the list of possible days to match the month and year.
    if month in ["September", "April", "June", "November"]:
        last_day_of_month = 30
    elif month == "February":
        if calendar.isleap(int(year)):
            last_day_of_month = 29
        else:
            last_day_of_month = 28
    else:
        last_day_of_month = 31
        
    # Update the days widget to display the correct days given the month,
    # and change the day to 1 if the current day is not in the current month.
    new_days = [str(day) for day in range(1, last_day_of_month + 1)]
    if not day in new_days:
            day = 1
    window[day_widget].update(values=new_days, value=day)
    # Update the text widget to display the day, month, and year.
    window[text_widget].update("{} {}, {}".format(month, day, year))


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

    # Build the interface.
    sg.theme('DarkAmber')
    layout = [  [sg.Text("Old semester start date:"),
                 sg.Text("January 1, 2019", key = "OLD_SEMESTER_DATE")],
                 [sg.Combo(MONTHS, key="OLD_MONTH", enable_events=True,
                          default_value=MONTHS[0]),
                 sg.Combo([str(day) for day in range(1, 32)], key="OLD_DAY",
                          enable_events=True, default_value=1),
                 sg.Combo([str(year) for year in range(2019,2030)], key="OLD_YEAR",
                          enable_events=True, default_value=2019)
                  ]
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
        elif event == "OLD_MONTH" or event == "OLD_YEAR" or event == "OLD_DAY":
            update_date(window, values, "OLD_MONTH","OLD_DAY", "OLD_YEAR",
                        "OLD_SEMESTER_DATE")
  

    window.close()

if __name__ == "__main__":
    main()
