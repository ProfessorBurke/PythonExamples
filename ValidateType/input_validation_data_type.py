"""
    Demonstrate input validation of data type with a loop.
"""

# Annotate variables.
password: str
patient_temp: float
patient_age: int
numeric: bool = True

# Obtain the user's password.
# Password must be at least eight characters.
# The input function always returns a string, so we do not
# need to validate type.
password = input("Please enter your password: ")
while len(password) < 8:
    print("The password must be at least eight characters.")
    password = input("Please enter your password: ")

# Obtain the patient's temperature.
# The temperature must be between 65 and 110 degrees Fahrenheit.
# Validate that the user has given us a float.
try:
    patient_temp = float(input("What is the patient's temperature? "))
except ValueError:
    print("The patient temperature must be numeric.")
    patient_temp = 0
    numeric = False
while patient_temp < 65 or patient_temp > 110:
    if numeric:
        print("Patient temperature must be between 65 and 110.")
    numeric = True
    try:
        patient_temp = float(input("What is the patient's temperature? "))
    except:
        print("The patient temperature must be numeric.")
        numeric = False
        

# Obtain the patient's age.
# This version validates only that the input is an int.
# It does not validate range.
# Note that a plain "except:" will catch all exceptions.
try:
    patient_age = int(input("What is the patient's age? "))
except ValueError:
    numeric = False   
while not numeric:
    print("The patient age must be numeric.")
    numeric = True
    try:
        patient_age = int(input("What is the patient's age? "))
    except:
        numeric = False
        
    
