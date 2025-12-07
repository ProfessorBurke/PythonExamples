from item import Item

class Inventory:
    """
        Represents an inventory that can hold items.

        Attributes:
            _items (dict[str, Item]): The inventory items.

    """

    def __init__(self) -> None:
        """Copy the field _items from the parameter, or {} if
           no parameter is passed."""
        self._items = {} 

    def add(self, item_name: str, item: Item) -> bool:
        """Add the item to the Inventory.  The Boolean result is leaving
           space for eventually having a size (or other) limit on the inventory."""
        self._items[item_name] = item
        return True

    def remove(self, item_name: str) -> bool:
        """Remove the item from the Inventory and return True if successful."""
        success: bool = False
        if item_name in self._items:
            self._items.pop(item_name)
            success = True
        return success

    def examine(self, item_name: str) -> str:
        """Return the value description for the item."""
        description: str = ""
        if item_name in self._items:
            description = self._items[item_name].get_description()
        return description

    def exchange_item(self, item_name: str, other_inventory: "Inventory")-> bool:
        """Give item_name to  other_inventory.  If successful, return True."""
        success: bool = False
        value: Item
        if item_name in self._items:
            value = self._items.pop(item_name)
            other_inventory.add(item_name, value)
            success = True
        return success

    def get_item(self, item_name: str) -> "Item | None":
        """Return the item."""
        return self._items.get(item_name)

    def is_empty(self) -> bool:
        """Return True if the Inventory is empty; False otherwise."""
        return len(self._items) == 0

    def to_json(self) -> dict[str, str]:
        """Convert the _items dictionary of name, Item pairs to
           a dictionary of name, serialized item pairs."""
        json: dict[str, str] = {}
        for name, value in self._items.items():
            json[name] = value.to_json()
        return json

    def from_json(self, json: dict[str, str]) -> None:
        """The json of an inventory is a dictionary of name-Item pairs."""
        self._items = {}
        for name, value in json.items():
            item: Item = Item()
            item.from_json(value)
            self._items[name] = item
    
    def __contains__(self, item_name: str)-> bool:
        """Returns true if item_name is a key in the _items dict."""
        return item_name in self._items

    def __str__(self) -> str:
        """Return a string representation of the Inventory."""
        return "\t"+ "\n\t".join(self._items)



def main() -> None:
    """Test the Inventory class."""
    # Note -- no new tests have been added since Item was enhanced and exits
    # got behavior.  Just got it running so it won't crash.
    # Annotate two Inventory variables.
    inv1: Inventory
    inv2: Inventory

    # Construct an inventory and read it from json
    inv1 = Inventory()
    inv1.from_json({"book": {"name": "book", "description": "a book", "action":"", "object":""},
                    "knife": {"name": "knife", "description": "a nasty knife", "action":"", "object":""},
                    "nest": {"name": "nest", "description": "some avian hard work", "action":"", "object":""}})
    
    # Default value for constructor argument
    inv2 = Inventory()
    

    print("*"*80)
    print("Printing an inventory.")
    print("Expecting book, knife, and nest, indented.")
    print("Actual: ")
    print(inv1)

    print("*"*80)
    print("Checking is_empty on a non-empty inventory.")
    print("Expecting: False")
    print("Actual:    ", end="")
    print(inv1.is_empty())

    print("*"*80)
    print("Checking is_empty on an empty inventory.")
    print("Expecting: True")
    print("Actual:    ", end="")
    print(inv2.is_empty())

    print("*"*80)
    print("Adding an egg to the same inventory and printing.")
    print("Expected: book, knife, nest, and egg, indented.")
    print("Actual: ")
    item: Item = Item()
    item.from_json({"name": "egg", "description": "A jewel-encrusted egg", "action":"", "object":""})
    inv1.add("egg", item)
    print(inv1)

    print("*"*80)
    print("Exchanging book with an empty inventory and printing the outcome.")
    print("Expected: True")
    print("Actual:   ", end="")
    print(inv1.exchange_item("book", inv2))

    print("*"*80)
    print("Printing the recipient inventory.")
    print("Expected: book")
    print("Actual: ")
    print(inv2)

    print("*"*80)
    print("Exchanging necklace with the other inventory and printing the outcome.")
    print("Expected: False")
    print("Actual:   ", end="")
    print(inv1.exchange_item("necklace", inv2))

    print("*"*80)
    print("Printing the recipient inventory.")
    print("Expected: book")
    print("Actual: ")
    print(inv2)

    print("*"*80)
    print("Testing book in inventory.")
    print("Expected: False")
    print("Actual:   ", end="")
    print("book" in inv1)

    print("*"*80)
    print("Testing egg in inventory.")
    print("Expected: True")
    print("Actual:   ", end="")
    print("egg" in inv1)

    print("*"*80)
    print("Printing an inventory.")
    print("Expected: knife, nest, and egg, indented.")
    print("Actual: ")
    print(inv1)
    print(inv1._items)

    print("*"*80)
    print("Examining an item.")
    print("Expected: A jewel-encrusted egg")
    print("Actual:   ", end="")
    print(inv1.examine("egg"))

    print("*"*80)
    print("Examining a nonexistent item.")
    print("Expected: ")
    print("Actual:   ", end="")
    print(inv1.examine("eggo"))

    print("*"*80)
    print("Removing an item.")
    print("Expected: True")
    print("Actual:   ", end="")
    print(inv1.remove("egg"))

    print("*"*80)
    print("Removing a nonexistent item.")
    print("Expected: False")
    print("Actual:   ", end="")
    print(inv1.remove("egg"))

    print("*"*80)
    print("Creating a json from an inventory with items.")
    print("Expected: {'knife': {'name': 'knife', 'description': 'a nasty knife'}, 'nest': {'name': 'nest', 'description': 'some avian hard work'}}")
    print("Actual:   ", end="")
    print(inv1.to_json())

    print("*"*80)
    print("Creating a json from an empty inventory.")
    print("Expected: {}")
    print("Actual:   ", end="")
    print(Inventory().to_json())

    print("*"*80)
    print("Reading a json with items into an inventory that already had items.")
    print("Expected: knife and nest, indented.")
    print("Actual:")
    inv3: Inventory = Inventory()
    inv2.from_json({"one": {"name":"one", "description":"thing one", "action":"", "object":""},
                    "two":{"name":"two", "description":"thing two", "action":"", "object":""}})
    inv3.from_json({"knife":{"name": 'knife', "description": 'A nasty knife', "action":"", "object":""},
                    "nest":{"name":'nest', "description": 'The result of some avian hard work', "action":"", "object":""}})
    print(inv3)

    print("*"*80)
    print("Reading an empty json into an inventory that already had items.")
    print("Expected: nothing")
    print("Actual:")
    inv3.from_json({})
    print(inv3)

if __name__ == "__main__":
    main()
