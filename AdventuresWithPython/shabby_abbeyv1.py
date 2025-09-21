"""
    Shabby Abbey v1
    Obtain a command from the player and manipulate it.
    Maggie
    9/17/2025
"""
# Annotate variable.
command: str

# Greet the player.
print("Welcome, Adventurer!")

# Obtain the player's command and manipulate it.
command = input("What is your command? ")
print("Your command is " + command)
print("The first letter of your command is " + command[0])
print("Your command in uppercase is " + command.upper())
print("Your command in lowercase is " + command.lower())
