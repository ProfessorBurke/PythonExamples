"""
    Calculate how much food our donation of US Dollars can purchase in
    Ukraine.

    Obtain the US Dollar donation amount from the user.

    Obtain the exchange rate and the cost of a loaf of bread in UAH from
    exchangeRateAPI and numbeoAPI, respectively.

    Calculate the amount of UAH in the donation and the number of loaves of
    bread that can be purchased.

    Example of how the program should look running (input is 100, assume an
    exchange rate of 47.29 and cost of bread 32.71):
    How much is being donated (USD)? $100
    With a donation of $100.00, you can buy 144.6 loaves of bread.
"""
import requests

# Annotate variables.
donation_usd: float
donation_uah: float
exchange_rate: float
cost_bread: float
loaves_bread: float
f: "TextIO"
api_key: str
url: str
response: requests.Response
data: dict
item: dict

# Obtain the current exchange rate for Ukrainian hryvnia
# from the exchangeratesapi site

# Get my API key from a file
# (to use this code, register for your own API key and put it
#  in exchangeRateAPI.txt)
f = open("exchangeRateAPI.txt")
api_key = f.readline().strip()
f.close()

# Make the request.
url = ("http://api.exchangeratesapi.io/v1/latest"
       + "?access_key=" + api_key
       + "&symbols=UAH")
response = requests.get(url)

# If successful, set the exchange rate to the correct value from the
# response -- otherwise set to a known prior rate.
if response.status_code == 200:
    data = response.json()
    exchange_rate = data['rates']['UAH']
else:
    # Rate on 5/2/2025
    exchange_rate = 41.76

# Obtain the price of bread in Kyiv, Ukraine from numbeo.com.
# Get my API key from a file
# (to use this code, register for your own API key and put it
#  in numbeoAPI.txt; note this service costs money)
f = open("numbeoAPI.txt")
api_key = f.readline().strip()
f.close()

city = "Kyiv"
country = "Ukraine"

url = ("https://www.numbeo.com/api/city_prices"
       +"?api_key=" + api_key
       +"&query=" + city
       +"&country=" + country)

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for item in data["prices"]:
        if "bread" in item["item_name"].lower():
            cost_bread = item["average_price"]
else:
    # Average price on 5/3/2025
    cost_bread = 32.714285714285715

# Obtain the donation amount.
donation_usd = float(input("How much is being donated (USD)? $"))

# Calculate the amount of UAH from the donation in USD and exchange rate.
donation_uah = donation_usd * exchange_rate

# Calculate the amount of bread that can be purchased.
# Round down to a whole number.
loaves_bread = donation_uah / cost_bread

# Display the result.
print("With a donation of ${:.2f}, you can buy {:.1f} loaves of bread."
      .format(donation_usd, loaves_bread))




