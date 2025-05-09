"""
    Write a program that obtains the cost of a loaf of bread in Kyiv, Ukraine
    and the cost of a loaf of bread in Washington DC, the United States.
    Get both costs in the same currency, such as US dollars.
    If you consider the cost of bread in the United States to be 1, or 100%,
    what percentage of that is the cost of a loaf of bread in Ukraine?

    Here is an example of the program running:
    How much is a loaf of bread in Washington, D.C.? $4.04
    How much is a loaf of bread in Kyiv, Ukraine? $.71
    A loaf of bread in Ukraine costs 17.6% of a loaf of bread in the U.S.
"""
# Annotate variables.
us_bread: float
ukraine_bread: float
relative_percent: float

# Obtain the prices of bread in the US and Ukraine, in dollars.
us_bread = float(input("How much is a loaf of bread in Washington, D.C.? $"))
ukraine_bread = float(input("How much is a loaf of bread in Kyiv, Ukraine? $"))

# Calculate the relative percent cost of Ukraine bread to US bread.
relative_percent = ukraine_bread / us_bread * 100

# Display the relative percent cost to the user.
print("A loaf of bread in Ukraine costs {:.1f}% of a loaf of bread in the U.S."
      .format(relative_percent))

### An f-string version of the output.
##print(f"A loaf of bread in Ukraine costs {relative_percent:.1f}% of a loaf of bread in the U.S.")
