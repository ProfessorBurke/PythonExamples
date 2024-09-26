def decimal_to_binary(n):
    result = 0
    factor = 1
    while n > 0:
        remainder = n % 2  # Get the binary digit
        n = n // 2         # Update the number (quotient)
        result += remainder * factor
        factor *= 10       # Move to the next place value in binary
    return result

# Test with a number
decimal_number = 153
binary_number = decimal_to_binary(decimal_number)
print(f"Binary of {decimal_number} is {binary_number}")
