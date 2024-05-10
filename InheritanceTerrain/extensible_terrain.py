"""Scrolling, tiled background sprite
   with wall collision detection."""

# Imports and initialize pygame.
import pygame
import io
import math
import random
pygame.init()

# Constants
LEFT: int = 0
RIGHT: int = 1
UP: int = 2
DOWN: int = 3
NOT_MOVING: int = -1

class Brick(pygame.sprite.Sprite):
    """Just another brick..."""

    def __init__(self, x: int, y: int, length: int, width: int) -> None:
        """Create an invisible sprite."""
        super().__init__()
        self.image = pygame.Surface((width, length))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx: int, dy: int) -> None:
        """Move by dx and dy."""
        self.rect.left += dx
        self.rect.right += dy

class DiscoBrick(Brick):
    """Just another brick..."""

    # Annotate object-level fields
    _counter: int
    _glow: pygame.Surface

    def __init__(self, x: int, y: int, length: int, width: int) -> None:
        """Create an invisible sprite."""
        super().__init__(x, y, length, width)
        self.image = pygame.Surface((width, length), flags = pygame.SRCALPHA)
        self._glow = pygame.image.load("smallwhiteglow.png").convert_alpha()
        self._glow.set_alpha(150)
        self._counter = random.randint(0, 100)


    def update(self):
        self._counter += 1
        if self._counter == 120:
            rand_color = pygame.Color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            self.image.fill(rand_color)
            rand_color = rand_color.lerp(pygame.Color(255, 255, 255), .2)
            self.image.fill(rand_color, (3, 3, self.rect.width-6, self.rect.height-6))
            self.image.blit(self._glow, (0, 0))
        
        elif self._counter == 180:
            self._counter = 0
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))

class Portal(Brick):
    """The cake is a lie."""

    # Annotate object-level fields
    _counter: int
    _spirals: list
    
    def __init__(self, x: int, y: int, length: int, width: int) -> None:
        """Create an invisible sprite."""
        super().__init__(x, y, length, width)
        self._spirals = [pygame.image.load("spiral1.jpg").convert(),
                         pygame.image.load("spiral2.jpg").convert(),
                         pygame.image.load("spiral3.jpg").convert(),
                         pygame.image.load("spiral4.jpg").convert()]
        self._counter = 0

    def update(self):
        self._counter += 1
        if self._counter % 10 == 0:
            self.image.blit(self._spirals[self._counter//10 - 1], (0,0))
            if self._counter == 40:
                self._counter = 0


class ScrollingBackground(pygame.sprite.Sprite):
    """A tile-based scrolling background."""

    # Annotate object-level fields
    _speed: int

    def __init__(self, terrain_data: dict, terrain_file: str) -> None:
        """Load map and build Surface."""
        # Annotate and initialize local variables
        name: str
        line: str
        tile_size: int
        width: int
        height: int
        x: int = 0
        y: int = 0
        tile: Brick
        terrain: io.TextIOWrapper
        # Superclass init.
        super().__init__()
        # Load the images to pygame Surfaces.

        # Load the terrain map into a 2D list.
        terrain_map: list = []
        with open(terrain_file) as terrain:
            line = terrain.readline()
            while line != "":
                terrain_map.append(line.split())
                line = terrain.readline()
        # Calculate the size of the Surface and create.
        tile_size = terrain_data[0][1].get_width()
        width = len(terrain_map[0]) * tile_size
        height = len(terrain_map) * tile_size
        self.image = pygame.Surface((width, height)) 
        # Blit the images to the Surface.
        # Create a Block if necessary.
        for row in terrain_map:
            for i in row:
                self.image.blit(terrain_data[int(i)][1], (x, y))
                if terrain_data[int(i)][0]:
                    # The first element in the list is the class of the
                    # object to create.
                    tile = terrain_data[int(i)][0](x, y, tile_size, tile_size)
                    # The third element in the list is the list of bricks
                    # to add the tile to.
                    for group in terrain_data[int(i)][2]:
                        group.add(tile)
                x += tile_size
            y += tile_size
            x = 0
        # Complete initialization
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self._speed = 5

    def scroll(self, direction: int, screen: pygame.Surface,
               brick_groups: list) -> None:
        """Move left, right, or not at all."""
        # Annotate and initialize local variable
        left: int = self.rect.left
        # Scroll image and bricks.
        if direction == LEFT:
            self.rect.left += self._speed
            if self.rect.left > 0:
                self.rect.left = 0
        elif direction == RIGHT:
            self.rect.left -= self._speed
            if self.rect.right < screen.get_width():
                self.rect.right = screen.get_width()
        for group in brick_groups:
            for brick in group:
                brick.move(self.rect.left - left, 0)

    def can_scroll(self, screen: pygame.Surface, direction: int) -> bool:
        """Return True if can scroll in direction."""
        scroll: bool = False
        if direction == LEFT and self.rect.left < 0:
            scroll = True
        elif direction == RIGHT and self.rect.right > screen.get_width():
            scroll = True
        return scroll


class Penguin(pygame.sprite.Sprite):
    """A player-controlled character."""

    # Annotate object-level fields
    _raw_image: pygame.Surface
    _speed: int
    _angle: int

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize from parameters."""
        super().__init__()
        self._raw_image = pygame.image.load("top_penguin.png")
        self._raw_image = self._raw_image.convert_alpha()
        self.image = self._raw_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, screen.get_height() / 2 - self.rect.height / 2)
        self._speed = 5
        self._angle = 0

    def move(self, screen: pygame.Surface, threshold: int,
             direction: int, background: ScrollingBackground) -> bool:
        """Attempt to move, return True if moved."""
        moved: bool = False
        if direction == LEFT:
            self._angle = 180
            self.image = pygame.transform.rotate(self._raw_image, 180)
            if not(self.rect.left < threshold and background.can_scroll(screen, direction)):
                self.rect.left -= self._speed
                if self.rect.left < 0:
                    self.rect.left = 0
                moved = True 
        elif direction == RIGHT:
            self._angle = 0
            self.image = self._raw_image
            if not (self.rect.right > screen.get_width() - threshold
                    and background.can_scroll(screen, direction)):
                self.rect.left += self._speed
                if self.rect.right > screen.get_width():
                    self.rect.right = screen.get_width()
                moved = True
        elif direction == UP:
            self._angle = 270
            self.image = pygame.transform.rotate(self._raw_image, 90)
            self.rect.top -= self._speed
            if self.rect.top < 0:
                self.rect.top = 0
            moved = True 
        elif direction == DOWN:
            self._angle = 90
            self.image = pygame.transform.rotate(self._raw_image, -90)
            self.rect.top += self._speed
            if self.rect.bottom > screen.get_height():
                self.rect.bottom = screen.get_height()
            moved = True
        return moved

    def backup(self) -> None:
        """Back up one unit displacement vector."""
        # Calculate a unit vector
        dx: float = -math.cos(math.radians(self._angle))  
        dy: float = -math.sin(math.radians(self._angle)) 
        # Add to rectangle
        self.rect.left += dx
        self.rect.top += dy        
            
def make_window(width: int, height: int, caption: str) -> pygame.Surface:
    """Create and return a pygame window."""
    screen: pygame.Surface
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def main() -> None:
    """The arrow keys move the penguin or scroll."""
    # Annotate and initialize variables.
    SCREEN_SIZE: int = 480
    screen: pygame.Surface
    background: ScrollingBackground
    bkgd_group: pygame.sprite.Group
    bricks: pygame.sprite.Group
    penguin: Penguin
    penguin_group: pygame.sprite.Group
    user_quit: bool = False
    e: pygame.event.Event
    scroll_threshold: int = 100
    direction: int = NOT_MOVING
    terrain_data: dict
    disco: pygame.sprite.Group
    portal_in: pygame.sprite.Group
    portal_out: pygame.sprite.Group

    # Create the terrain dictionary.
    screen = make_window(SCREEN_SIZE, SCREEN_SIZE, "Scrolling Background")
    bricks = pygame.sprite.Group()
    disco = pygame.sprite.Group()
    portal_in = pygame.sprite.Group()
    portal_out = pygame.sprite.Group()
    
    terrain_data = { 0: [Brick,
                         pygame.image.load("ice_block.jpg").convert(),
                         [bricks]],
                     1: [None,
                         pygame.image.load("ice_wall.jpg").convert(),
                         []],
                     2: [DiscoBrick,
                         pygame.image.load("ice_wall.jpg").convert(),
                         [disco]],
                     3: [Portal,
                         pygame.image.load("ice_wall.jpg").convert(),
                         [portal_in]],
                     4: [Portal,
                         pygame.image.load("ice_wall.jpg").convert(),
                         [portal_out]]}
    
    # Set up the rest of the assets.
    image_files: list = ["ice_block.jpg", "ice_wall.jpg"]
    background = ScrollingBackground(terrain_data, "ice_castle_top.txt")
    bkgd_group = pygame.sprite.Group(background)
    penguin = Penguin(screen)
    penguin_group = pygame.sprite.Group(penguin)
    clock: pygame.time.Clock = pygame.time.Clock()

    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)

        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.KEYDOWN:
                # Process movement arrow keys.
                if e.__dict__["key"] == pygame.K_LEFT:
                    direction = LEFT
                elif e.__dict__["key"] == pygame.K_RIGHT:
                    direction = RIGHT
                elif e.__dict__["key"] == pygame.K_UP:
                    direction = UP
                elif e.__dict__["key"] == pygame.K_DOWN:
                    direction = DOWN
            elif e.type == pygame.KEYUP:
                if (not pygame.key.get_pressed()[pygame.K_LEFT] 
                        and not pygame.key.get_pressed()[pygame.K_RIGHT]
                        and not pygame.key.get_pressed()[pygame.K_UP]
                        and not pygame.key.get_pressed()[pygame.K_DOWN]):
                    direction = NOT_MOVING

        # Move the penguin or the background.
        penguin_group.clear(screen, background.image)
        if not penguin.move(screen, scroll_threshold, direction, background):
            background.scroll(direction, screen, [bricks, disco, portal_in, portal_out])
        # Check for collisions.
        while pygame.sprite.spritecollide(penguin, bricks, False):
            penguin.backup()
        if pygame.sprite.spritecollide(penguin, portal_in, False):
            new_brick = random.choice(portal_out.sprites())
            penguin.rect = new_brick.rect.copy()
        # Redraw and show.
        disco.update()
        portal_in.update()
        portal_out.update()
        bkgd_group.draw(screen)
        disco.draw(screen)
        portal_in.draw(screen)
        portal_out.draw(screen)
        penguin_group.draw(screen)
        pygame.display.flip()
         
    pygame.quit()

main()
