import pygame
import random


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

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

    def __init__(self, height=20, width=10, block_size=32, fps=60) -> None:

        self.h = height
        self.w = width
        self.block_size = block_size
        self.res = self.block_size * self.w, self.block_size * self.h
        self.fps = fps
        self.gameboard = [[0] * self.w for _ in range(self.h)]

        self.cur_tetromino = None
        self.tetromino_type = 0
        self.tetromino_size = 0
        self.x = 0
        self.y = 0

        self.init_tetromino()
    
    def init_tetromino(self):
        self.tetromino_type = random.randint(0, len(Tetris.tetrominoes) - 1)
        self.cur_tetromino = Tetris.tetrominoes[self.tetromino_type]
        self.tetromino_size = len(self.cur_tetromino)
        self.x = (self.w - self.tetromino_size) // 2
        self.y = 0

    def shift_horizontal(self, dx):
        self.x += dx
        if dx < 0:
            for r in range(self.tetromino_size):
                for c in range(self.tetromino_size):
                    if self.cur_tetromino[r][c]:
                        if self.has_collision(self.y + r, self.x + c):
                            self.x -= dx
                            return
                        else:
                            break
        else:
            for r in range(self.tetromino_size):
                for c in range(self.tetromino_size - 1, -1, -1):
                    if self.cur_tetromino[r][c]:
                        if self.has_collision(self.y + r, self.x + c):
                            self.x -= dx
                            return
                        else:
                            break

    def shift_down(self):
        self.y += 1
        for c in range(self.tetromino_size):
            for r in range(self.tetromino_size - 1, -1, -1):
                if self.cur_tetromino[r][c]:
                    if self.has_collision(self.y + r, self.x + c):
                        self.y -= 1
                        self.touch_down()
                        self.init_tetromino()
                        return
                    else:
                        break
    
    def touch_down(self):
        dirty_rows = set()
        for r in range(self.tetromino_size):
            for c in range(self.tetromino_size):
                if self.cur_tetromino[r][c]:
                    self.gameboard[self.y + r][self.x + c] = self.cur_tetromino[r][c]
                    dirty_rows.add(self.y + r)
        self.check_lines(dirty_rows)
    
    def check_lines(self, rows):
        num_completed_lines = 0
        for r in rows:
            is_completed = True
            for c in range(self.w):
                if not self.gameboard[r][c]:
                    is_completed = False
                    continue
            if is_completed:
                self.clear_line(r)
                num_completed_lines += 1

        # TODO: logic for handling score
    
    def clear_line(self, row):
        del self.gameboard[row]
        self.gameboard = [[0] * self.w] + self.gameboard

    def rotate(self):

        def rotate_clockwise(matrix):
            transpose(matrix)
            reflect(matrix)
        
        def rotate_counter_clockwise(matrix):
            reflect(matrix)
            transpose(matrix)
            
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

        rotate_clockwise(self.cur_tetromino)
        # rotate_counter_clockwise(self.cur_tetromino)
        
        for r in range(self.tetromino_size):
            for c in range(self.tetromino_size):
                if self.cur_tetromino[r][c] and self.has_collision(self.y + r, self.x + c):
                    rotate_counter_clockwise(self.cur_tetromino)
                    return
    
    # check collision for one block
    def has_collision(self, r, c):
        if c < 0 or c >= self.w or r >= self.h or self.gameboard[r][c]:
            return True
        return False

    def run(self):

        pygame.init()
        screen = pygame.display.set_mode(self.res)

        grid = [[pygame.Rect(c * self.block_size, r * self.block_size, self.block_size, self.block_size) for c in range(self.w)] for r in range(self.h)]

        clock = pygame.time.Clock()
        running = True
        
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_LEFT:
                        self.shift_horizontal(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.shift_horizontal(1)
                    elif event.key == pygame.K_DOWN:
                        self.shift_down()
                    elif event.key == pygame.K_UP:
                        self.rotate()

            screen.fill("black")

            for r in range(self.h):
                for c in range(self.w):
                    if self.gameboard[r][c]:
                        pygame.draw.rect(screen, WHITE, grid[r][c])
                    else:
                        pygame.draw.rect(screen, GRAY, grid[r][c], 1)

            if self.cur_tetromino:
                for r in range(self.tetromino_size):
                    for c in range(self.tetromino_size):
                        if self.cur_tetromino[r][c]:
                            pygame.draw.rect(
                                screen, WHITE, 
                                pygame.Rect(
                                    (self.x + c) * self.block_size, 
                                    (self.y + r) * self.block_size, 
                                    self.block_size, self.block_size
                                )
                            )

            pygame.display.flip()

            clock.tick(self.fps)
            
        pygame.quit()

if __name__ == '__main__':
    tetris_game = Tetris()
    tetris_game.run()
