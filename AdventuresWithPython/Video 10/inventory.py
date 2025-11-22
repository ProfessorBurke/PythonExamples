
class Inventory:
    """
    Represents an inventory that can hold items.

    Attributes:
        _items (dict[str, str]): The inventory items.

    """

    def __init__(self, items: dict[str, str] | None = None) -> None:
        """Copy the field _items from the parameter, or {} if
           no parameter is passed."""
        self._items = {} if items is None else dict(items)

    def add(self, item_name: str, item_description: str) -> None:
        """Add the item to the Inventory."""
        self._items[item_name] = item_description

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
            description = self._items[item_name]
        return description

    def exchange_item(self, item_name: str, other_inventory: "Inventory")-> bool:
        """Give item_name to  other_inventory.  If successful, return True."""
        success: bool = False
        value: str
        if item_name in self._items:
            value = self._items.pop(item_name)
            other_inventory.add(item_name, value)
            success = True
        return success

    def is_empty(self) -> bool:
        """Return True if the Inventory is empty; False otherwise."""
        return len(self._items) == 0

    def to_json(self) -> dict[str, str]:
        return self._items

    def from_json(self, json: dict[str, str]) -> None:
        self._items = json
    
    def __contains__(self, item_name: str)-> bool:
        """Returns true if item_name is a key in the _items dict."""
        return item_name in self._items

    def __str__(self) -> str:
        """Return a string representation of the Inventory."""
        return "\t"+ "\n\t".join(self._items)



def main() -> None:
    """Test the Inventory class."""
    # Annotate two Inventory variables.
    inv1: Inventory
    inv2: Inventory
    
    # Constructor with argument
    inv1 = Inventory({"book": "An ancient book", "knife": "A nasty knife",
                     "nest": "The result of some avian hard work"})
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
    inv1.add("egg", "A jewel-encrusted egg")
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
    print("Expected: {'knife': 'A nasty knife', 'nest': 'The result of some avian hard work'}")
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
    inv3: Inventory = Inventory({"one": "thing one", "two": "thing two"})
    inv3.from_json({'knife': 'A nasty knife', 'nest': 'The result of some avian hard work'})
    print(inv3)

    print("*"*80)
    print("Reading an empty json into an inventory that already had items.")
    print("Expected: nothing")
    print("Actual:")
    inv3.from_json({})
    print(inv3)

if __name__ == "__main__":
    main()
