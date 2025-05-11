"""
    Calculate how much food our donation of US Dollars can purchase in
    Ukraine.

    Obtain the US Dollar donation amount, the exchange rate, and the cost
    of a loaf of bread in Ukraine in UAH.  Calculate the equivalent
    amount of UAH and give the number of loaves of bread that can be purchased.

    Example of how the program should look running (inputs are 100, 47.29, 32.71):
    How much is being donated (USD)? $100
    How many UAH is 1 USD worth? 47.29
    What is the cost of a loaf of bread (UAH)? 32.71
    With a donation of $100.00, you can buy 144.6 loaves of bread.
"""

# Annotate variables.
donation_usd: float
donation_uah: float
exchange_rate: float
cost_bread: float
loaves_bread: float

# Obtain the donation amount, exchange rate, and cost of bread.
donation_usd = float(input("How much is being donated (USD)? $"))
exchange_rate = float(input("How many UAH is 1 USD worth? "))
cost_bread = float(input("What is the cost of a loaf of bread (UAH)? "))

# Calculate the amount of UAH from the donation in USD and exchange rate.
donation_uah = donation_usd * exchange_rate

# Calculate the amount of bread that can be purchased.
loaves_bread = donation_uah / cost_bread

# Display the result.
print("With a donation of ${:.2f}, you can buy {:.1f} loaves of bread."
      .format(donation_usd, loaves_bread))

### The output, but with an f-string.
##print(f"With a donation of ${donation_usd:.2f}, you can buy {loaves_bread:.1f} loaves of bread.")

