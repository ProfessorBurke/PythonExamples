"""
    Write a program that combines several files into one.
    The program asks the user for file names in a loop until the
    user types "done."  For each file name, the program should
    check if the file exists, and if it does, it should read every
    value in the file and append it to a file called consolidated.txt.

    For simplicity, each file should be in the same directory as the program.
    If the file doesn’t exist, the program should tell the user it couldn’t
    find the file.  If it does exist, the program should print a message
    letting the user know the file’s contents were added to consolidated.txt.

    To test this program, you should create several text files to be
    consolidated into one and put them in the same directory as your program.

"""
# Import file libraries.
from io import TextIOWrapper
import os.path

# Annotate variables.
in_file: TextIOWrapper
out_file: TextIOWrapper
file_name: str
line: str

# Open the consolidation file for writing.
out_file = open("consolidated.txt", "w")

# Get the first file name (or "done") from the user.
file_name = input("Please enter a file to be consolidated, or 'done' to quit: ")

# Consolidate the files until the user is done.
while file_name.lower() != "done":
    if os.path.isfile(file_name):
        # Read all lines from in_file and write them to out_file.
        in_file = open(file_name)
        line = in_file.readline()
        while line != "":
            out_file.write(line)
            line = in_file.readline()
        # Close the file we just consolidated.
        in_file.close()
        # Let the user know the file was consolidated.
        print("{} has been consolidated.".format(file_name))
    else:
        # Print a message if the file doesn't exist.
        print("Can't find {}.".format(file_name))

    # Get the next name (or "done") from the user.
    file_name = input("Please enter the next file to be consolidated, or 'done' to quit: ")

# Close the consolidation file.
out_file.close()
    
