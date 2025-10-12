"""
    Generate an exit string for a location in our data structure.
    Maggie
    10/03/2025
"""

# An exhaustive test suite.
abbey: list[list[str|int]] = [["","","", 1, 1, 1, 1],          # 0: N S E W
                              ["","","", 1, 1, 1, -1],         # 1: N S E
                              ["","","", 1, 1, -1, 1],         # 2: N S W
                              ["","","", 1, 1, -1, -1],        # 3: N S                                    
                              ["","","", 1, -1, 1, 1],         # 4: N E W
                              ["","","", 1, -1, 1, -1],        # 5: N E
                              ["","","", 1, -1, -1, 1],        # 6: N W
                              ["","","", 1, -1, -1, -1],       # 7: N                                
                              ["","","", -1, 1, 1, 1],         # 8: S E W   
                              ["","","", -1, 1, 1, -1],        # 9: S E
                              ["","","", -1, 1, -1, 1],        # A: S W
                              ["","","", -1, 1, -1, -1],       # B: S                                  
                              ["","","", -1, -1, 1, 1],        # C: E W
                              ["","","", -1, -1, 1, -1],       # D: E
                              ["","","", -1, -1, -1, 1],       # E: W
                              ["","","", -1, -1, -1, -1]]      # F:

# A parallel list of correct outputs.
output: list[str] = ["There are exits to the (N)orth, (S)outh, (E)ast and (W)est.", # 0
                     "There are exits to the (N)orth, (S)outh and (E)ast.",         # 1
                     "There are exits to the (N)orth, (S)outh and (W)est.",         # 2
                     "There are exits to the (N)orth and (S)outh.",                 # 3
                     "There are exits to the (N)orth, (E)ast and (W)est.",          # 4
                     "There are exits to the (N)orth and (E)ast.",                  # 5
                     "There are exits to the (N)orth and (W)est.",                  # 6
                     "There is an exit to the (N)orth.",                            # 7
                     "There are exits to the (S)outh, (E)ast and (W)est.",          # 8
                     "There are exits to the (S)outh and (E)ast.",                  # 9
                     "There are exits to the (S)outh and (W)est.",                  # A
                     "There is an exit to the (S)outh.",                            # B
                     "There are exits to the (E)ast and (W)est.",                   # C
                     "There is an exit to the (E)ast.",                             # D
                     "There is an exit to the (W)est.",                             # E
                     "There are no exits."]                                         # F


test_num: int
i: int
exits_str: str
directions_string: list[str] = ["(N)orth", "(S)outh", "(E)ast", "(W)est"]

test_num = 0
while test_num < len(abbey):
    location: int = test_num
    exits_list: list[int] = abbey[location][3:]

    exits: list[str] = []
    i = 0
    while i < len(exits_list):
        if exits_list[i] != -1:
            exits.append(directions_string[i])
        i += 1

    if len(exits) == 0:
        exits_str = "There are no exits."
    elif len(exits) == 1:
        exits_str = "There is an exit to the " + exits[0] + "."
    elif len(exits) == 2:
        exits_str = "There are exits to the " + exits[0] + " and " + exits[1] + "."
    elif len(exits) == 3:
        exits_str = ("There are exits to the " + exits[0] + ", "
                     + exits[1] + " and " + exits[2] + ".")
    else:
        exits_str = ("There are exits to the " + exits[0] + ", "
                     + exits[1] + ", " + exits[2] + " and "
                     + exits[3] + ".")
    
    print("Generated output: " + exits_str)
    print("Expected output:  " + output[test_num])
    print("\n" + "*"*50)

    test_num += 1


    

