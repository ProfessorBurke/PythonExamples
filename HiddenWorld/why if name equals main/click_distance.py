"""
    Display the location of mouse clicks and calculate the distance
    between them.
"""
import turtle
import distance

class ClickHandler():
    """Handle clicks by drawing a line from the old click to the new click and a dot
       at the new click; display the distance between old and new clicks."""
    def __init__(self):
        """Initialize old_click to (0, 0)."""
        self.old_click = (0, 0)
        
    def on_click(self, x, y):
        """Click handler.  Draw a line between clicks, a dot at the click, and display
           the distance (using the distance formula) between clicks."""
        print("Distance between the clicks is: {}.".
              format(distance.distance_between((x,y), self.old_click)))
        turtle.setpos(x, y)
        turtle.dot(5, "black")
        self.old_click = (x, y)

def main() -> None:
    """Calculate the distance between user clicks."""

    # Create a ClickHandler object.
    clicky: ClickHandler = ClickHandler()

    # Install the callback for clicks.
    turtle.onscreenclick(clicky.on_click)

    # Start the turtle graphics loop.
    turtle.mainloop()

if __name__ == "__main__":
    main()
