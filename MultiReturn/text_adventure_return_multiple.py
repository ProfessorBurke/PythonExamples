"""
    A simple text adventure.
    
"""

def print_field_description():
    """Describe the field, including the directions that can be moved."""
    print("You are standing in a field of long grass dotted with wildflowers.")
    print("To the (N)orth, you see what looks like an abandoned settlement.")
    print("To the (E)ast, you see a forest.")
    print("To the (S)outh is a fast-flowing river.  It looks dangerous.")
    print("To the (W)est is an unscalable cliff face.")

def print_wood_description():
    """Describe the woods, including the directions that can be moved."""
    print("You are in a quiet, dense wood with no discernible path.")
    print("To the (N)orth, you see what looks like an abandoned settlement.")
    print("To the (E)ast, you see more forest.")
    print("To the (S)outh is a fast-flowing river.  It looks dangerous.")
    print("To the (W)est is a field.")

def print_settlement_description():
    """Describe the settlement, including the directions that can be moved."""
    print("This appears to be an abandoned settlement.  You are standing in what appears to have been the town square.")
    print("To the (N)orth, you see more of the settlement.")
    print("To the (E)ast, you see a forest.")
    print("To the (S)outh is a field.")
    print("To the (W)est is an unscalable cliff face.")

def visit_field(direction: str) -> tuple[str, str]:
    """Return the player's new location based on direction they want to move."""
    # Annotate and initialize local variables.
    location: str = "field"
    message: str = ""

    # Determine the new location based on direction.
    if direction == "E":
        location = "wood"
    elif direction == "N":
        location = "settlement"
    elif direction == "S":
        location = "gameover"
        message = "You've fallen in the river and have been swept out to sea."
    elif direction == "W":
        message = "There is an impassable cliff in that direction."
    return location, message

def visit_wood(direction: str) -> tuple[str, str]:
    """Return the player's new location based on the direction they want to move."""
    # Annotate and initialize local variables.
    location: str = "wood"
    message: str = ""

    # Determine the new location based on direction.
    if direction == "E":
        location = "wood"
    elif direction == "N":
        location = "settlement"
    elif direction == "W":
        location = "field"
    elif direction == "S":
        location = "gameover"
        message = "You've fallen in the river and have been swept out to sea."
    return location, message

def visit_settlement(direction: str) -> tuple[str, str]:
    """Return the player's new location based on the direction they want to move."""
    # Annotate and initialize local variables.
    location: str = "settlement"
    message: str = ""

    # Determine the new location based on direction.
    if direction == "E":
        location = "wood"
    elif direction == "N":
        location == "settlement"
    elif direction == "W":
        message = "There is an impassable cliff in that direction."
    elif direction == "S":
        location = "field"
    return location, message

def get_new_location(current_location: str, direction: str) -> tuple[str, str]:
    """Return the player's new location based on their current location
       and the direction they want to move."""
    # Annotate variables.
    new_location: str
    message: str 

    # Get the new location by calling the appropriate function.
    if current_location == "field":
        new_location, message = visit_field(direction)
    elif current_location == "settlement":
        new_location, message = visit_settlement(direction)
    elif current_location == "wood":
        new_location, message = visit_wood(direction)

    return new_location, message

# Annotate variables.
choice: str = "X"
location: str = "field"
message: str 

# Print a welcome message.
print("Welcome to Simple Adventure!")
print("You may type N, S, E, or W to move in a direction, or Q to quit.")

# Obtain the user's action and handle it.  The action will
# be a direction to move or to quit.
while choice != "Q":

    # Describe the current location
    if location == "field":
        print_field_description()
    elif location == "wood":
        print_wood_description()
    elif location == "settlement":
        print_settlement_description()
        
    # Obtain the user's command and update the location accordingly.
    choice = input("What is your command? (N, S, E, W, Q): ")
    if choice != "Q":
        location, message = get_new_location(location, choice)

    if message != "":
        print(message)


    # If the game ended in one of the locations, set choice to Q.
    if location == "gameover":
        choice = "Q"
