"""
    Shabby Abbey v9
    Obtain a command from the player and respond to it until
    the user chooses to quit.
    Maggie
    11/8/2025
"""
import json
import typing
import copy
from Inventory import Inventory

# Define constants.
DIRECTIONS: tuple[str] = ("N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST")
QUIT_COMMANDS: tuple[str] = ("Q", "QUIT")
LOOK_COMMANDS: tuple[str] = ("L", "LOOK")
TAKE_COMMANDS: tuple[str] = ("T", "TAKE")
DROP_COMMANDS: tuple[str] = ("D", "DROP")
SAVE_COMMANDS: tuple[str] = ("V", "SAVE")
RESTORE_COMMANDS: tuple[str] = ("R", "RESTORE")
INVENTORY_COMMANDS: tuple[str] = ("I", "INVENTORY")
EXAMINE_COMMANDS: tuple[str] = ("X", "EXAMINE")
DIRECTIONS_STRING: tuple[str] = ("(N)orth", "(S)outh", "(E)ast", "(W)est")


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

def get_description(location: dict[str, object], long: bool = False) -> str:
    """Return the short or long description of the location, long if it
       hasn't been visited before or long is True; short otherwise."""
    description: str
    # If first time visiting or long requested, get the description.
    if long or location["visits"] == 0:
        description = location["description"]
    # Otherwise just the name of the location.
    else:
        description = location["name"]
    # Add the items that are here.
    if not location["inventory"].is_empty():
        description += "\nYou see:\n"
        description += str(location["inventory"])
    return description

def inventory_swap(from_inventory: Inventory, to_inventory: Inventory,
                   item: str, action: str) -> None:
    """Remove the item from the from_inventory and place in the to_inventory,
       if it is in the from_inventory.  Print an appropriate message if not."""
    # Attempt to exchange the item.
    if from_inventory.exchange_item(item, to_inventory):
        print(item + " has been " + action + ".")
    # If the item was not successfully exchanged.
    else:
        print("I don't see " + item + ".")

def save_abbey(abbey: dict[str, object], file_name: str) -> bool:
    """Save the abbey dungeon to the file file_name and return True if
       successful, and False otherwise."""
    f: typing.TextIO
    success: boolean = True
    location: dict[str, object]
    try:
        with open(file_name, "w") as f:
            # Convert the player Inventory to a JSON format.
            abbey["player_inventory"] = abbey["player_inventory"].to_json()
            # Convert the inventory objects in the dungeon to JSONS.
            for location in abbey["dungeon"]:
                location["inventory"] = location["inventory"].to_json()
            json.dump(abbey, f, indent=4)
    except PermissionError:
        print(f"***Permission denied: cannot write to {file_name}***")
        success = False
    except TypeError as e:
        print(f"***Unable to serialize data to JSON: {e}***")
        success = False
    except OSError as e:
        print(f"***File system error while saving {file_name}: {e}***")
        success = False        
    except Exception as e:
        print(f"***An unexpected error occurred: {e}***")
        success = False
    return success 

def load_abbey(file_name: str) -> dict[str, object]:
    """Load the abbey dungeon from the file file_name or
       return a default dungeon."""
    abbey: dict[str, object]
    location: dict[str, object]
    inventory: Inventory
    f: typing.TextIO
    abbey = {"current_location": 0,
             "player_inventory": Inventory(),
             "dungeon": [{"name": "dark room",
                          "description": "You are in a dark room with no exits.  Best go home.",
                          "exits": {},
                          "visits": 0,
                          "inventory": Inventory()}]}
    try:
        with open(file_name, "r") as f:
            abbey = json.load(f)
            # Convert the player inventory dict to an Inventory object.
            inventory = Inventory()
            inventory.from_json(abbey["player_inventory"])
            abbey["player_inventory"] = inventory
            # Convert each location's inventory dict to an Inventory object.
            for location in abbey["dungeon"]:
                inventory = Inventory()
                inventory.from_json(location["inventory"])
                location["inventory"] = inventory
    except FileNotFoundError:
        print(f"***File not found: {file_name}***")
    except json.JSONDecodeError:
        print(f"***Invalid JSON format in file: {file_name}***")
    except Exception as e:
        print(f"***An unexpected error occurred: {e}***")
    return abbey    
    
def main() -> None:
    """Obtain and process commands from the player until they choose to quit."""
    # Annotate and define constants.
    START_DUNGEON: str = "abbey.json"
    SAVE_DUNGEON: str = "save.json"
    
    # Define the dungeon.
    abbey: list[dict[str, object]]
    data: dict[str, object]
    data = load_abbey(START_DUNGEON)
    abbey = data["dungeon"]
    current_location: int = data["current_location"]
    player_inventory: Inventory = data["player_inventory"]
    
    # Annotate variables.
    command: str = ""
    command_parts: list[str]

    # Greet the player.
    print("Welcome, Adventurer!")

    while not command in QUIT_COMMANDS:
        # Describe the current location.
        print(get_description(abbey[current_location]))
        print(get_exits_string(abbey[current_location]["exits"]))
        abbey[current_location]["visits"] += 1

        # Obtain the player's command and convert to uppercase, split, take the first letter
        # of the command.
        command = input("What is your command? ")
        command_parts = command.split()
        if len(command_parts) > 0:
            command = command_parts[0].upper()

        # Move the player if a direction command.
        if command in DIRECTIONS:
            command = command[0]
            if command in abbey[current_location]["exits"]:
                current_location = abbey[current_location]["exits"][command]
        # Handle save and restore.
        elif command in SAVE_COMMANDS:
            # Create a dictionary of data to be saved.
            data = {"dungeon": abbey, "current_location": current_location,
                    "player_inventory": player_inventory}
            # Save it.
            if save_abbey(copy.deepcopy(data), SAVE_DUNGEON):
                print("Saved.")
            else:
                print("There was a problem saving.")
        elif command in RESTORE_COMMANDS:
            # Load the dictionary of data and save it in appropriate variables.
            data = load_abbey(SAVE_DUNGEON)
            abbey = data["dungeon"]
            current_location = data["current_location"]
            player_inventory = data["player_inventory"]
        # Handle a look command.
        elif command in LOOK_COMMANDS:
            print(get_description(abbey[current_location], True))
        # Handle inventory commands.
        elif command in TAKE_COMMANDS:
            if len(command_parts) > 1:
                inventory_swap(abbey[current_location]["inventory"], player_inventory,
                               command_parts[1], "taken")
            else:
                print("You must take something.")
        elif command in DROP_COMMANDS:
            if len(command_parts) > 1:
                inventory_swap(player_inventory, abbey[current_location]["inventory"], 
                               command_parts[1], "dropped")
            else:
                print("You must drop something.")
        elif command in INVENTORY_COMMANDS:
            if player_inventory.is_empty():
                print("You aren't carrying anything.")
            else:
                print("You have:")
                print(player_inventory)
        elif command in EXAMINE_COMMANDS:
            if len(command_parts) > 1:
                if command_parts[1] in player_inventory:
                    print(player_inventory.examine(command_parts[1]))
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

