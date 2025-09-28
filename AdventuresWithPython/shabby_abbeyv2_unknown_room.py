"""
    Shabby Abbey v2
    Checking for both direction and current room -- an example
    of how a simple if statement isn't going to cut it!
    Obtain a command from the player and manipulate it.
    Maggie
    9/27/2025
"""
# Annotate variable.
command: str

# Greet the player.
print("Welcome, Adventurer!")

# Describe the current location.
#print("You're in the cloister.")
#print("There are exits to the (N)orth, (S)outh, (E)ast, and (W)est.")

# Obtain the player's command and convert to uppercase.
command = input("What is your command? ")
command = command.upper()
#command = command[0]

room = "church"

# Move the player based on their command.
if room == "cloister":
    if command == "N" or command == "NORTH":
        print("You're in the church.")
        print("There is an exit to the (S)outh.")
    elif command == "S" or command == "SOUTH":
        print("You're in the kitchen.")
        print("There is an exit to the (N)orth.")
    elif command == "E" or command == "EAST":
        print("You're in the library.")
        print("There is an exit to the (W)est.")
    elif command == "W" or command == "WEST":
        print("You're in the garden.")
        print("There is an exit to the (E)ast.")  
    else:
        print("I didn't understand that command.")
elif room == "church":
    if command == "S" or command == "SOUTH":
        print("You're in the cloister.")
        print("There are exits to the (N)orth, (S)outh, (E)ast, and (W)est.")
    elif (command == "N" or command == "NORTH"
          or command == "E" or command == "EAST"
          or command == "W" or command == "WEST"):
        print("You bumped into a wall.")
        print("You're in the church.")
        print("There is an exit to the (S)outh.")        
    else:
        print("I didn't understand that command.")    
elif room == "kitchen":
    if command == "N" or command == "NORTH":
        print("You're in the cloister.")
        print("There are exits to the (N)orth, (S)outh, (E)ast, and (W)est.")
    elif (command == "S" or command == "SOUTH"
          or command == "E" or command == "EAST"
          or command == "W" or command == "WEST"):
        print("You bumped into a wall.")
        print("You're in the kitchen.")
        print("There is an exit to the (N)orth.")
    else:
        print("I didn't understand that command.")
elif room == "library":
    if command == "W" or command == "WEST":
        print("You're in the cloister.")
        print("There are exits to the (N)orth, (S)outh, (E)ast, and (W)est.")
    elif (command == "S" or command == "SOUTH"
          or command == "E" or command == "EAST"
          or command == "N" or command == "NORTH"):
        print("You bumped into a wall.")
        print("You're in the library.")
        print("There is an exit to the (W)est.")
    else:
        print("I didn't understand that command.")
elif room == "garden":
    if command == "E" or command == "EAST":
        print("You're in the cloister.")
        print("There are exits to the (N)orth, (S)outh, (E)ast, and (W)est.")
    elif (command == "S" or command == "SOUTH"
          or command == "W" or command == "WEST"
          or command == "N" or command == "NORTH"):
        print("You bumped into a wall.")
        print("You're in the garden.")
        print("There is an exit to the (E)ast.")  
    else:
        print("I didn't understand that command.") 

print("Thank you for playing.")

