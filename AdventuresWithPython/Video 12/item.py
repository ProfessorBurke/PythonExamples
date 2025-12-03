
class Item:
    """
        Description

        Attributes:
            _name: str
            _description: str
    """

    def __init__(self) -> None:
        """Set the name and decription fields from parameters."""
        self._name = None
        self._description = None

    def get_name(self) -> str:
        """Return this item's name."""
        return self._name

    def get_description(self) -> str:
        """Return this item's description."""
        return self._description

    def to_json(self) -> str:
        """Convert data to a serializable form."""
        return {"name": self._name, "description": self._description}

    def from_json(self, json: str) -> None:
        """Restore fields from serialized data."""
        self._name = json["name"]
        self._description = json["description"]
    
