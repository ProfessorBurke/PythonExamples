from enum import Enum

class CommandType(Enum):
    """
        Represents the different kinds of player commands in the text-adventure game.

        Each enum member stores a set of strings containing the valid words or
        abbreviations that map to that command. The `from_word` method performs
        a case-insensitive lookup by checking which command's set contains the
        given word.

        Members:
            MOVE:       Movement commands such as "GO", compass directions, and abbreviations.
            LOOK:       Commands for examining the current room or surroundings.
            TAKE:       Commands for picking up an item.
            DROP:       Commands for dropping or placing an item.
            SAVE:       Commands for saving the current game state.
            RESTORE:    Commands for loading a previously saved game.
            INVENTORY:  Commands for listing items currently carried.
            EXAMINE:    Commands for inspecting a specific object.
            QUIT:       Commands for exiting the game.
            UNKNOWN:    Fallback used when a word does not match any known command.
    """
    MOVE = {"N", "NORTH", "S", "SOUTH", "E", "EAST", "W", "WEST"}
    LOOK = {"L", "LOOK"}
    TAKE = {"T", "TAKE"}
    DROP = {"D", "DROP"}
    SAVE = {"V", "SAVE"}
    RESTORE = {"R", "RESTORE"}
    INVENTORY = {"I", "INVENTORY"}
    EXAMINE = {"X", "EXAMINE"}
    QUIT = {"Q", "QUIT"}
    UNKNOWN = set()

    @classmethod
    def from_word(cls, word: str) -> "CommandType":
        """
        Returns the CommandType corresponding to the given word.

        The lookup is case-insensitive and checks whether the uppercase version
        of the word appears in any member's set of accepted command strings.

        Parameters:
            word (str): The player's input word to interpret.

        Returns:
            CommandType: The matching command type, or CommandType.UNKNOWN if no match is found.
        """
        result: "CommandType" = cls.UNKNOWN
        command_type: "CommandType"
        word = word.upper()
        for command_type in cls:
            if word in command_type.value:
                result = command_type
        return result


class Command:
    """
        Represents a command typed by the player.
        Parses the command and can return different command components.

        Attributes:
            _raw: str            The original command text
            _words: list[str]    A list of command words
            _type: CommandType   The type of this command
            _object: str | None  The object of the command
    """
        
        
    def __init__(self, text: str):
        """Initialize fields from the raw text typed by the player."""
        # Strip white space and split into individual words.
        self._raw = text.strip()
        self._words = self._raw.split()

        # If there was no command, set _type and _object appropriately.
        if not self._words:
            self._type = CommandType.UNKNOWN
            self._object = None
        # If there was a command, extract type and object.
        else:
            # The first word identifies the command type.
            self._type = CommandType.from_word(self._words[0])

            # If it's a move command, at present, that's also the object.
            if self._type is CommandType.MOVE:
                self._object = self._words[0].upper()[0]

            # If it's not move, the rest is the object (or no object).
            else:
                self._object = " ".join(self._words[1:]) if len(self._words) > 1 else None

    def is_type(self, command_type: CommandType) -> bool:
        """Return true if the passed type is this command's type; False otherwise."""
        return self._type is command_type

    def get_object(self) -> "str | None":
        """Return the object of the command."""
        return self._object


