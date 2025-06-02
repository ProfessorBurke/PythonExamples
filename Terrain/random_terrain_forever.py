"""Draw a randomized, tiled endless background."""

# Import the random library.
import random
# Import and initialize pygame.
import pygame
pygame.init()


class Player(pygame.sprite.Sprite):

    # Annotate class-level constants
    UP: int = 1
    DOWN: int = 3
    LEFT: int = 2
    RIGHT: int = 0
    STOP: int = 4

    # Annotate object-level fields
    _dx: int
    _dy: int
    _speed: int
    _face_right: pygame.Surface

    def __init__(self, image: pygame.Surface, x: int, y: int, speed: int) -> None:
        """Initialize the sprite."""
        super().__init__()
        self._face_right = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._dx = 0
        self._dy = 0
        self._speed = speed

    def turn(self, direction: int) -> None:
        """Turn the player to face the direction of movement."""
        if direction != Player.STOP:
            rotation: int = direction * 90
            x: int = self.rect.centerx
            y: int = self.rect.centery
            self.image = pygame.transform.rotate(self._face_right, rotation)
            self.rect.centerx = x
            self.rect.centery = y

    def move(self, direction: int) -> None:
        self._dx = 0
        self._dy = 0
        if direction != Player.STOP:
            self.turn(direction)
            if direction == Player.LEFT:
                self._dx = -self._speed
            elif direction == Player.RIGHT:
                self._dx = self._speed
            if direction == Player.UP:
                self._dy = -self._speed
            elif direction == Player.DOWN:
                self._dy = self._speed

    def update(self, screen: pygame.Surface) -> None:
        """Move sprite by _dx, _dy."""
        self.rect.top += self._dy
        self.rect.left += self._dx
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width() - int(self.rect.width / 4)
        elif self.rect.left < 0:
            self.rect.left = int(self.rect.width / 4)
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height() - int(self.rect.height / 4)
        elif self.rect.top < 0:
            self.rect.top = int(self.rect.height / 4)

    def within_threshold(self, screen: pygame.Surface, threshold: int,
                         direction: int) -> bool:
        return ((direction == Player.UP and self.rect.top < threshold)
                or (direction == Player.DOWN and self.rect.bottom >= screen.get_height() - threshold)
                or (direction == Player.LEFT and self.rect.left < threshold)
                or (direction == Player.RIGHT and self.rect.right >= screen.get_width() - threshold))
 

class Background(pygame.sprite.Sprite):
    """ A potentially infinite scrolling tile-based background that grows as needed."""

    # Size of a tile.
    TILE_SIZE: int = 25
    # Locations of the tiles within the tiles Surface.
    DIRT_LT: tuple[int] = (0,0)
    ROCK_LT: tuple[int] = (25,0)
    GRASS_LT: tuple[int] = (25, 25)
    WATER_LT: tuple[int] = (100, 25)
    # Numbers in the terrain map for different kinds of terrain.
    DIRT: int = 0
    ROCK: int = 1
    GRASS: int = 2
    WATER: int = 3

    # Object-level fields
    _tiles: list[pygame.Surface]  # The tiles for different kinds of terrain
    _terrain: list[list[int]]     # The terrain map, a 2d list of integer
    _left_top: list[int]          # The index in the terrain map of the TL of image
    _direction: int               # Direction the player is moving if it's the background that must move.

    def __init__(self, width: int, height: int) -> None:
        """Create the terrain map and image.  The initial terrain fits in the window.
           Background begins not moving and left, top is 0,0 in the terrain map."""
        super().__init__()
        self._direction = Player.STOP
        # Create the terrain map
        self._terrain = []
        self._left_top = [0, 0]
        self._generate_initial_terrain(width, height)
        # Create the starting image from the terrain,
        # located at (0,0).
        tiles_surf: pygame.Surface = pygame.image.load("terrain.jpg").convert()
        self._tiles = [pygame.Surface((Background.TILE_SIZE, Background.TILE_SIZE)),
                       pygame.Surface((Background.TILE_SIZE, Background.TILE_SIZE)),
                       pygame.Surface((Background.TILE_SIZE, Background.TILE_SIZE)),
                       pygame.Surface((Background.TILE_SIZE, Background.TILE_SIZE))]
        self._tiles[0].blit(tiles_surf, (0, 0), pygame.Rect(Background.DIRT_LT, (Background.TILE_SIZE, Background.TILE_SIZE)))
        self._tiles[1].blit(tiles_surf, (0, 0), pygame.Rect(Background.ROCK_LT, (Background.TILE_SIZE, Background.TILE_SIZE)))
        self._tiles[2].blit(tiles_surf, (0, 0), pygame.Rect(Background.GRASS_LT, (Background.TILE_SIZE, Background.TILE_SIZE)))
        self._tiles[3].blit(tiles_surf, (0, 0), pygame.Rect(Background.WATER_LT, (Background.TILE_SIZE, Background.TILE_SIZE)))                                            
        self.image = self._get_surface(width, height)
        self.rect = self.image.get_rect()


    ########################################################################
    # Helper methods for creating a "random" terrain.                      #
    ########################################################################
    def _add_regions(self, max_regions: int, region_type: int) -> None:
        """Make pockets of a region type in the terrain by randomly generating
           a number of regions between 1 and max_regions and randomly generating
           a size, and then making a rectangle of that size at that location."""
        num_regions: int = random.randint(1, max_regions)
        region: int
        location: tuple[int]
        size: int
        row: int
        col: int
        for region in range(num_regions):
            location = (random.randint(0, len(self._terrain)),
                        random.randint(0, len(self._terrain[0])))
            size = random.randint(1, len(self._terrain)//4)
            for row in range(max(location[0]-size//2, 0), min(location[0]+size//2, len(self._terrain))):
                for col in range(max(location[1]-size//2, 0), min(location[1]+size//2, len(self._terrain[0]))):
                    self._terrain[row][col] = region_type

    def _get_neighbors(self, row: int, col: int) -> list[int]:
        """Make a list of terrain types neighboring a terrain, including the
           terrain at row, col.  Be sure not to index past edges of the terrain."""
        neighbors: list[int] = []
        rows: int = len(self._terrain)
        cols: int = len(self._terrain[0])
        row_offset: int
        col_offset: int
        new_row: int
        new_col: int
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                new_row = row + row_offset
                new_col = col + col_offset
                if 0 <= new_row and new_row < rows and 0 <= new_col and new_col < cols:
                    neighbors.append(self._terrain[new_row][new_col])
        return neighbors

    def _generate_initial_terrain(self, width: int, height: int) -> None:
        """Generate an initial terrain that is grass with pockets of dirt,
           stone, and water."""
        # Create an initial grassy area
        row: int
        col: int
        surrounding: list[int]
        for row in range(height // Background.TILE_SIZE):
            self._terrain.append([])
            for col in range(width // Background.TILE_SIZE):
                self._terrain[row].append(Background.GRASS)
        # Add water, rock, and dirt.
        self._add_regions(5, Background.WATER)
        self._add_regions(7, Background.ROCK)
        self._add_regions(6, Background.DIRT)
        # Now mess up the edges.
        for row in range(len(self._terrain)):
            for col in range(len(self._terrain[row])):
                surrounding = self._get_neighbors(row, col)
                self._terrain[row][col] = random.choice(surrounding)

    def _generate_new_tile(self, row: int, col: int) -> int:
        """Generate a new tile that will extend the current terrain."""
        # Get the surrounding tile types.
        choices = self._get_neighbors(row, col)
        # Weight non-grass tiles higher 50% of the time.
        heads: int = random.randint(0, 1)
        if heads:
            weighted_choices: list[int] = []
            choice: int
            for choice in choices:
                weighted_choices.append(choice)
                if choice != Background.GRASS:
                    weighted_choices.append(choice)
        else:
            weighted_choices = choices
        return random.choice(weighted_choices)

    def _insert_row_above(self) -> None:
        """Insert a row above the existing terrain. This becomes the new row at index zero."""
        # Create a row of random values that favor grass.
        row: list = []
        for col in range(len(self._terrain[0])):
            row.append(random.choice([Background.GRASS]*50 + [Background.WATER, Background.ROCK, Background.DIRT]))
        # Add it to the start of the list.
        self._terrain.insert(0, row)
        # Now coordinate that more with existing terrain.
        col_index: int
        for col_index in range(len(row)):
            self._terrain[0][col_index] = self._generate_new_tile(0, col_index)
        
    def _insert_row_below(self) -> None:
        """Insert a row at the bottom of the existing terrain."""
        # Create a row of random values that favor grass.
        row: list = []
        for col in range(len(self._terrain[0])):
            row.append(random.choice([Background.GRASS]*50 + [Background.WATER, Background.ROCK, Background.DIRT]))
        # Add it to the end of the list.
        self._terrain.append(row)
        # Now coordinate that more with existing terrain.
        col_index: int
        row_index: int = len(self._terrain)-1
        for col_index in range(len(row)):
            self._terrain[row_index][col_index] = self._generate_new_tile(row_index, col_index)

    def _insert_col_left(self) -> None:
        """Insert a column to the left of the existing terrain."""
        # For each row, insert a value to the left.
        # Start with random values that favor grass.
        for row in self._terrain:
            row.insert(0, random.choice([Background.GRASS]*50 + [Background.WATER, Background.ROCK, Background.DIRT]))
        # Now coordinate that more with existing terrain.
        row_index: int
        for row_index in range(len(self._terrain)):
            self._terrain[row_index][0] = self._generate_new_tile(row_index, 0)
        
    def _insert_col_right(self) -> None:
        """Insert a column to the right of the existing terrain."""
        # For each row, insert a value to the right.
        # Start with random values that favor grass.
        for row in self._terrain:
            row.append(random.choice([Background.GRASS]*50 + [Background.WATER, Background.ROCK, Background.DIRT]))
        # Now coordinate that more with existing terrain.
        last_index: int = len(self._terrain[0]) - 1
        row_index: int
        for row_index in range(len(self._terrain)):
            self._terrain[row_index][last_index] = self._generate_new_tile(row_index, last_index)

    def _get_surface(self, width: int, height: int) -> pygame.Surface:
        # The Surface to draw the tiles on.
        surf: pygame.Surface = pygame.Surface((width, height))
        # row and col index into the two-dimensional list of map tile numbers.
        row: int
        col: int
        # x and y are the blit coordinates on surf -- they will stay between 0,0 and width, height.
        x: int = 0
        y: int = 0
        # Iterate through the 2D list of map tile numbers for the part that's showing,
        # which begins at self._left_top.  Blit the correct tile for the map from the _tiles.
        for row in range(self._left_top[1], self._left_top[1] + height//Background.TILE_SIZE):
            for col in range(self._left_top[0], self._left_top[0] + width//Background.TILE_SIZE):
                surf.blit(self._tiles[self._terrain[row][col]], (x, y))
                x += Background.TILE_SIZE
            y += Background.TILE_SIZE
            x = 0
        return surf   

    ########################################################################
    # Public methods.                                                      #
    ########################################################################

    def move(self, direction: int) -> None:
        """Set the direction of movement for the background (in terms of player motion)."""
        self._direction = direction

    def update(self, screen: pygame.Surface) -> None:
        """Move the background one unit in self._direction, possibly adding terrain and redrawing."""
        # If player is moving up and we need to add terrain, add terrain.
        # Otherwise, subtract one from top.
        if self._direction == Player.UP:
            if self._left_top[1] == 0:
                self._insert_row_above()
            else:
                self._left_top[1] -= 1
            
        # If player is moving down past the border and we need to add terrain, add terrain.
        # Add one to top.
        elif self._direction == Player.DOWN:
            if (self._left_top[1] + screen.get_height() // Background.TILE_SIZE) == len(self._terrain):
                self._insert_row_below()
            self._left_top[1] += 1
            
        # If player is moving left past the border and we need to add terrain, add terrain.
        # Otherwise, subtract one from left.
        elif self._direction == Player.LEFT:
            if self._left_top[0] == 0:
                self._insert_col_left()
            else:
                self._left_top[0] -= 1
            
        # If player is moving right and we need to add terrain, add terrain.
        # Add one to left.
        elif self._direction == Player.RIGHT:
            if (self._left_top[0] + screen.get_width() // Background.TILE_SIZE) == len(self._terrain[0]):
                self._insert_col_right()
            self._left_top[0] += 1

        # If we had to move the background, redraw the image.
        if self._direction != Player.STOP:
            self.image = self._get_surface(screen.get_width(), screen.get_height())
            self.rect = self.image.get_rect()



                   

def main() -> None:
    """Allow the user to explore an infinite random space."""
    # Annotate and initialize window and background constants and variables.
    WIDTH: int = 800
    HEIGHT: int = 600
    SPEED: int = 10
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Use the arrow keys to explore")
    background: Background = Background(WIDTH, HEIGHT)
    background_group: pygame.sprite.Group = pygame.sprite.Group(background)

    # Annotate and initialize constants and variables for the sprite.
    THRESHOLD: int = 20 # how close it can get to the wall before we move the background
    player: Player = Player(pygame.image.load("class_dash_sprite.png").convert_alpha(),
                      25, 25, SPEED)
    player_group: pygame.sprite.Group = pygame.sprite.Group(player)
    direction: int = Player.STOP

    # Annotate and initialize event and game loop variables.
    user_quit: bool = False
    e: pygame.event.Event
    keys: tuple
    key: int


    # Create the clock for timing the game loop.
    clock: pygame.time.Clock = pygame.time.Clock()

    # Process events until the user chooses to quit.
    while not user_quit:
        # Loop 30 times per second
        clock.tick(30)
        for e in pygame.event.get():
            # Process a quit choice.
            if e.type == pygame.QUIT:
                user_quit = True
            elif e.type == pygame.KEYDOWN:
                key = e.__dict__["key"]
                if key == pygame.K_UP:
                    direction = Player.UP
                elif key == pygame.K_DOWN:
                    direction = Player.DOWN
                elif key == pygame.K_RIGHT:
                    direction = Player.RIGHT
                elif key == pygame.K_LEFT:
                    direction = Player.LEFT
            # If all arrow keys are up, stop the player.
            elif e.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if not (keys[pygame.K_UP] or keys[pygame.K_DOWN] or
                        keys[pygame.K_RIGHT] or keys [pygame.K_LEFT]):
                    direction = Player.STOP

        # Move the sprites if needed.
        if direction == Player.STOP:
            player.move(Player.STOP)
            background.move(Player.STOP)
        else:
            if player.within_threshold(screen, THRESHOLD, direction):
                background.move(direction)
                player.turn(direction)
                player.move(Player.STOP)
            else:
                player.move(direction)
                background.move(Player.STOP)
                    
        # Draw the background.
        background_group.update(screen)
        background_group.draw(screen)
        player_group.update(screen)
        player_group.draw(screen) 
                
        # Show the display.
        pygame.display.flip()
    pygame.quit()

main()
