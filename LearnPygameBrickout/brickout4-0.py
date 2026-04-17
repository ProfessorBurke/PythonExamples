
# Pygame setup
import pygame
pygame.init()
pygame.display.init()

# Import libraries
import random

class Ball(pygame.sprite.Sprite):

    def __init__(self, size: int, x: int, y: int, dx: int, dy: int) -> None:
        """Create a Surface with dimensions (size, size) and initialize
           other fields from parameters.  Give Surface a colorkey of black
           and draw a white circle."""
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255),
                           (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._dx = dx
        self._dy = dy

    def update(self, screen: pygame.Surface) -> None:
        """Move the ball by dx, dy and check boundaries with the screen."""
        self.rect.left += self._dx
        self.rect.top += self._dy

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
            self._dy *= -1

class Brick(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, x: int, y: int) -> None:
        """Create a brick sprite from image at (x, y)."""
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)

# Annotate variables
ball: Ball
ball_group: pygame.sprite.Group
brick_group: pygame.sprite.Group
screen: pygame.Surface
square: pygame.Surface
paddle: pygame.Surface
sparkles: pygame.Surface
background: pygame.Surface
clock: pygame.time.Clock
e: pygame.event.Event
running: bool
x: int = 98
y: int = 98
dx: int = 5
dy: int = 5
paddle_x: int
paddle_y: int
paddle_dx: int = 10
keys: pygame.key.ScancodeWrapper # like list[bool]
i: int

# Game setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Brickout 4.0")
clock = pygame.time.Clock()

# Asset setup.
background = pygame.Surface((600, 400))
# ...Create the ball and ball group.
ball = Ball(25, 100, 100, 5, 5)
ball_group = pygame.sprite.Group(ball)
# ...Create the paddle.
paddle = pygame.Surface((100, 20))
paddle.fill((0, 0, 255))
paddle_x = screen.get_width() // 2 - paddle.get_width() // 2
paddle_y = screen.get_height() - paddle.get_height() * 2
sparkles = pygame.Surface((paddle.get_width(), paddle.get_height()))
sparkles.set_colorkey((0, 0, 0))
# ...Create the bricks and brick_group.
NUM_BRICKS: int = 10
OFFSET: int = 2
BRICK_HEIGHT: int = 20
colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
color: tuple[int]
brick_width: int = screen.get_width() // NUM_BRICKS - 2*OFFSET
brick_group = pygame.sprite.Group()
x: int = OFFSET
y: int = BRICK_HEIGHT
for color in colors:
    brick_surf: pygame.Surface = pygame.Surface((brick_width, BRICK_HEIGHT))
    brick_surf.fill(color)
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
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                background.fill((random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_dx
        if paddle_x < 0:
            paddle_x = 0
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_dx
        if paddle_x + paddle.get_width() >= screen.get_width():
            paddle_x = screen.get_width() - paddle.get_width()
    if keys[pygame.K_SPACE]:
        #sparkles.fill((0, 0, 0))
        for i in range(50):
            pygame.draw.circle(sparkles, (random.randint(0, 255),
                                          random.randint(0, 255),
                                          random.randint(0, 255)),
                               (random.randint(0, sparkles.get_width()-1),
                                random.randint(0, sparkles.get_height()-1)),
                               random.randint(1, sparkles.get_height()//6))
    else:
        sparkles.fill((0, 0, 0))


    # Update the ball.
##    ball_group.update(screen)
##    if pygame.sprite.spritecollide(ball, brick_group, True):
##        ball._dy *= -1

    # Boundary checking with paddle
    if (ball._dy > 0 and (ball.rect.bottom >= paddle_y) and
        (ball.rect.right >= paddle_x and ball.rect.left <= paddle_x + paddle.get_width())):
        ball.rect.bottom = paddle_y 
        ball._dy *= -1
    
    screen.blit(background, (0, 0))
    brick_group.draw(screen)
##    ball_group.draw(screen)
##    screen.blit(paddle, (paddle_x, paddle_y))
##    screen.blit(sparkles, (paddle_x, paddle_y))

    pygame.display.flip()

pygame.quit()
