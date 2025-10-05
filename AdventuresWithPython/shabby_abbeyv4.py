"""
    Shabby Abbey v4
    Obtain a command from the player and manipulate it until
    the user chooses to quit.
    Maggie
    10/03/2025
"""
# Define constants.
DIRECTIONS: list[str] = ["N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"]
QUIT_COMMANDS: list[str] = ["Q", "QUIT"]

NAME: int = 0
DESCRIPTION: int = 1
EXITS: int = 2
NORTH: int = 3
SOUTH: int = 4
EAST: int = 5
WEST: int = 6

abbey: list = [["cloister", "You are in a courtyard.",
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
               ["storage room", "Artifacts, old manuscripts, and dust.",
                "There is an exit to the (S)outh.",
                -1, 3, -1, -1]]

# Annotate variable.
command: str = ""
current_location: int = 0
location_index: int

# Greet the player.
print("Welcome, Adventurer!")

while not command in QUIT_COMMANDS:
    # Describe the current location.
    print("You're in the " + abbey[current_location][NAME] + ".")
    print(abbey[current_location][EXITS])

    # Obtain the player's command and convert to uppercase, take the first letter.
    command = input("What is your command? ")
    command = command.upper()

    # Move the player based on their command.
    if command in DIRECTIONS:
        command = command[0]
        location_index = DIRECTIONS.index(command) + NORTH
        if abbey[current_location][location_index] != -1:
            current_location = abbey[current_location][location_index]
    elif not command in QUIT_COMMANDS:
        print("I didn't understand that command.")


print("Thank you for playing.")

