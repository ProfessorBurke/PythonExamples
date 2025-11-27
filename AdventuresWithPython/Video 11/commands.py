from enum import Enum

class CommandType(Enum):
    MOVE = {"N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"}
    TAKE = {"T", "TAKE"}
    LOOK = {"L", "LOOK"}
    DROP = {"D", "DROP"}
    SAVE = {"V", "SAVE"}
    RESTORE = {"R", "RESTORE"}
    INVENTORY = {"I", "INVENTORY"}
    EXAMINE = {"X", "EXAMINE"}
    QUIT = {"Q", "QUIT"}
    UNKNOWN = set()

    @classmethod
    def from_words(cls, word: str) -> "CommandType":
        result: "CommandType" = CommandType.UNKNOWN
        command_type: "CommandType"
        word = word.upper()
        for command_type in cls:
            if word in command_type.value:
                result = command_type
        return result

class Command:
    """
        Represents a command typed by the player.
        Can confirm the CommandType and return the object.

        Attributes:
            _type: CommandType  The type of this command
            _object: str | None The object of this command
    """

    def __init__(self, text: str) -> None:
        raw: str = text.strip()
        words: list[str] = raw.split()

        if not words:
            self._type = CommandType.UNKNOWN
            self._object = None
        else:
            self._type = CommandType.from_words(words[0])
            if self._type is CommandType.MOVE:
                self._object = words[0].upper()[0]
            else:
                self._object = " ".join(words[1:]) if len(words)>1 else None

    def is_type(self, command_type: CommandType) -> bool:
        return self._type is command_type

    def get_object(self) -> "str|None":
        return self._object




    
