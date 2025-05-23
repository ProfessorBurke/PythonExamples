"""
    Total the investment in AI in 2019, given a file of records
    structured as:
        business type
        year
        amount invested

"""
# Import from io so we can annotate the file
# reference variable
from io import TextIOWrapper

# Annotate variables.
data: list
total: int
i: int
ai_file: TextIOWrapper

# Read the text file into a list called data.
with open("AIInvestment.txt") as ai_file:
    data = ai_file.readlines()

# Now total only the 2019 amounts.
total = 0
for i in range(8, len(data), 15):
    total += int(data[i])

# Display the total.
print("The total AI investment from 2019 is {}.".format(total))
