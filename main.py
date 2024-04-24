import pygame


COL, ROW = 10, 20
TILE_SIZE = 32
RES = TILE_SIZE * COL, TILE_SIZE * ROW

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

pygame.init()
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
running = True

# rect = pygame.Rect(1, 10, TILE_SIZE, TILE_SIZE)
grid = [[pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE) for c in range(COL)] for r in range(ROW)]

class Tetris:

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

    def __init__(self, h=20, w=10) -> None:
        self.h = 20
        self.w = 10
        # self.gameboard = None

        self.cur_tetromino = None
        self.tetromino_size = 0
        self.x = 0
        self.y = 0

        self.init_tetromino()
    
    def init_tetromino(self):
        # TODO: random
        self.cur_tetromino = Tetris.tetrominoes[4]
        self.tetromino_size = len(self.cur_tetromino)
        self.x = (self.w - self.tetromino_size) // 2
        self.y = 0

    def shift_horizontal(self, dx):
        self.x += dx

    def shift_down(self):
        self.y += 1

    def rotate(self):

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
        
        if not self.cur_tetromino:
            return

        rotate(self.cur_tetromino)

tetris_game = Tetris(ROW, COL)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_LEFT:
                tetris_game.shift_horizontal(-1)
            elif event.key == pygame.K_RIGHT:
                tetris_game.shift_horizontal(1)
            elif event.key == pygame.K_DOWN:
                tetris_game.shift_down()
            elif event.key == pygame.K_UP:
                tetris_game.rotate()

    screen.fill("black")

    # pygame.draw.rect(screen, GRAY, rect)

    for r in range(ROW):
        for c in range(COL):
            pygame.draw.rect(screen, GRAY, grid[r][c], 1)

    if tetris_game.cur_tetromino:
        for r in range(tetris_game.tetromino_size):
            for c in range(tetris_game.tetromino_size):
                if tetris_game.cur_tetromino[r][c]:
                    pygame.draw.rect(
                        screen, WHITE, 
                        pygame.Rect(
                            (tetris_game.x + c) * TILE_SIZE, 
                            (tetris_game.y + r) * TILE_SIZE, 
                            TILE_SIZE, TILE_SIZE
                        )
                    )

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()