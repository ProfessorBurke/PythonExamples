"""
    Write a program that combines several files into one.
    The program asks the user for the name of the directory containing
    the files to be consolidated.  It then consolidates all files in that
    directory into one file in that directory called consolidated.txt.

"""
# Import file libraries.
from io import TextIOWrapper
import os

# Annotate variables.
in_file: TextIOWrapper
out_file: TextIOWrapper
dir_name: str
file_name: str
file_path: str
files: list
line: str
e: Exception

# Get the directory name from the user.
dir_name = input("Please enter the name of the folder with the files: ")

# Try listing the files in the directory and throw an exception if we can't.
try:
    files = os.listdir(dir_name)
except Exception as e:
    print("Couldn't list files in the directory {}.".format(dir_name))

# We've got the directory files, open and consolidate.
else:
    # Try opening the output file in the directory.
    try:
        outfile = open(os.path.join(dir_name, "consolidated.txt"), "w")
    except Exception as e:
        print("Something went wrong while opening the output file.")

    # The output file has successfully been opened.
    else:
        # Consolidate the files in the directory.
        for file_name in files:
            # Create the path to the file through the directory.
            file_path = os.path.join(dir_name, file_name)
            # If it's a file, write the lines of the file to out_file.
            if os.path.isfile(file_path) and not file_name.startswith("."):
                try:
                    with open(file_path) as in_file:
                        for line in in_file:
                            out_file.write(line)
                    # Let the user know the file was consolidated.
                    print("{} has been consolidated.".format(file_name))
                except Exception as e:
                    print("There was a problem with {}.".format(file_name))       
    
        # Close the consolidation file.
        out_file.close()
    
