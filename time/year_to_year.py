"""
    Convert a calendar from one year to the next year.
"""
from datetime import date
from datetime import timedelta
import re


def get_full_date(prompt: str) -> date:
    """Obtain a full date string from the user and return as a date object."""
    date_str: str
    input_error: bool = True
    y: str
    m: str
    d: str
    input_date: date
    
    while input_error:
        print("Please enter the date as year, month, day, e.g. 2023, 1, 22")
        date_str = input(prompt)
        try:
            y,m,d = date_str.split(",")
            input_date = date(int(y),int(m),int(d))
            input_error = False
        except:
            print("I'm sorry, your date was not in a usable format.")
    return input_date

def get_file_contents(prompt: str) -> list:
    """Get a file name from the user, open the file and read the contents
       into a list and return.  If there's a file error, return an
       empty list."""
    file_name: str
    contents: list = []
    in_file: "file"
    
    file_name = input(prompt)
    try:
        with open(file_name) as in_file:
            contents = in_file.readlines()
            in_file.close()
    except:
        print("I'm sorry, there was an error with the file.")
    return contents

def write_file(contents: list) -> None:
    """Get a file name from the user, open the file and write contents
       to the file, one element to a line."""
    file_name: str
    out_file: "file"
    file_name = input("What would you like to name the output file? ")
    try:
        with open(file_name, "w") as out_file:
            for line in contents:
                out_file.write(line)
            out_file.close()
    except:
        print("I'm sorry, there was an error with the file.")
            

def convert_date(old_start: date, new_start: date, old_assignment: date) -> date:
    """Convert the old assignment date to the date for the new semester."""
    return new_start + (old_assignment - old_start)

def main() -> None:
    """Get the old and new semester start dates and the old calendar.
       Convert the old calendar to a new calendar and write to a file."""

    # Annotate variables.
    old_semester_start: date
    new_semester_start: date
    new_date: date
    calendar: list
    i: int
    match: re.Match
    m: str
    d: str

    # Get the old semester and new semester start dates
    # from the user.  
    old_semester_start = get_full_date("What is the old semester start date? ")
    new_semester_start = get_full_date("What is the new semester start date? ")
    
    # Get the old semester due dates file from the user.
    # Read in the lines of the file as a list.
    calendar = get_file_contents("Please enter the file with the old calendar: ")

    # Adjust all of the calendar dates for the new semester.
    for i in range(len(calendar)):
        # Find each date in the line and process it.
        for match in re.finditer(r'(\d+/\d+)', calendar[i]):
            # Update the date to the equivalent new semester date.
            m, d = match.group(1).split("/")
            new_date = convert_date(old_semester_start, new_semester_start,
                                    date(old_semester_start.year, int(m), int(d)))
            # Replace the old date with the new date in the calendar.
            calendar[i] = (calendar[i][:match.start()] +
                           str(new_date.month) + "/" +
                           str(new_date.day) + calendar[i][match.end():])

    # Write the calendar to a new file
    write_file(calendar)


if __name__ == "__main__":
    main()
