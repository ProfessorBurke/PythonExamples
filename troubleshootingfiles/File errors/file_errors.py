""" Open a file, read all lines, and print them
    to the screen.
"""
import io
import traceback

file_name: str = "movies_file.txt"
file: io.TextIOWrapper = open(file_name)

line: str = file.readline()
while line != "":
    print(line.strip())
    line = file.readline()

file.close()



# It doesn't matter what syntax you use to open the file,
# if the file isn't found, Python will throw an
# exception!
try:
    with open(file_name) as file:
        file.close()
except FileNotFoundError:
    traceback.print_exc()
