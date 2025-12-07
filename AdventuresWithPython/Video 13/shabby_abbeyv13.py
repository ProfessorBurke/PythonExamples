"""
    Shabby Abbey v13
    Obtain a command from the player and respond to it until
    the user chooses to quit.
    This is a fully object-oriented version of the system with
    items that can act on exits.
    Maggie
    12/04/2025
"""

from inventory import Inventory
from location import Location
from item import Item
from loader import Loader
from commands import Command, CommandType

class Game:
    """
        A text adventure game that obtains commands from the user and follows
        them to allow the user to move around a dungeon and take, drop, and
        examine items.

        Attributes:
        _player_inventory: Inventory
        _current_location: Location
        _locations_lookup: dict[str, Location]
        _loader: Loader
    """

    def __init__(self) -> None:
        """Create the loader, read in the dungeon.
           The data returned from the loader consists of:
           current location, player inventory, 
           and the locations lookup table."""
        self._loader = Loader()
        save_data: dict[str, object] = self._loader.load_abbey(Loader.START)
        self._locations_lookup = save_data["location_lookup"]
        self._current_location = save_data["current_location"]
        self._player_inventory = save_data["player_inventory"]

    def _handle_save(self) -> "str | None":
        """The player has chosen to save the dungeon. Return
           an appropriate message."""
        response: "str | None" = None
        # Create the save data dictionary and send it to the loader for saving.
        save_data: dict[str, object] = {}
        save_data["current_location"] = self._current_location
        save_data["location_lookup"] = self._locations_lookup
        save_data["player_inventory"] = self._player_inventory
        # Save it.
        if self._loader.save_abbey(save_data):
           response = "Saved."
        else:
           response = "There was a problem saving."
        return response

    def _handle_restore(self) -> "str | None":
        """The player has chosen to restore the dungeon.  Return
           an appropriate message."""
        response: "str | None" = None
        # Load the dictionary of data and save it in appropriate variables.
        save_data: dict[str, object] = self._loader.load_abbey(Loader.SAVE)
        self._locations_lookup = save_data["location_lookup"]
        self._current_location = save_data["current_location"]
        self._player_inventory = save_data["player_inventory"]
        return response
    
    def _inventory_swap(self, from_inventory: Inventory, to_inventory: Inventory,
                       item: str, action: str) -> str:
        """Remove the item from the from_inventory and place in the to_inventory,
           if it is in the from_inventory.  Print an appropriate message if not."""
        response: str
        # Attempt to exchange the item.
        if from_inventory.exchange_item(item, to_inventory):
            response = item + " has been " + action + "."
        # If the item was not successfully exchanged.
        else:
            response = "I don't see " + item + "."
        return response

    def _handle_take(self, command: Command) -> "str | None":
        """The player has chosen to take an item. Return
           an appropriate message."""
        response: "str | None" = None
        item: str = command.get_object()
        if item is None:
            response = "You must take something."
        else:
            response = self._inventory_swap(self._current_location.get_inventory(),
                                            self._player_inventory, item, "taken")
        return response

    def _handle_drop(self, command: Command) -> "str | None":
        """The player has chosen to drop an item.  Return
           an appropriate message."""
        response: "str | None" = None
        item: str = command.get_object()
        if item is None:
            response = "You must drop something."
        else:
            response = self._inventory_swap(self._player_inventory,
                                            self._current_location.get_inventory(),
                                            item, "dropped")
        return response

    def _handle_inventory(self) -> "str | None":
        """The player has chosen to list their inventory. Return
           the inventory or a message indicating they have nothing."""
        response: "str | None" = None
        if self._player_inventory.is_empty():
            response = "You aren't carrying anything."
        else:
            response = "You have:\n" + str(self._player_inventory)
        return response

    def _handle_move(self, command: Command) -> "str | None":
        """The player has chosen to exit the current location. Change the
           current location if a valid exit."""
        direction: str
        response: "str | None" = None
        direction = command.get_object()
        next_location_name: str
        next_location: Location
        next_location_name = self._current_location.go(direction)
        next_location = self._locations_lookup.get(next_location_name)
        if next_location is None:
            response = "You can't exit in that direction."
        else:
            self._current_location = next_location
        return response

    def _handle_examine(self, command: Command) -> "str | None":
        """The player has chosen to examine something.  Return
           a description of the thing or an appropriate message."""
        response: "str | None" = None
        item: "str | None" = command.get_object()
        if item is None:
            response = "You must examine something."
        else:
            if item in self._player_inventory:
               response = self._player_inventory.examine(item)
            else:
               response = "You don't have "
               response += "an " if item.lower()[0] in ["a", "e", "i", "o", "u"] else "a "
               response += item + "."
        return response

    def _handle_look(self) -> "str | None":
        """The player has chosen to look at the current location.  Return
           a description of the current location."""
        response: "str | None" = None
        response = self._current_location.get_long_description()
        return response

    def _handle_use(self, command: Command) -> "str | None":
        """The player has chosen to use an item.  Let them try."""
        response: "str | None" = None
        item_name: "str | None" = command.get_object()
        if item_name is None:
            response = "You must use something in your inventory."
        else:
            if item_name in self._player_inventory:
                item: Item = self._player_inventory.get_item(item_name)
                response = self._current_location.use_item(item)
            else:
                response = "You don't have "
                response += "an " if item_name.lower()[0] in ["a", "e", "i", "o", "u"] else "a "
                response += item_name + "."
        return response
       
        
    def play(self) -> None:
        """Obtain and process commands from the player until they choose to quit."""
        
        # Annotate variables.
        user_input: str = ""
        command: Command = Command("UNKNOWN")
        response: "str | None" = None
        
        item: str

        # Greet the player.
        print("Welcome, Adventurer!")

        while not command.is_type(CommandType.QUIT):
            # Describe the current location.
            print(self._current_location.get_description())

            # Obtain the player's input and instantiate a command.
            user_input = input("What is your command? ")
            command = Command(user_input)

            # Move the player if a direction command.
            if command.is_type(CommandType.MOVE):
                response = self._handle_move(command)

            # Handle save and restore.
            elif command.is_type(CommandType.SAVE):
                response = self._handle_save()
            elif command.is_type(CommandType.RESTORE):
                response = self._handle_restore()
                
            # Handle a look command.
            elif command.is_type(CommandType.LOOK):
                response = self._handle_look()
                
            # Handle inventory commands.
            elif command.is_type(CommandType.TAKE):
                response = self._handle_take(command)
                
            elif command.is_type(CommandType.DROP):
                response = self._handle_drop(command)
                
            elif command.is_type(CommandType.INVENTORY):
                response = self._handle_inventory()
                
            elif command.is_type(CommandType.EXAMINE):
                response= self._handle_examine(command)

            # Handle a use command.
            elif command.is_type(CommandType.USE):
                response = self._handle_use(command)
                        
            # Handle an unrecognizable command.
            elif command.is_type(CommandType.UNKNOWN):
                response = "I didn't understand that command."

            # Display feedback from the command, if any, and reset the response variable.
            if response:
                print(response)
                response = None

        print("Thank you for playing.")

def main() -> None:
    """Create a Game object and send it the play message."""
    Game().play()

if __name__ == "__main__":
    main()
