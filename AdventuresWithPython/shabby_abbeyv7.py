"""
    Shabby Abbey v7
    Obtain a command from the player and respond to it until
    the user chooses to quit.
    Maggie
    10/20/2025
"""
# Define constants.
DIRECTIONS: tuple[str] = ("N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST")
QUIT_COMMANDS: tuple[str] = ("Q", "QUIT")
LOOK_COMMANDS: tuple[str] = ("L", "LOOK")
TAKE_COMMANDS: tuple[str] = ("T", "TAKE")
DROP_COMMANDS: tuple[str] = ("D", "DROP")
INVENTORY_COMMANDS: tuple[str] = ("I", "INVENTORY")
EXAMINE_COMMANDS: tuple[str] = ("X", "EXAMINE")
DIRECTIONS_STRING: tuple[str] = ("(N)orth", "(S)outh", "(E)ast", "(W)est")

NAME: int = 0
DESCRIPTION: int = 1
EXITS: int = 2
VISITS: int = 3
INVENTORY: int = 4

def get_exits_string(exits_dict: dict[str, int]) -> str:
    """Generate and return a string describing the exits from the dictionary."""
    
    exits_str : str
    # Turn the exits keys into direction strings for the player.
    exits: list[str] = [DIRECTIONS_STRING[DIRECTIONS.index(key)]
                        for key in exits_dict]
    
    # Compose the string based on how many exits there are.
    if len(exits) == 0:
        exits_str = "There are no exits."
    elif len(exits) == 1:
        exits_str = "There is an exit to the " + exits[0] + "."
    else:
        exits_str = ("There are exits to the " + ", ".join(exits[:-1])
                     + " and " + exits[-1] + ".")
    return exits_str

def get_description(location: list[str | int | dict], long: bool = False) -> str:
    """Return the short or long description of the location, long if it
       hasn't been visited before or long is True; short otherwise."""
    description: str
    # If first time visiting or long requested, get the description.
    if long or location[VISITS] == 0:
        description = location[DESCRIPTION]
    # Otherwise just the name of the location.
    else:
        description = location[NAME]
    # Add the items that are here.
    if location[INVENTORY]:
        description += "\nThere is a " + ".\nThere is a ".join(location[INVENTORY]) + "."
    return description

def inventory_swap(from_inventory: dict[str,str], to_inventory: dict[str, str],
                   item: str, action: str) -> None:
    """Remove the item from the from_inventory and place in the to_inventory,
       if it is in the from_inventory.  Print an appropriate message if not."""
    # If the item is in from_inventory, swap to to_inventory and print a message.
    if item in from_inventory:
        to_inventory[item] = from_inventory[item]
        del from_inventory[item]
        print(item + " has been " + action + ".")
    # If the item is not in from_inventory, print a message.
    else:
        print("I don't see " + item + ".")
    
def main() -> None:
    """Obtain and process commands from the player until they choose to quit."""
    # Define the dungeon.
    abbey: list[str | int | dict] = [["cloister", "You are in a courtyard.",
                    {"N":1, "S":2, "E":3, "W":4}, 0, {}],
                   ["church", "In front of you is a large stone church.",
                    {"S":0}, 0,
                    {"book": "An ancient book with a decorative leather cover."}],
                   ["kitchen", "Kitchen or torture chamber?",
                    {"N":0}, 0,
                    {"knife": "A rusty knife with an engraved handle.",
                     "skull": "A tiny rat skull on a silver chain."}],
                   ["library", "A monastic library.",
                    {"N":5, "W":0}, 0, {}],
                   ["garden", "An overgrown garden.",
                    {"E":0}, 0, {}],
                   ["storage room", "Artifacts, old manuscripts, and dust.",
                    {"S":3}, 0, {}]]

    # Annotate variables.
    command: str = ""
    current_location: int = 0
    player_inventory: dict[str, str] = {}
    command_parts: list[str]

    # Greet the player.
    print("Welcome, Adventurer!")

    while not command in QUIT_COMMANDS:
        # Describe the current location.
        print(get_description(abbey[current_location]))
        print(get_exits_string(abbey[current_location][EXITS]))
        abbey[current_location][VISITS] += 1

        # Obtain the player's command and convert to uppercase, split, take the first letter
        # of the command.
        command = input("What is your command? ")
        command_parts = command.split()
        if len(command_parts) > 0:
            command = command_parts[0].upper()

        # Move the player if a direction command.
        if command in DIRECTIONS:
            command = command[0]
            if command in abbey[current_location][EXITS]:
                current_location = abbey[current_location][EXITS][command]
        # Handle a look command.
        elif command in LOOK_COMMANDS:
            print(get_description(abbey[current_location], True))
        # Handle inventory commands.
        elif command in TAKE_COMMANDS:
            if len(command_parts) > 1:
                inventory_swap(abbey[current_location][INVENTORY], player_inventory,
                               command_parts[1], "taken")
            else:
                print("You must take something.")
        elif command in DROP_COMMANDS:
            if len(command_parts) > 1:
                inventory_swap(player_inventory, abbey[current_location][INVENTORY], 
                               command_parts[1], "dropped")
            else:
                print("You must drop something.")
        elif command in INVENTORY_COMMANDS:
            print("You have:\n\t" + "\n\t".join(player_inventory))
        elif command in EXAMINE_COMMANDS:
            if len(command_parts) > 1:
                if command_parts[1] in player_inventory:
                    print(player_inventory[command_parts[1]])
                else:
                    print("You don't have a " + command_parts[1] + ".")
            else:
                print("You must examine something.")
        # Handle an unrecognizable command.
        elif not command in QUIT_COMMANDS:
            print("I didn't understand that command.")


    print("Thank you for playing.")

if __name__ == "__main__":
    main()
