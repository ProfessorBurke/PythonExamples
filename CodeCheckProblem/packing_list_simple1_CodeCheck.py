"""
    Determine what items should be packed depending on mode of travel.
    
    If the user answers "yes" to the question about traveling by plane,
    the output should be:
    You should pack:
    what you need for your destination
    headphones
    reading material
    
    If they answer anything other than "yes", the output should be:
    You should pack:
    what you need for your destination
"""
##IN yes
##IN no
##IN absolutely

plane_answer: str
packing_list: str = ""

# Obtain the answer to the air travel question from the user.
plane_answer = input("Are you traveling by plane? (yes / no): ")

# Determine what should be packed based on the travel answer.
packing_list += "what you need for your destination"
# Write an if statement that will be True if the output should
# include headphones and reading material and then append the string
# provided below to the packing list if the user is traveling by
# plane.
##HIDE
if plane_answer == "yes":
##EDIT if
##HIDE
    packing_list += "\nheadphones\nreading material"
##EDIT "\nheadphones\nreading material"


# Display the packing list to the user.
print("You should pack:")
print(packing_list)


"""
Public URL (for your students): https://codecheck.io/files/22060413157uisqvpjjtnzpzncisithtbrw
Edit URL (for you only): https://codecheck.io/private/problem/22060413157uisqvpjjtnzpzncisithtbrw/DVD7XRR2CTSGPGON6GQ75KC46
"""
