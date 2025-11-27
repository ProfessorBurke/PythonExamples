"""
    Shabby Abbey v11
    Obtain a command from the player and respond to it until
    the user chooses to quit.
    Maggie
    11/23/2025
"""
import json
import typing
from inventory import Inventory
from location import Location
from commands2 import Command, CommandType

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

def save_abbey(data_in: dict[str, object], file_name: str) -> bool:
    """Save the abbey dungeon to the file file_name and return True if
       successful and False otherwise.
       DATA_IN -- the data coming in is:
       - current_location: a Location object
       - player_inventory: an Inventory object
       - dungeon: a list of Location objects
       DATA_OUT -- the data going to the file is:
       - current_location: the name of the current location (a string)
       - player_inventory: a serialized inventory 
       - dungeon: a list of serialized locations
    """
    f: typing.TextIO                    # The file reference variable
    success: boolean = True             # Whether an error occured; returned.
    locations: list[dict[str, object]]  # Serialized list of locations for DATA_OUT.
    location: Location                  # The next location to serialize in DATA_IN.
    data_out: dict[str, object] = {}    # The dictionary going to the file (DATA_OUT).
    try:
        with open(file_name, "w") as f:
            # Put a serialized player inventory in data_out.
            data_out["player_inventory"] = data_in["player_inventory"].to_json()
            # Put serialized locations in a list and then in data_out.
            locations = []
            for location in data_in["dungeon"]:
                locations.append(location.to_json())
            data_out["dungeon"] = locations
            # Put the name of the current location in data_out.
            data_out["current_location"] = data_in["current_location"].get_name()
            json.dump(data_out, f, indent=4)
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
       return a default dungeon.  
       DATA_IN -- the data from the file is:
       - current_location: the name of the current location (a string)
       - player_inventory: a serialized inventory 
       - dungeon: a list of serialized locations
       DATA_OUT -- the data being returned is:
       - current_location: a Location object
       - player_inventory: an Inventory object
       - dungeon: a list of Location objects
    """
    
    data_in: dict[str, object]                  # The data read in from the JSON file.
    data_out: dict[str, object]                 # The data to return.
    json_location: dict[str, object]            # The JSON data for one location.
    location: Location                          # The Location object currently being constructed.
    inventory: Inventory                        # The Inventory object currently being constructed.
    name_location: dict[str, Location] = {}     # The dictionary of location name-Location object pairs.
    name_exits: dict[str, dict[str,str]] = {}   # The dictionary of location name-exits dict pairs. Temporary.
    f: typing.TextIO                            # The JSON file we're reading.
    
    # Create the default data to return in case there's an error reading
    location = Location()
    location.from_json({"name": "dark room",
                          "description": "You are in a dark room with no exits.  Best go home.",
                          "exits": {},
                          "visits": 0,
                          "inventory": {}})
    data_out = {"current_location": location,
                "player_inventory": Inventory(),
                "dungeon": [location]}
    try:
        with open(file_name, "r") as f:
            data_in = json.load(f)
            # Convert the serialized player inventory to an Inventory object and add to data_out.
            inventory = Inventory()
            inventory.from_json(data_in["player_inventory"])
            data_out["player_inventory"] = inventory
            # Pass #1, convert each serialized location to a Location object,
            # And populate name_exits and name_location for pass 2
            for json_location in data_in["dungeon"]:
                location = Location()
                exits = location.from_json(json_location)
                name_exits[location.get_name()] = exits
                name_location[location.get_name()] = location
            # Pass #2, connect the locations together.
            for name, exits in name_exits.items():
                location = name_location[name]
                for exit_str, traveling_to in exits.items():
                    location.add_exit(exit_str, name_location[traveling_to])
            # Create a list of just the Location objects and add to data_out.
            data_out["dungeon"] = list(name_location.values())
            # The current Location object is current_location in data_in.
            data_out["current_location"] = name_location[data_in["current_location"]]
    except FileNotFoundError:
        print(f"***File not found: {file_name}***")
    except json.JSONDecodeError:
        print(f"***Invalid JSON format in file: {file_name}***")
    except Exception as e:
        print(f"***An unexpected error occurred: {e}***")
    return data_out    
    
def main() -> None:
    """Obtain and process commands from the player until they choose to quit."""
    # Annotate and define constants.
    START_DUNGEON: str = "abbey.json"
    SAVE_DUNGEON: str = "save.json"
    
    # Define the dungeon.
    data: dict[str, object]
    data = load_abbey(START_DUNGEON)
    current_location: Location = data["current_location"]
    player_inventory: Inventory = data["player_inventory"]
    
    # Annotate variables.
    user_input: str = ""
    next_location: Location
    command: Command = Command("UNKNOWN")
    direction: str
    item: str

    # Greet the player.
    print("Welcome, Adventurer!")

    while not command.is_type(CommandType.QUIT):
        # Describe the current location.
        print(current_location.get_description())

        # Obtain the player's input and instantiate a command.
        user_input = input("What is your command? ")
        command = Command(user_input)

        # Move the player if a direction command.
        if command.is_type(CommandType.MOVE):
            direction = command.get_object()
            next_location = current_location.go(direction)
            if next_location is None:
                print("There's no exit in that direction.")
            else:
                current_location = next_location
        # Handle save and restore.
        elif command.is_type(CommandType.SAVE):
            # The locations and player_inventory are already in the dictionary,
            # Set the current_location to current_location and save.
            data["current_location"] = current_location
            # Save it.
            if save_abbey(data, SAVE_DUNGEON):
                print("Saved.")
            else:
                print("There was a problem saving.")
        elif command.is_type(CommandType.RESTORE):
            # Load the dictionary of data and save it in appropriate variables.
            data = load_abbey(SAVE_DUNGEON)
            current_location = data["current_location"]
            player_inventory = data["player_inventory"]
        # Handle a look command.
        elif command.is_type(CommandType.LOOK):
            print(current_location.get_long_description())
        # Handle inventory commands.
        elif command.is_type(CommandType.TAKE):
            item = command.get_object()
            if item is None:
                print("You must take something.")
            else:
                inventory_swap(current_location.get_inventory(), player_inventory,
                               item, "taken")
        elif command.is_type(CommandType.DROP):
            item = command.get_object()
            if item is None:
                print("You must drop something.")
            else:
                inventory_swap(player_inventory, current_location.get_inventory(),
                               item, "dropped")
        elif command.is_type(CommandType.INVENTORY):
            if player_inventory.is_empty():
                print("You aren't carrying anything.")
            else:
                print("You have:")
                print(player_inventory)
        elif command.is_type(CommandType.EXAMINE):
            item = command.get_object()
            if item is None:
                print("You must examine something.")
            else:
                if item in player_inventory:
                    print(player_inventory.examine(item))
                else:
                    print("You don't have ", end="")
                    print("an " if item.lower()[0] in ["a", "e", "i", "o", "u"] else "a ", end="")
                    print(item + ".")
        # Handle an unrecognizable command.
        elif command.is_type(CommandType.UNKNOWN):
            print("I didn't understand that command.")


    print("Thank you for playing.")

if __name__ == "__main__":
    main()
