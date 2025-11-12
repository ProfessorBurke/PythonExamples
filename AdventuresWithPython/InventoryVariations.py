
class Inventory:
    """
    Represents an inventory that can hold items.

    Attributes:
        _items (dict[str, str]): The inventory items.
        _locked (bool): Whether the inventory is locked.
        _key (str): the key to unlock the inventory
        _max_items (int): The maximum number of items the inventory can hold.

    """

    def __init__(self, max_items: int, items: dict[str, str] | None = None) -> None:
        """Copy the field _items from the parameter, or {} if
           no parameter is passed."""
        self._items = {} if items is None else dict(items)
        self._locked = False
        self._key = None
        self._max_items = max_items

    def add(self, item_name: str, item_description: str) -> bool:
        """Add the item to the Inventory."""
        result: bool = False
        if not self._locked:
            if len(self._items) < self._max_items:
                self._items[item_name] = item_description
                result = True
        return result

    def remove(self, item_name: str) -> bool:
        """Remove the item from the Inventory and return True if successful."""
        success: bool = False
        if not self._locked:
            if item_name in self._items:
                self._items.pop(item_name)
                success = True
        return success

    def examine(self, item_name: str) -> str:
        """Return the value description for the item."""
        description: str = ""
        if not self._locked:
            if item_name in self._items:
                description = self._items[item_name]
        else:
            description = "A blur."
        return description

    def exchange_item(self, item_name: str, other_inventory: "Inventory")-> bool:
        """Give item_name to  other_inventory.  If successful, return True."""
        success: bool = False
        value: str
        if not self._locked and not other_inventory.is_locked:
            if item_name in self._items:
                value = self._items.pop(item_name)
                # If we can add to the other inventory, do so.
                if other_inventory.add(item_name, value)
                    success = True
                # Otherwise, put the item back here.
                else:
                    self._items[item_name] = value
        return success

    def is_empty(self) -> bool:
        """Return True if the Inventory is empty; False otherwise."""
        result: bool = False
        if not self._locked:
            result = len(self._items) == 0
        return result

    def lock(self, key: str) -> None:
        """Lock the inventory."""
        self._locked = True
        self._key = key

    def unlock(self, key: str) -> bool:
        """Unlock the inventory if the key is correct."""
        result: bool = False
        if key == self._key:
            self._locked = False
            result = True
        return result

    def is_locked(self) -> bool:
        """Return True if the Inventory is locked; False otherwise."""
        return self._locked

    def to_json(self) -> dict[str, str]:
        return {"items": self._items, "locked": self._locked,
                "key": self._key, "max_items": self._max_items}

    def from_json(self, json: dict[str, str]) -> None:
        self._items = json["items"]
        self._locked = json["locked"]
        self._key = json["key"]
        self._max_items = json["max_items"]
    
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
