"""
    Fixing while True code.
"""

##The pseudocode from the question
##do{
##  get some input.
##  if the input meets my conditions, break;
##  Otherwise ask again.
##} while(true)

# A solution to the original question that doesn't use
# while(true) and break
def valid_input(input_value: int) -> bool:
    """Validate that input_value is between 1 and 10."""
    return 1 <= input_value and input_value <= 10

input_value = int(input("Please enter a number between 1 and 10: "))
while not valid_input(input_value):
    print("That number isn't between 1 and 10.")
    input_value = int(input("Please enter a number between 1 and 10: "))

assert 1 <= input_value and input_value <= 10


### A strawman argument about why we should use a flag
##while True:
##    do_stuff_needed_at_start_of_loop()
##    inp: int = get_some_input()
##    if (testCondition(inp)):
##        break
##    act_on_input(inp)
##
##
### The strawman "remedy" as an example of bad non-while true code.
##running:bool = True
##while running:
##    do_stuff_needed_at_start_of_loop()
##    inp: int = get_some_input()
##    if testCondition(inp):
##        running = False
##    else:
##        act_on_input(inp)
##


# The while True version
while True:
    input_value: int = int(input("Please enter a positive number: "))
    input_value2: int = int(input("Please enter another positive number: "))
    input_value3: int = int(input("Please enter a third positive number: "))
    if (input_value <= 0 or inputValue2 <= 0 or inputValue3 <= 0)
	break;
    print("Congratulations!  You entered three positive numbers.")

		
print("You've made it past the second loop!")

# The imagined loop reimagined without while(true) or the flag.
input_value: int = 1
input_value2: int = 1
input_value3: int = 1

def still_running(a: int, b: int, c: int) -> bool:
    """Determine if we're still running if all values are positive."""
    return a > 0 and b > 0 and c > 0


while (still_running(input_value, input_value2, input_value3)):
    input_value: int = int(input("Please enter a positive number: "))
    input_value2: int = int(input("Please enter another positive number: "))
    input_value3: int = int(input("Please enter a third positive number: "))
    if (input_value > 0 and inputValue2 > 0 and inputValue3 > 0):
        print("Congratulations!  You entered three positive numbers.")





