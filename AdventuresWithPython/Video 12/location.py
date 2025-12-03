from __future__ import annotations
from inventory import Inventory

class Location:
    """
        A Location in the dungeon.

        Attributes:
            _name: str
            _description: str
            _num_visits: int
            _exits: dict[str, Location]
            _inventory: Inventory
    """

    _DIRECTION_NAMES: dict[str, str] = {
        "N": "(N)orth",
        "S": "(S)outh",
        "E": "(E)ast",
        "W": "(W)est"
    }

    def __init__(self) -> None:
        """Initialize a Location with default values.  The Location
           data should be set with from_json and add_exit."""
        self._name = ""
        self._description = ""
        self._num_visits = 0
        self._exits = {}
        self._inventory = Inventory()

    def _get_exits_string(self) -> str:
        """Create a string describing the visible exits."""
        exits_str : str
        # Turn the exits keys into direction strings for the player.
        exits: list[str] = [Location._DIRECTION_NAMES[direction]
                            for direction in self._exits]
        
        # Compose the string based on how many exits there are.
        if len(exits) == 0:
            exits_str = "There are no exits."
        elif len(exits) == 1:
            exits_str = "There is an exit to the " + exits[0] + "."
        else:
            exits_str = ("There are exits to the " + ", ".join(exits[:-1])
                         + " and " + exits[-1] + ".")
        return exits_str

    def get_name(self) -> str:
        """Return this location's name."""
        return self._name

    def get_long_description(self) -> str:
        """Return a detailed description of the location, including
           inventory items."""
        description: list = []
        description.append(self._name)
        description.append(self._description) 
        description.append(self._get_exits_string())
        if not self._inventory.is_empty():
            description.append("You see:\n" + str(self._inventory))
        return "\n".join(description)

    def get_description(self) -> str:
        """Return this location's description, including inventory items."""
        description_str: str 
        if self._num_visits > 0:
            description_str = self._name + "\n"
            if not self._inventory.is_empty():
                description_str += "You see:\n" + str(self._inventory)
        else:
            description_str = self.get_long_description()
        return description_str


    def get_inventory(self) -> Inventory:
        """Return a reference to this location's inventory object."""
        return self._inventory

    def add_exit(self, direction: str, location: "Location") -> None:
        self._exits[direction] = location

    def go(self, direction: str) -> Location | None:
        """Return the Location the player will be in if they move in direction,
           or None if there's no exit in that location."""
        self._num_visits += 1
        return self._exits.get(direction)

    def to_json(self) -> dict[str, object]:
        """Return a dictionary of this object's data in a serializable format."""
        data: dict[str, object] = {}
        exits: dict[str, str] = {}
        for direction, location in self._exits.items():
            exits[direction] = location.get_name()
        data["exits"] = exits
        data["name"] = self._name
        data["description"] = self._description
        data["visits"] = self._num_visits
        data["inventory"] = self._inventory.to_json()
        return data

    def from_json(self, data: dict[str, object]) -> dict[str, str]:
        """Read field values from the json dict and return the exits
           dict to the loader for final connections."""
        exits: dict[str, str] 
        exits = data["exits"]
        self._exits = {}
        self._name = data["name"] 
        self._description = data["description"] 
        self._num_visits = data["visits"]
        self._inventory.from_json(data["inventory"])
        return exits


def main() -> None:
    """Test the Location class."""
    library: Location = Location()
    hall: Location = Location()
    study: Location = Location()

    library_inventory: Inventory = Inventory({"book": "A Python book.", "candlestick": "Could be a clue."})

    # Hard-code some values
    library._name = "Library"
    library._description = "A dangerous location."
    library._num_visits = 3
    library._inventory = library_inventory
    library._exits = {"N": hall}

    hall._name = "Hall"
    hall._description = "Linking the library and the study."
    hall._num_visits= 0
    hall._exits = {"S": library, "N": study}
    hall._inventory = Inventory()

    study._name = "Study"
    study._description = "Nobody's studying here."
    study._num_visits = 0
    study._exits = {"S": hall}
    study._inventory = Inventory()

    print("*"*80)
    print("Getting the description of each location.")
    print("Expecting:")
    print("Library\nYou see:\n\tbook\n\tcandlestick")
    print("Hall\nLinking the library and the study.")
    print("There are exits to the (S)outh and (N)orth.")
    print("Study\nNobody's studying here.\nThere is an exit to the (S)outh.")
    print("Actual:")
    print(library.get_description())
    print(hall.get_description())
    print(study.get_description())

    print("*"*80)
    print("Getting the json of each location.")
    print("Expecting:")
    print("{'exits': {'N': 'Hall'}, 'name': 'Library', 'description': 'A dangerous location.', 'num_visits': 3, ", end="")
    print("'inventory': {'book': 'A Python book.', 'candlestick': 'Could be a clue.'}},", end="")
    print("{'exits': {'S': 'Library', 'N': 'Study'}, 'name': 'Hall', 'description': 'Linking the library and the study.',", end="")
    print("'num_visits': 0, 'inventory': {}}", end="")
    print("{'exits': {'S': 'Hall'}, 'name': 'Study', 'description': \"Nobody's studying here.\", 'num_visits': 0,", end="")
    print("'inventory': {}}")
    print("Actual:")
    print(library.to_json())
    print(hall.to_json())
    print(study.to_json())

    print("*"*80)
    print("Initializing a Location from a new json and printing its description.")
    print("Expecting:")
    print("Tent\nA circus tent.\nThere are no exits. You see:\n\tballoon")
    print("Actual:")
    new_loc: Location = Location()
    new_loc.from_json({"exits": {"N":"Fairground"}, "name": "Tent", "description": "A circus tent.", "num_visits":0,
                       "inventory": {"balloon":"An abandoned balloon."}})
    print(new_loc.get_description())
      
    print("*"*80)
    print("Directly accessing the inventory of the location and examining the balloon.")
    print("Expecting:")
    print("An abandoned balloon.")
    print("Actual:")
    print(new_loc._inventory.examine("balloon"))

    print("*"*80)
    print("Testing the second pass for connecting exits.")
    print("Connecting exits for hall, which we'll create new and load from JSON, then connect exits from dict.")
    print("Expecting:")
    print("(N) Long description of study, (S) long description of library, (E) None.")
    print("Actual:")
    hall = Location()
    exits = hall.from_json({'exits': {'S': 'Library', 'N': 'Study'},
                           'name': 'Hall', 'description': 'Linking the library and the study.',
                            'num_visits': 0, 'inventory': {}})
    locations_inv = {"Hall": hall, "Library": library, "Study": study}
    for direction, location_name in exits.items():
        hall.add_exit(direction, locations_inv[location_name])
    print("Moving north from the reconsistituted hall:")
    print(hall.go("N").get_long_description())
    print("Moving south from the reconsistuted hall:")
    print(hall.go("S").get_long_description())
    print("Moving east from the reconsistuted hall:")
    print(hall.go("E"))

if __name__ == "__main__":
    main()

