from enum import Enum

# Words to remove from the command.
FILLER_WORDS = frozenset({"THE", "A", "AN", "AT", "TO", "WITH", "IN", "ON", "OF", "MY"})

# Acceptable direction words and their mapping to the direction word used in the game.
DIRECTION_LOOKUP = {"NORTH": "N",
                    "N": "N",
                    "SOUTH": "S",
                    "S": "S",
                    "EAST": "E",
                    "E" : "E",
                    "WEST": "W",
                    "W": "W"}

class CommandType(Enum):
    """
        Represents the different kinds of player commands in the text-adventure game.

        Each enum member stores a set of strings containing the valid words or
        abbreviations that map to that command. The `from_word` method performs
        a case-insensitive lookup by checking which command's set contains the
        given word.

        Members:
            MOVE:       Commands for movement, not including directions which are objects.
            LOOK:       Commands for examining the current room or surroundings.
            TAKE:       Commands for picking up an item.
            DROP:       Commands for dropping or placing an item.
            SAVE:       Commands for saving the current game state.
            RESTORE:    Commands for loading a previously saved game.
            INVENTORY:  Commands for listing items currently carried.
            EXAMINE:    Commands for inspecting a specific item.
            USE:        Commands for using an item.
            QUIT:       Commands for exiting the game.
            UNKNOWN:    Fallback used when a word does not match any known command.
    """
    MOVE = frozenset({"GO", "MOVE", "WALK", "RUN", "EXIT"})
    LOOK = frozenset({"L", "LOOK"})
    TAKE = frozenset({"T", "TAKE", "GET"})
    DROP = frozenset({"D", "DROP", "PUT"})
    SAVE = frozenset({"V", "SAVE"})
    RESTORE = frozenset({"R", "RESTORE"})
    INVENTORY = frozenset({"I", "INVENTORY"})
    EXAMINE = frozenset({"X", "EXAMINE"})
    USE = frozenset({"U", "USE"})
    QUIT = frozenset({"Q", "QUIT"})
    UNKNOWN = frozenset()

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
        result: "CommandType" = CommandType.UNKNOWN
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
            _type: CommandType   The type of this command
            _object: str | None  The object of the command
    """
    def __init__(self, text: str):
        """Parse the player's raw text into a CommandType and object."""
        # Tokenize, removing filler words.
        raw = text.strip()
        words = self._tokenize(raw)

        # Set command type to unknown and object to None if there are no words left.
        if not words:
            self._type = CommandType.UNKNOWN
            self._object = None
        # Otherwise parse the command into a command type and object (or None).
        else:
            command, self._object = self._parse_command(words)
            self._type = CommandType.from_word(command)

    def _tokenize(self, text: str) -> list[str]:
        """Convert text to a list of strings using white space as
           a delimiter, removing filler words."""
        return [t for t in text.split() if t.upper() not in FILLER_WORDS]

    def _parse_command(self, tokens: list[str]) -> tuple[str, str]:
        """Parse the tokenized, non-empty command list into a command string
           and an object string or None."""
        command_word: str = ""
        object_: str = None
        verb: str = tokens[0].upper()
        
        # The player has typed a direction only, so return (MOVE, direction from lookup table)
        if verb in DIRECTION_LOOKUP:
            object_ = DIRECTION_LOOKUP.get(verb)
            verb = "MOVE"
        # The player has typed a move command and possibly a direction, so return the move
        # command and the correct direction from the lookup table or None if the word
        # isn't in the directions lookup or if there isn't a second word
        elif verb in CommandType.MOVE.value:
            if len(tokens) > 1:
                object_ = DIRECTION_LOOKUP.get(tokens[1].upper())
        # The player has typed a command and object
        elif len(tokens) > 1:
            object_ = " ".join(tokens[1:])

        return (verb, object_)

    def is_type(self, type_: CommandType) -> bool:
        """Returns True if the passed type matches this object's command type."""
        return self._type is type_

    def get_object(self) -> "str | None":
        """Returns the object string or None."""
        return self._object



def test_parser():
    print("Command Parser Test Harness")
    print("Type commands to see how they are parsed.")
    print("Type 'nope' to exit the harness.")
    print()

    raw: str = input("> ")
    while not raw.lower().strip() == "nope":
       
        cmd = Command(raw)

        print(f" Raw Input:      {raw!r}")
        print(f" CommandType:    {cmd._type}")
        print(f" Object Parsed:  {cmd.get_object()!r}")
        print("-" * 40)
        
        raw = input("> ")


if __name__ == "__main__":
    test_parser()
