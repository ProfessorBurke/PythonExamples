"""
    Demonstrate Python name resolution error.
    Note that I'm not annotating variables here just to
    avoid any confusion that annotation defines a variable.
    It doesn't.  You can annotate this and it won't make
    a difference.
"""

# Define a global variable.
x = 0

def funky1() -> None:
    """Access the global variable x."""
    print(x)

def funky2() -> None:
    """Define and access a local variable x."""
    x = 10
    print(x)

def funky3() -> None:
    """Now let the funk hit the fan."""
    print(x)
    x = 10

funky1()
funky2()
funky3()



