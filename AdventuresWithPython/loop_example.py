"""
    Example of a while loop.
    10/3/2025
"""
command: str

command = input("What is your command? ")
print("You commanded " + command)

while command.upper() != "Q":
    command = input("What is your command? ")
    print("You commanded " + command)

print("And I did quit!")
