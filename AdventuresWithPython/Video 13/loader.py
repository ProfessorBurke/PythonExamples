from inventory import Inventory
from location import Location
from item import Item
import json
import typing

class Loader:
    """
        Description

        Attributes:
            _save_path: str
            _start_path: str

    """

    # Class-level constants:
    START: int = 0
    SAVE: int = 1

    def __init__(self) -> None:
        """Set the save and start paths."""
        self._start_path = "abbey.json"
        self._save_path = "save.json"

    def save_abbey(self, data_in: dict[str, object]) -> bool:
        """Save the abbey dungeon to save file and return True if
           successful and False otherwise.
           DATA_IN -- the data coming in is:
           - current_location: a Location object
           - player_inventory: an Inventory object
           - location_lookup: a dictionary of name-Location object pairs
           DATA_OUT -- the data going to the file is:
           - current_location: the name of the current location (a string)
           - player_inventory: a serialized inventory 
           - location_lookup: a dictionary of name - serialized location objects
        """
        f: typing.TextIO                    # The file reference variable
        success: boolean = True             # Whether an error occured; returned.
        locations: [dict[str, object]]      # Serialized list of locations for DATA_OUT.
        location: Location                  # The next location to serialize in DATA_IN.
        data_out: dict[str, object] = {}    # The dictionary going to the file (DATA_OUT).
        try:
            with open(self._save_path, "w") as f:
                # Put a serialized player inventory in data_out.
                data_out["player_inventory"] = data_in["player_inventory"].to_json()
                # Put serialized locations in a list and then in data_out.
                locations = {}
                for name, location in data_in["location_lookup"].items():
                    locations[name] = location.to_json()
                data_out["location_lookup"] = locations
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

    def load_abbey(self, from_: int) -> dict[str, object]:
        """Load the abbey dungeon from save file or start file according
           to the value of from_ or return a default dungeon.  
           DATA_IN -- the data from the file is:
           - current_location: the name of the current location (a string)
           - player_inventory: a serialized inventory 
           - location_lookup: a dictionary of location name - serialized location object pairs
           DATA_OUT -- the data being returned is:
           - current_location: a Location object
           - player_inventory: an Inventory object
           - location_lookup: a dictionary of location name - location object pairs
        """
        
        data_in: dict[str, object]                  # The data read in from the JSON file.
        data_out: dict[str, object]                 # The data to return.
        json_location: dict[str, object]            # The JSON data for one location.
        location: Location                          # The Location object currently being constructed.
        inventory: Inventory                        # The Inventory object currently being constructed.
        name_location: dict[str, Location] = {}     # The dictionary of location name-Location object pairs.
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
                    "location_lookup": {"dark room": location}}
        try:
            if from_ == Loader.START:
                file_name = self._start_path
            else:
                file_name = self._save_path
            with open(file_name, "r") as f:
                data_in = json.load(f)
                # Convert the serialized player inventory to an Inventory
                # object and add to data_out.
                inventory = Inventory()
                inventory.from_json(data_in["player_inventory"])
                data_out["player_inventory"] = inventory
                # Convert each serialized location to a Location object,
                # And populate name_exits and name_location for pass 2
                for name, json_location in data_in["location_lookup"].items():
                    location = Location()
                    location.from_json(json_location)
                    name_location[location.get_name()] = location
                # Add the name-location lookup table to data_out.
                data_out["location_lookup"] = name_location
                # The current Location object is current_location in data_in.
                data_out["current_location"] = name_location[data_in["current_location"]]
        except FileNotFoundError:
            print(f"***File not found: {file_name}***")
        except json.JSONDecodeError:
            print(f"***Invalid JSON format in file: {file_name}***")
        except Exception as e:
            print(f"***An unexpected error occurred: {e}***")
        return data_out   
