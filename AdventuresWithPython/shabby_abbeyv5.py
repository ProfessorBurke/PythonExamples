"""
    Shabby Abbey v5
    Obtain a command from the player and respond to it until
    the user chooses to quit.
    Maggie
    10/10/2025
"""
# Define constants.
DIRECTIONS: tuple[str] = ("N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST")
QUIT_COMMANDS: tuple[str] = ("Q", "QUIT")
DIRECTIONS_STRING: tuple[str] = ("(N)orth", "(S)outh", "(E)ast", "(W)est")

NAME: int = 0
DESCRIPTION: int = 1
EXITS: int = 2
NORTH: int = 0
SOUTH: int = 1
EAST: int = 2
WEST: int = 3

def get_exits_string(exits_list: list[int]) -> str:
    """Generate and return a string describing the exits from the list."""
    
    exits_str : str
    exits: list[str] = [DIRECTIONS_STRING[i] for i in range(len(exits_list))
                  if exits_list[i] != -1]

    if len(exits) == 0:
        exits_str = "There are no exits."
    elif len(exits) == 1:
        exits_str = "There is an exit to the " + exits[0] + "."
    else:
        exits_str = ("There are exits to the " + ", ".join(exits[:-1])
                     + " and " + exits[-1] + ".")
    return exits_str
    
def main() -> None:
    """Obtain and process commands from the player until they choose to quit."""
    abbey: list[str | list] = [["cloister", "You are in a courtyard.",
                    [1, 2, 3, 4]],
                   ["church", "In front of you is a large stone church.",
                    [-1, 0, -1, -1]],
                   ["kitchen", "Kitchen or torture chamber?",
                    [0, -1, -1, -1]],
                   ["library", "A monastic library.",
                    [5, -1, -1, 0]],
                   ["garden", "An overgrown garden.",
                    [-1, -1, 0, -1]],
                   ["storage room", "Artifacts, old manuscripts, and dust.",
                    [-1, 3, -1, -1]]]

    # Annotate variable.
    command: str = ""
    current_location: int = 0
    location_index: int

    # Greet the player.
    print("Welcome, Adventurer!")

    while not command in QUIT_COMMANDS:
        # Describe the current location.
        print("You're in the " + abbey[current_location][NAME] + ".")
        print(get_exits_string(abbey[current_location][EXITS]))

        # Obtain the player's command and convert to uppercase, take the first letter.
        command = input("What is your command? ")
        command = command.upper()

        # Move the player based on their command.
        if command in DIRECTIONS:
            command = command[0]
            location_index = DIRECTIONS.index(command) 
            if abbey[current_location][EXITS][location_index] != -1:
                current_location = abbey[current_location][EXITS][location_index]
        elif not command in QUIT_COMMANDS:
            print("I didn't understand that command.")


    print("Thank you for playing.")

if __name__ == "__main__":
    main()
