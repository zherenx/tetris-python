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

def rotate(matrix):
    transpose(matrix)
    reflect(matrix)
    
def transpose(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[j][i], matrix[i][j] = matrix[i][j], matrix[j][i]

def reflect(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n // 2):
            matrix[i][j], matrix[i][-j - 1] = matrix[i][-j - 1], matrix[i][j]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_LEFT:
                x -= 1
            elif event.key == pygame.K_RIGHT:
                x += 1
            elif event.key == pygame.K_DOWN:
                y += 1
            elif event.key == pygame.K_UP:
                if cur_tetromino:
                    rotate(cur_tetromino)

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