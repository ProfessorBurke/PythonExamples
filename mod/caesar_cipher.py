"""
    Demonstrate a Caesar cipher.
"""

def encode(character: str, shift: int) -> str:
    """Encodes a single character by shifting it to the right.
       Assume shift is < 26 and > -26. """
    encoded_character: str = character
    if character.isalpha(): 
        start = ord('A') if character.isupper() else ord('a')
        encoded_character = chr(start + (ord(character) - start + shift) % 26)
    return encoded_character  

def decode(character: str, shift: int) -> str:
    """Decodes a single character by shifting it to the left."""
    return encode(character, -shift)

# Example usage:
plaintext: str = "Hello World"
shift_amount: int = 3
encoded_text: str

# Encode
encoded_text = ''.join(encode(char, shift_amount) for char in plaintext)
print("Encoded:", encoded_text)

# Decode
print("Decoded:", ''.join(decode(char, shift_amount) for char in encoded_text))
