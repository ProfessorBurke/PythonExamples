"""
    Shabby Abbey v3
    Obtain a command from the player and move them based on the command.

    Maggie
    9/27/2025
"""
# Define constants.
DIRECTIONS: list[str] = ["N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"]
NAME: int = 0
DESCRIPTION: int = 1
EXITS: int = 2
NORTH: int = 3
SOUTH: int = 4
EAST: int = 5
WEST: int = 6

# Annotate and initialize variables.
command: str
current_location: int = 5
location_index: int
abbey: list[list[str|int]] = [["cloister", "You are in a courtyard.",
          "There are exits to the (N)orth, (S)outh, (E)ast, and (W)est.",
          1, 2, 3, 4],
         ["church", "In front of you is a large stone church.",
          "There is an exit to the (S)outh.",
          -1, 0, -1, -1],
         ["kitchen", "Kitchen or torture chamber?",
          "There is an exit to the (N)orth.",
          0, -1, -1, -1],
         ["library", "A monastic library.",
          "There are exits to the (N)orth and (W)est.",
          5, -1, -1, 0],
         ["garden", "An overgrown garden.",
          "There is an exit to the (E)ast.",
          -1, -1, 0, -1],
         ["storage room", "Artifacts, old manuscripts, and lots of dust!",
          "There is an exit to the (S)outh.",
          -1, 3, -1, -1]]

# Greet the player.
print("Welcome, Adventurer!")

# Describe the current location.
print("You're in the " + abbey[current_location][NAME] + ".")
print(abbey[current_location][EXITS])

# Obtain the player's command and convert to uppercase.
command = input("What is your command? ")
command = command.upper()

# Move the player based on their command.
if command in DIRECTIONS:
    command = command[0]
    location_index = DIRECTIONS.index(command) + NORTH
    if abbey[current_location][location_index] != -1:
        current_location = abbey[current_location][location_index] 
else:
    print("I didn't understand that command.")

print("You're in the " + abbey[current_location][NAME] + ".")
print(abbey[current_location][EXITS])

print("Thank you for playing.")

