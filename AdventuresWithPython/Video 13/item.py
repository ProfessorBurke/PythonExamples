

class Item:
    """
        Description

        Attributes:
            _name: str
            _description: str
            _action: str
            _object: str
    """

    def __init__(self) -> None:
        """Set the name and decription fields from parameters."""
        self._name = None
        self._description = None
        self._action = None
        self._object = None

    def get_name(self) -> str:
        """Return this item's name."""
        return self._name

    def get_description(self) -> str:
        """Return this item's description."""
        return self._description

    def use(self) -> dict[str, str]:
        """Return the action and password."""
        return {"action": self._action, "object": self._object}

    def to_json(self) -> dict[str, str]:
        """Convert data to a serializable form."""
        return {"name": self._name, "description": self._description,
                "object": self._object, "action": self._action}

    def from_json(self, data: str) -> None:
        """Restore fields from serialized data."""
        self._name = data["name"]
        self._description = data["description"]
        self._object = data["object"]
        self._action = data["action"]
    
