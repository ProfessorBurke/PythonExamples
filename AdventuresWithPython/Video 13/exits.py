
class Exit:
    """
        Description

        Attributes:
            _name: str
            _location: str
            _description: str
            _state_descriptions: dict[str, str]
            _state: list[str]
            _state_changes: list[dict]
    """

    def __init__(self) -> None:
        """Set the name and decription fields from parameters."""
        self._name = ""
        self._description = ""
        self._state_descriptions = {}
        self._location = None
        self._state = []
        self._state_changes = []
        self._dysfunctional_states = []

    def get_name(self) -> str:
        """Return this exit's name."""
        return self._name

    def get_description(self) -> str:
        """Return this item's description, which is the base
           description, plus possible state information layered
           on top.
           self._state is a list of ExitState enum values
           self._state_descriptions is a dictionary of 
              ExitState,str pairs
           So if self._state is [ExitState.LOCKED, ExitState.UNBLOCKED],
           this will find the descriptions for those two states in
           self._state_descriptions and append them to the description.
        """
        description: str = self._description + "\n"
        # Some states don't require any description and don't have any.
        # Include only additional description for states for which there is some.
        for state in self._state:
            if self._state_descriptions.get(state):
                description +=  self._state_descriptions[state] + "\n"
        return description

    def get_location(self) -> "str | None":
        """Return the Location that this exit leads to, or
           None if the exit is unpassable."""
        return self._location if not self.is_impassable() else None

    def use_item(self, action: str) -> str:
        """Transform the state of the object, if the action is
           one that is part of this object, and this object is in the correct
           state for transformation.
           Return the appropriate success or failure message.
           
           _state_changes is structured as a dictionary of:
           action : {"state": str,
                     "success_str": str,
                     "fail_str": str}
        """
        result: str = ""
        # Get the specific action dictionary for this action
        action_data: dict = self._state_changes.get(action)
        # If this exit has an action dictionary for this action
        if not action_data is None:
            # If this exit is not in the correct state for action,
            # set the result string accordingly.
            if not (action_data["state"] in self._state):
                result = action_data["fail_str"]
                
            # Otherwise, state matches, transform.
            else:
                self._state.remove(action_data["state"])
                result = action_data["success_str"]
        # If there's no state change for this action.
        else:
            result = "You can't use that here."
        return result

    def is_impassable(self) -> bool:
        """Return True if this exit is impassable and False otherwise."""
        impassable: bool = False
        i: int = 0
        while i < len(self._state) and not impassable:
            if self._state[i] in self._dysfunctional_states:
                impassable = True
            i += 1
        return impassable

    def to_json(self) -> dict:
        """Convert data to a serializable form."""
        json: dict = {}
        json["name"] = self._name
        json["location"] = self._location
        json["description"] = self._description
        json["state_descriptions"] = self._state_descriptions
        json["state"] = self._state
        json["state_changes"] = self._state_changes
        json["dysfunctional_states"] = self._dysfunctional_states
        return json

    def from_json(self, json: str) -> None:
        """Restore fields from serialized data."""
        self._name = json["name"]
        self._description = json["description"]
        self._location = json["location"]
        self._state_descriptions = json["state_descriptions"]
        self._state = json["state"]
        self._state_changes = json["state_changes"]
        self._dysfunctional_states = json["dysfunctional_states"]




def main() -> None:
    north_exit_json: dict = {"name": "cloistertochurchdoor",
                             "location": "church",
                             "description": "A sturdy-looking door with a diamond-shaped stained glass window.",
                             "state_descriptions":
                                {"locked": "The door appears to be locked.",
                                 "blocked": "There is a pile of rubble in front of the door."},
                             "state": ["locked", "blocked"],
                             "dysfunctional_states": ["locked", "blocked"],
                             "state_changes": {
                                "unlock" : {"state": "locked",
                                            "success_str": "There is a click and the door swings open.",
                                            "fail_str": "The door isn't locked"},
                                "unblock" : {"state": "blocked",
                                             "success_str": "You've cleared the rubble from the front of the door.",
                                             "fail_str": "This door isn't blocked."}}}

    # Create an exit from json.
    north_exit: Exit = Exit()

    print("\n" + "*"*80)
    print("Creating an exit from JSON and printing the location field.")
    print("Expecting church")
    north_exit.from_json(north_exit_json)
    print("Actual: " + north_exit._location)

    print("\n" + "*"*80)
    print("Printing the _state_changes field.")
    print("Expecting (look at hard-coded json)")
    print("Actual: ")
    print(north_exit._state_changes)

    print("\n" + "*"*80)
    print("Printing the _state field.")
    print("Expecting ['locked', 'blocked']")
    print("Actual: ")
    print(north_exit._state)

    print("\n" + "*"*80)
    print("Printing exit's description.")
    print("Expecting A sturdy-looking door with a diamond-shaped stained glass window.")
    print("Actual: " + north_exit._description)

    print("\n" + "*"*80)
    print("Sending exit get_description() and printing.")
    print("Expecting:")
    print("A sturdy-looking door with a diamond-shaped stained glass window.")
    print("The door appears to be locked.")
    print("There is a pile of rubble in front of the door.")
    print("Actual: ")
    print(north_exit.get_description())

    print("\n" + "*"*80)
    print("Attempting to lock a locked door. Printing message and description.")
    print("Expecting:")
    print("You can't use that here.")
    print("A sturdy-looking door with a diamond-shaped stained glass window.")
    print("The door appears to be locked.")
    print("There is a pile of rubble in front of the door.")
    print("Actual: ")
    print(north_exit.use_item("lock"))
    print(north_exit.get_description())

    print("\n" + "*"*80)
    print("Send the exit the to_json message; print.")
    print("Expecting: (look at hard-coded json)")
    print("Actual: ")
    print(north_exit.to_json())
    
    print("\n" + "*"*80)
    print("Attempting to unlock a locked door . Printing message and description.")
    print("Expecting:")
    print("There is a click and the door swings open.")
    print("A sturdy-looking door with a diamond-shaped stained glass window.")
    print("There is a pile of rubble in front of the door.")
    print("Actual: ")
    print(north_exit.use_item("unlock"))
    print(north_exit.get_description())

    print("\n" + "*"*80)
    print("Send the exit the to_json message; print.")
    print("Expecting: (look at hard-coded json, but state should not include locked.)")
    print("Actual: ")
    print(north_exit.to_json())




if __name__ == "__main__":
    main()






