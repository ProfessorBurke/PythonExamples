"""
    Checksum example.
"""

def number_to_digits(number: int) -> list[int]:
    """Given an integer, return a list of its digits, peeled off using mod."""
    digits: list[int] = []
    while number > 0:
        # Get the last digit using mod
        digit: int = number % 10
        # Add the digit to the start of the list
        digits.insert(0, digit)
        # Remove the last digit using integer division
        number //= 10             
    return digits

# Example data
number_to_checksum: int = 53872  
expected_checksum: int = 5

# Turn the number into a list to facilitate the summing.
digits: list[int] = number_to_digits(number_to_checksum)
total: int = sum(digits)

# Validate the checksum
if total % 10 == expected_checksum:
    print("Checksum is valid.")
else:
    print("Checksum is invalid.")




