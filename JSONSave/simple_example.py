# Import the json library for saving characters.
import json

class Character():
    """
         A simple character with a name and some stats.
    """
    # Annotate object-level fields.
    _name: str
    _charisma: int
    _strength: int

    def __init__(self, name: str, charisma: int, strength: int) -> None:
        """Initialize fields from parameters."""
        super().__init__()
        self._name = name
        self._charisma = charisma
        self._strength = strength

    def to_json(self):
        """Convert data to a dictionary and then to JSON.
           Return the JSON."""
        return json.dumps({
            'name': self._name,
            'charisma': self._charisma,
            'strength': self._strength
        })

    @staticmethod
    def from_json(json_str: str) -> "Character":
        """Create and return a Character object from the
           json_str passed as a parameter."""
        character_dict: dict = json.loads(json_str)
        return Character(character_dict["name"],
                         character_dict["charisma"],
                         character_dict["strength"])

    def __str__(self) -> str:
        """Create a string version of the object meant for
           printing to the console."""
        return "{:10s}{}\n{:10s}{}\n{:10s}{}\n".format(
            "Name:", self._name,
            "Charisma:", self._charisma,
            "Strength:", self._strength)

    
def create_character() -> Character:
    """Obtain character stats from the user and then
       instantiate and return a Character object."""
    name: str = input("What is your character's name? ")
    charisma: int = int(input("What is your character's charisma? "))
    strength: int = int(input("What is your character's strength? "))
    return Character(name, charisma, strength)

def main() -> None:
    """Create a character, save it to a file, load it
       back in."""

    # Create and print a character.
    character_write: Character = create_character()
    print("You just created the following character: ")
    print(character_write)

    # Get a JSON version of the character and save it to a file.
    with open("character.json", "w") as f:
        f.write(character_write.to_json())

    # Load the character file in.
    with open("character.json", "r") as f:
        character_read: Character = Character.from_json(f.read())

    print("I just read this character from the file character.json:")
    print(character_read)


if __name__ == "__main__":
    main()
