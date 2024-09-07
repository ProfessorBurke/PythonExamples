"""
    Bouncing ball game that allows the user to change the ball's size and color.
    The walls contain two kinds of hazards that lock the ball's size and color.
    They also contain bombs and heals that go into the Ball's inventory.
    Bombs destroy everything on the walls, and heals restore the ball's ability
    to change size and color.
"""
import pygame
import random
import json
import os
from enum import Enum
    
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SAVE_FILE = "game_state.json"

class SquareKind(Enum):
    BOMB = 0
    HEAL = 1
    LOCK_SIZE = 2
    LOCK_COLOR = 3

class Inventory:
    """The Ball's inventory of squares."""

    # Object-level fields
    _bombs: int
    _heals: int
    
    def __init__(self, bombs:int = 0, heals:int = 0) -> None:
        """Initialize inventory to parameters or zero as default."""
        self._bombs = bombs
        self._heals = heals

    # Adding to the inventory
    def add_bomb(self) -> None:
        """Add a bomb."""
        self._bombs += 1

    def add_heal(self) -> None:
        """Add a heal."""
        self._heals += 1

    # Using from the inventory
    def use_bomb(self) -> bool:
        """Use a bomb, if there is a bomb.  Return True if successful."""
        success: bool = False
        if self._bombs > 0:
            self._bombs -= 1
            success = True
        return success

    def use_heal(self) -> bool:
        """Use a heal, if there is a heal.  Return True if successful."""
        success: bool = False
        if self._heals > 0:
            self._heals -= 1
            success = True
        return success

    # Save and restore
    def to_json(self) -> str:
        """Convert data to a dictionary and then to JSON.
           Return the JSON."""
        return json.dumps({
            "bombs": self._bombs,
            "heals": self._heals
        })

    @staticmethod
    def from_json(json_str: str) -> "Inventory":
        """Create and return an Inventory object from the
           json_str passed as a parameter."""
        inventory_dict: dict = json.loads(json_str)
        return Inventory(bombs = inventory_dict["bombs"],
                         heals = inventory_dict["heals"])
    
class Ball(pygame.sprite.Sprite):
    """The player character -- a ball that bounces.  The player
       can change the ball's size and color."""

    # Class-level constants
    START_SIZE = 100
    MIN_SIZE = 50
    MAX_SIZE = 150
    COLOR = pygame.Color("green")
    SPEED = 5
    INCREASE = 10
    DECREASE = -10

    # Object-level fields
    _inventory: Inventory
    _size: tuple
    _color: pygame.Color
    _dx: int
    _dy: int
    _size_locked: bool
    _color_locked: bool

    
    def __init__(self, x: int, y: int, size: int = START_SIZE,
                 color: pygame.Color = COLOR, dx: int = SPEED, dy: int = SPEED,
                 size_locked: bool = False, color_locked: bool = False,
                 inventory: Inventory = Inventory()) -> None:
        """Initialize from parameters and defaults,
           and create the image and rectangle."""
        super().__init__()
        self._size = size
        self._color = color
        self._dx, self._dy = dx, dy
        self._size_locked = size_locked
        self._color_locked = color_locked
        self._inventory = inventory
        self.update_image((x,y))

    def update_image(self, center: tuple) -> None:
        """Create the image and rectangle after a change."""
        self.image = pygame.Surface((self._size, self._size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self._color, (self._size // 2, self._size // 2), self._size // 2)
        self.rect = self.image.get_rect(center = center)

    def update(self):
        """Move and boundary check."""
        # Move by dx and dy.
        self.rect.x += self._dx
        self.rect.y += self._dy

        # Boundary check, setting location to edges if beyond,
        # and reverse direction at a boundary.
        if self.rect.left < 0:
            self._dx = -self._dx
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self._dx = -self._dx
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
            self._dy = -self._dy
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self._dy = -self._dy

    # Changes from the user
    def change_size(self, increment: int) -> None:
        """Change the size of the ball according to increment, and change
           the speed accordingly (larger balls move slower)."""
        if not self._size_locked:
            self._size = max(Ball.MIN_SIZE, min(Ball.MAX_SIZE, self._size + increment))
            self._speed = max(1, Ball.MAX_SIZE - self._size + 1)
            self.update_image(self.rect.center)

    def change_color(self) -> None:
        """Change to a random color."""
        if not self._color_locked:
            self._color = pygame.Color((random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255)))
            self.update_image(self.rect.center)

    # Changes from collisions
    def lock_size(self) -> None:
        """When _size_locked is True, the ball can't change size."""
        if not self._size_locked:
            self._size = Ball.MIN_SIZE
            self.update_image(self.rect.center)
            self._size_locked = True

    def lock_color(self) -> None:
        """When _color_locked is True, the ball can't change color."""
        if not self._color_locked:
            self._color = (pygame.Color("black"))
            self.update_image(self.rect.center)
            self._color_locked = True

    # Inventory management
    def add_bomb(self) -> None:
        """Add a bomb to the inventory."""
        self._inventory.add_bomb()

    def add_heal(self) -> None:
        """Add a heal to the inventory."""
        self._inventory.add_heal()

    def use_bomb(self) -> bool:
        """Use a bomb (if there is one) and return success."""
        return self._inventory.use_bomb()

    def use_heal(self) -> None:
        """Use a bomb (if there is one) and return success."""
        if self._inventory.use_heal():
            self._size_locked = False
            self._color_locked = False

    # Save and restore
    def to_json(self) -> str:
        """Convert data to a dictionary and then to JSON.
           Return the JSON."""
        return json.dumps({
            "inventory": self._inventory.to_json(),
            "size": self._size,
            "color": tuple(self._color),
            "dx": self._dx,
            "dy": self._dy,
            "size_locked": self._size_locked,
            "color_locked": self._color_locked,
            "x": self.rect.centerx,
            "y": self.rect.centery
        })

    @staticmethod
    def from_json(json_str: str) -> "Ball":
        """Create and return a Ball object from the
           json_str passed as a parameter."""
        ball_dict: dict = json.loads(json_str)
        return Ball(ball_dict["x"], ball_dict["y"], size = ball_dict["size"],
                    color = pygame.Color(ball_dict["color"]), 
                    dx = ball_dict["dx"], dy = ball_dict["dy"],
                    size_locked = ball_dict["size_locked"],
                    color_locked = ball_dict["color_locked"],
                    inventory = Inventory.from_json(ball_dict["inventory"]))


class Square(pygame.sprite.Sprite):
    """A good or bad item that the circle can collide with."""

    # Class-level constants
    SIZE = 20
    BOMB_COLOR = pygame.Color("red") 
    HEAL_COLOR = pygame.Color("green")
    LOCK_SIZE_COLOR = pygame.Color("yellow")
    LOCK_COLOR_COLOR = pygame.Color("black")

    # Object-level fields:
    _kind: SquareKind
    
    def __init__(self, x: int, y: int, kind: SquareKind) -> None:
        """Initialize a square from parameters."""
        super().__init__()
        self._kind = kind
        self.image = pygame.Surface((Square.SIZE, Square.SIZE))
        if kind == SquareKind.BOMB:
            self.image.fill(Square.BOMB_COLOR)
        elif kind == SquareKind.HEAL:
            self.image.fill(Square.HEAL_COLOR)
        elif kind == SquareKind.LOCK_SIZE:
            self.image.fill(Square.LOCK_SIZE_COLOR)
        else:
            self.image.fill(Square.LOCK_COLOR_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

    # Save and restore
    def to_json(self) -> str:
        """Convert data to a dictionary and then to JSON.
           Return the JSON."""
        return json.dumps({
            "kind": self._kind.value,
            "x": self.rect.x,
            "y": self.rect.y
        })

    @staticmethod
    def from_json(json_str: str) -> "Square":
        """Create and return a Square object from the
           json_str passed as a parameter."""
        square_dict: dict = json.loads(json_str)
        return Square(square_dict["x"],
                      square_dict["y"],
                      SquareKind(square_dict["kind"]))



def save_game(ball: Ball, square_group: pygame.sprite.Group) -> None:
    """Save the ball to the save file."""
    try:
        with open(SAVE_FILE, "w") as f:
            f.write(ball.to_json() + "\n")
            for square in square_group:
                f.write(square.to_json() + "\n")
    except:
        print("An error occurred while saving.")
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)

def restore_game() -> tuple:
    """Restore the ball from the save file, if it exists.
       Return the ball or None if there was an exception."""
    ball: Ball
    squares: list = []
    square_line: str
    try:
        with open(SAVE_FILE, "r") as f:
            ball = Ball.from_json(f.readline())
            square_line = f.readline()
            while square_line != "":
                squares.append(Square.from_json(square_line))
                square_line = f.readline()
                
    except:
        ball = None
        squares = None
    return ball, squares

def game() -> None:
    # Annotate variables
    screen: pygame.surface.Surface
    background: pygame.surface.Surface
    clock: pygame.time.Clock
    ball: Ball
    ball_group: pygame.sprite.Group
    square_group: pygame.sprite.Group
    event: pygame.event.Event
    kind: SquareKind
    x: int
    y: int
    square: Square
    squares: list
    hits: list
    hit: Square
    running: bool
    
    # Create the screen and background
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(pygame.Color("white"))
    screen.blit(background, (0, 0))
    pygame.display.set_caption("b for bomb, h for heal, arrow keys to change size, space to change color")

    # Create the clock
    clock = pygame.time.Clock()

    # Create the ball
    ball, squares = restore_game()
    if not ball:
        ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Create the sprite groups
    ball_group = pygame.sprite.Group()
    ball_group.add(ball)
    if not squares:
        square_group = pygame.sprite.Group()
    else:
        square_group = pygame.sprite.Group(squares)

    # Run the main game loop
    running = True
    while running:

        # Get the events off the event queue and handle them.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.change_size(Ball.INCREASE)
                elif event.key == pygame.K_DOWN:
                    ball.change_size(Ball.DECREASE)
                elif event.key == pygame.K_SPACE:
                    ball.change_color()
                elif event.key == pygame.K_b:
                    if ball.use_bomb():
                        square_group.empty()
                        print("Used a bomb")
                elif event.key == pygame.K_h:
                    ball.use_heal()
                    print("Healed")

        # Randomly spawn squares
        if random.randint(1, 100) <= 2:  
            kind = random.choice(list(SquareKind))
            x = random.choice([0, SCREEN_WIDTH - Square.SIZE])
            y = random.randint(0, SCREEN_HEIGHT - Square.SIZE)
            square = Square(x, y, kind) 
            square_group.add(square)

        # Check for and handle square collisions
        hits = pygame.sprite.spritecollide(ball, square_group, True)
        for hit in hits:
            if hit._kind == SquareKind.BOMB: 
                ball.add_bomb()
                print("Adding a bomb")
            elif hit._kind == SquareKind.HEAL:
                ball.add_heal()
                print("Adding a heal")
            elif hit._kind == SquareKind.LOCK_SIZE: 
                ball.lock_size()
                print("Locking size")
            elif hit._kind == SquareKind.LOCK_COLOR:
                ball.lock_color()
                print("Locking color")

        # Clear, update, and draw.
        square_group.clear(screen, background)
        ball_group.clear(screen, background)
        square_group.update()
        ball_group.update()
        square_group.draw(screen)
        ball_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    save_game(ball, square_group)
    pygame.quit()

if __name__ == "__main__":
    game()
