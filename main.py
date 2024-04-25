from copy import deepcopy
import pygame
import random


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

class Tetromino:

    def __init__(self, shape, color):
        self.shape = deepcopy(shape)
        self.color = color
        self.size = len(self.shape)

    def rotate_clockwise(self):
        transpose(self.shape)
        reflect(self.shape)
    
    def rotate_counter_clockwise(self):
        reflect(self.shape)
        transpose(self.shape)

class Tetris:

    tetromino_shapes = [
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], [
            [1, 1],
            [1, 1]
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

    tetromino_colors = [
        (0, 255, 255),
        (255, 255, 0),
        (128, 0, 128),
        (0, 0, 255),
        (255, 127, 0),
        (0, 255, 0),
        (255, 0, 0)
    ]

    grid_color = (40, 40, 40)

    def __init__(self, height=20, width=10, block_size=32, fps=60) -> None:

        self.h = height
        self.w = width
        self.block_size = block_size
        self.res = self.block_size * self.w, self.block_size * self.h
        self.fps = fps

        self.gameboard = [[0] * self.w for _ in range(self.h)]

        self.cur_tetromino = None
        self.x = 0
        self.y = 0

        self.free_fall_interval = 1000 # TODO: update when level up
        self.free_fall_timer_event = pygame.USEREVENT + 1

        self.init_next_tetromino()
    
    def init_next_tetromino(self):
        tetromino_type = random.randint(0, len(Tetris.tetromino_shapes) - 1)
        self.cur_tetromino = Tetromino(Tetris.tetromino_shapes[tetromino_type], Tetris.tetromino_colors[tetromino_type])

        self.x = (self.w - self.cur_tetromino.size) // 2
        self.y = 0

    def shift_horizontal(self, dx):
        self.x += dx
        if dx < 0:
            for r in range(self.cur_tetromino.size):
                for c in range(self.cur_tetromino.size):
                    if self.cur_tetromino.shape[r][c]:
                        if self.has_collision(self.y + r, self.x + c):
                            self.x -= dx
                            return
                        else:
                            break
        else:
            for r in range(self.cur_tetromino.size):
                for c in range(self.cur_tetromino.size - 1, -1, -1):
                    if self.cur_tetromino.shape[r][c]:
                        if self.has_collision(self.y + r, self.x + c):
                            self.x -= dx
                            return
                        else:
                            break

    def shift_down(self):
        self.y += 1
        for c in range(self.cur_tetromino.size):
            for r in range(self.cur_tetromino.size - 1, -1, -1):
                if self.cur_tetromino.shape[r][c]:
                    if self.has_collision(self.y + r, self.x + c):
                        self.y -= 1
                        self.touch_down()
                        self.init_next_tetromino()
                        return
                    else:
                        break
    
    def touch_down(self):
        dirty_rows = set()
        for r in range(self.cur_tetromino.size):
            for c in range(self.cur_tetromino.size):
                if self.cur_tetromino.shape[r][c]:
                    self.gameboard[self.y + r][self.x + c] = self.cur_tetromino.color
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
        
        if not self.cur_tetromino:
            return

        self.cur_tetromino.rotate_clockwise()
        
        for r in range(self.cur_tetromino.size):
            for c in range(self.cur_tetromino.size):
                if self.cur_tetromino.shape[r][c] and self.has_collision(self.y + r, self.x + c):
                    self.cur_tetromino.rotate_counter_clockwise()
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

        pygame.time.set_timer(self.free_fall_timer_event, self.free_fall_interval)
        
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == self.free_fall_timer_event:
                    self.shift_down()

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

            if self.cur_tetromino:
                for r in range(self.cur_tetromino.size):
                    for c in range(self.cur_tetromino.size):
                        if self.cur_tetromino.shape[r][c]:
                            pygame.draw.rect(
                                screen, 
                                self.cur_tetromino.color, 
                                pygame.Rect(
                                    (self.x + c) * self.block_size, 
                                    (self.y + r) * self.block_size, 
                                    self.block_size, self.block_size
                                )
                            )
            
            for r in range(self.h):
                for c in range(self.w):
                    if self.gameboard[r][c]:
                        pygame.draw.rect(screen, self.gameboard[r][c], grid[r][c])
                    pygame.draw.rect(screen, Tetris.grid_color, grid[r][c], 1)

            pygame.display.flip()

            clock.tick(self.fps)
            
        pygame.quit()

if __name__ == '__main__':
    tetris_game = Tetris()
    tetris_game.run()
