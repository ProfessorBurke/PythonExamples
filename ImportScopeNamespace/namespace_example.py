import random

def roll_die(num_sides: int) -> int:
    """Return a random number between 1 and num_sides."""
    return random.randint(1, num_sides)

def main() -> None:
    """'Roll' two d6 and display the results."""
    die1: int = roll_die(6)
    die2: int = roll_die(6)
    print("You rolled {},{}.".format(die1, die2))

if __name__ == "__main__":
    main()

