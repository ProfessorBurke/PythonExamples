"""
    Calculate the distance between two points.
"""
import math

def distance_between(point1 : tuple, point2: tuple) -> float:
    """Calculate and return the distance between point1 and
       point2 using the distance formula. Each point is an
       x,y tuple. """
    return math.sqrt((point1[0]- point2[0])**2
                     + (point1[1]- point2[1])**2)

def main() -> None:
    """Test the distance_between function with user input."""
    point1: tuple
    point2: tuple
    point1 = (float(input("Please enter x of point 1: ")),
              float(input("Please enter y of point 1: ")))
    point2 = (float(input("Please enter x of point 2: ")),
              float(input("Please enter y of point 2: ")))
    print("The distance between the points is {}".
          format(distance_between(point1, point2)))

if __name__ == "__main__":
    main()

