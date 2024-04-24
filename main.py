# Example file showing a basic pygame "game loop"
import pygame


# TODO: refactor to ROW, COL
COL, ROW = 10, 20
TILE_SIZE = 32
RES = TILE_SIZE * COL, TILE_SIZE * ROW

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
running = True

# rect = pygame.Rect(1, 10, TILE_SIZE, TILE_SIZE)
grid = [[pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE) for c in range(COL)] for r in range(ROW)]

tetrominoes = [
    [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ], [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ], [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ], [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ], [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ], [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
]

cur_tetromino = None

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    # pygame.draw.rect(screen, GRAY, rect)

    for r in range(ROW):
        for c in range(COL):
            pygame.draw.rect(screen, GRAY, grid[r][c], 1)

    if not cur_tetromino:
        # TODO: random
        cur_tetromino = tetrominoes[4]
        tetromino_size = len(cur_tetromino)
        x, y = 3, 0

    for r in range(tetromino_size):
        for c in range(tetromino_size):
            if cur_tetromino[r][c]:
                pygame.draw.rect(
                    screen, WHITE, pygame.Rect((x + c) * TILE_SIZE, (y + r) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()