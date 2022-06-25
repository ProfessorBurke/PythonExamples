"""
    Demonstrate Python name resolution error.
    Note that I'm not annotating variables here just to
    avoid any confusion that annotation defines a variable.
    It doesn't.  You can annotate this and it won't make
    a difference.
"""


def funky1(x) -> None:
    """Access the global variable x."""
    print(x)

def funky2() -> None:
    """Define and access a local variable x."""
    x = 10
    print(x)

def funky3(x) -> None:
    """Now let the funk hit the fan."""
    print(x)
    x = 10

def main() -> None:
    x = 0
    funky1(x)
    funky2()
    funky3(x)

main()

