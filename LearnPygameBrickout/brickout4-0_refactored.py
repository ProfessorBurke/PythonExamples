
# Pygame setup
import pygame
pygame.init()
pygame.display.init()

# Import libraries
import random

class Brick(pygame.sprite.Sprite):
    """An individual brick.  The goal of the game is to destroy all bricks.
       Bricks are rectangular colored Surfaces with a location.
    """
    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)

class Paddle(pygame.sprite.Sprite):
    """The player-controlled paddle.  It is controlled by the keyboard.
    """
    STILL: int = 0
    MOVING_RIGHT: int = 1
    MOVING_LEFT: int = 2

    def __init__(self, width: int, height: int, x: int, y: int, dx: int) -> None:
        super().__init__()
        self._dx = dx
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._moving = Paddle.STILL
        
    def update(self, screen: pygame.Surface) -> None:
        if self._moving == Paddle.MOVING_LEFT:
            self.rect.left -= self._dx
            if self.rect.left < 0:
                self.rect.left = 0
        elif self._moving == Paddle.MOVING_RIGHT:
            self.rect.left += self._dx
            if self.rect.right >= screen.get_width():
                self.rect.right = screen.get_width()

    def set_moving(self, keys: pygame.key.ScancodeWrapper)-> None:
        """Update motion according to what keys are pressed."""
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            self._moving = Paddle.STILL
        elif keys[pygame.K_LEFT]:
            self._moving = Paddle.MOVING_LEFT
        elif keys[pygame.K_RIGHT]:
            self._moving = paddle.MOVING_RIGHT
        else:
            self._moving = Paddle.STILL
        
class Ball(pygame.sprite.Sprite):
    """
        Attributes:
        image, _dx, _dy
        Public methods:
        __init__, update, draw
    """
        
    def __init__(self, size: int, x: int, y: int, dx: int, dy: int) -> None:
        """Create a Surface with dimensions (size, size), set colorkey to
           black and draw a circle.  Set fields from remaining parameters."""
        super().__init__()
        self._dx = dx
        self._dy = dy
        self.image = pygame.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255),
                           (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._in_play = True

    def update(self, screen: pygame.Surface) -> None:
        """Change x and y by dx and dy and boundary check with screen."""
        self.rect.left += self._dx
        self.rect.top += self._dy

        # Boundary checking
        if self.rect.left <= 0:
            self.rect.left = 0
            self._dx *= -1
        elif self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()
            self._dx *= -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self._dy *= -1
        elif self.rect.bottom >= screen.get_height():
            self.rect.bottom = screen.get_height()
            self._dy = 0
            self._in_play = False

    def in_play(self) -> bool:
        """Return True if the ball is still in play; False otherwise."""
        return self._in_play

    def bounce(self) -> None:
        """Bounce the ball."""
        self._dy *= -1

        
# Annotate variables
screen: pygame.Surface
background: pygame.Surface
clock: pygame.time.Clock
e: pygame.event.Event
running: bool

keys: pygame.key.ScancodeWrapper # like list[bool]
i: int
ball: Ball
ball_group: pygame.sprite.Group
#balls: list[Ball]
brick: Brick
brick_group: pygame.sprite.Group
brick_x: int = 0
brick_y: int = 0

# Game setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Brickout 4.0")
clock = pygame.time.Clock()

# Asset setup.
background = pygame.Surface((600, 400))

# Create the paddle
PADDLE_WIDTH: int = 100
PADDLE_HEIGHT: int = 20
paddle_dx: int = 10
paddle_x: int = screen.get_width() // 2 - PADDLE_WIDTH // 2
paddle_y: int = screen.get_height() - PADDLE_HEIGHT * 2
paddle: Paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, paddle_x, paddle_y, paddle_dx)
paddle_group: pygame.sprite.Group = pygame.sprite.Group(paddle)

# Create the ball
ball = Ball(25, 100, 100, 5, 5)
ball_group = pygame.sprite.Group(ball)

# Create the bricks
NUM_BRICKS: int = 10
OFFSET: int = 2
BRICK_HEIGHT: int = 20
brick_colors: list[tuple] = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
brick_group = pygame.sprite.Group()
brick_width: int = screen.get_width() // NUM_BRICKS - OFFSET * 2

x: float = OFFSET
y: int = BRICK_HEIGHT
for color in brick_colors:
    brick_surf = pygame.Surface((brick_width, BRICK_HEIGHT))
    brick_surf.fill((color))
    for i in range(NUM_BRICKS):
        brick_group.add(Brick(brick_surf, x, y))
        x += brick_width + OFFSET * 2
    y += BRICK_HEIGHT + OFFSET
    x = OFFSET  

# Game loop
running = True
while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONUP:
            x, y = e.pos

    # Clear the location of bricks, paddle, and ball.
    brick_group.clear(screen, background)
    ball_group.clear(screen, background)
    paddle_group.clear(screen, background)

    # Update the paddle according to what keys are pressed.
    keys = pygame.key.get_pressed()
    paddle.set_moving(keys)
    paddle_group.update(screen)

    # Update the ball and check for brick and paddle collisions if it's in play.
    ball_group.update(screen)
    if ball.in_play():
        if pygame.sprite.spritecollide(ball, brick_group, True):
            ball.bounce()

        if pygame.sprite.spritecollide(ball, paddle_group, False):
            ball.rect.bottom = paddle.rect.top
            ball.bounce()
    else:
        ball_group.remove(ball)
            
    # Draw the new state of bricks, paddle, and ball.
    brick_group.draw(screen)
    ball_group.draw(screen)
    paddle_group.draw(screen)

    pygame.display.flip()

pygame.quit()
