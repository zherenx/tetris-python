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

    background_color = (40, 40, 40)

    normal_text_color = (255, 255, 255)

    def __init__(self, height=20, width=10, block_size=32, fps=60) -> None:

        self.h = height
        self.w = width
        self.block_size = block_size

        self.fps = fps

        self.reset_game()
    
    def reset_game(self):
        self.gameboard = [[0] * self.w for _ in range(self.h)]

        self.cur_tetromino = None
        self.x = 0
        self.y = 0

        self.next_tetromino = None
        self.update_next_tetromino()
        self.update_tetromino()

        self.score = 0
        self.free_fall_interval = 1000 # TODO: update when level up

        self.game_over = False

    def update_tetromino(self):
        self.cur_tetromino = self.next_tetromino
        self.x = (self.w - self.cur_tetromino.size) // 2
        self.y = 0

        self.update_next_tetromino()

        if self.has_collision_cur_tetromino():
            self.game_over = True
    
    def update_next_tetromino(self):
        tetromino_type = random.randint(0, len(Tetris.tetromino_shapes) - 1)
        self.next_tetromino = Tetromino(
            Tetris.tetromino_shapes[tetromino_type], Tetris.tetromino_colors[tetromino_type]
        )

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
                        self.update_tetromino()
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

        # TODO: update score calculation logic
        self.score += num_completed_lines * 100
    
    def clear_line(self, row):
        del self.gameboard[row]
        self.gameboard = [[0] * self.w] + self.gameboard

    def rotate(self):
        if not self.cur_tetromino:
            return
        self.cur_tetromino.rotate_clockwise()
        if self.has_collision_cur_tetromino():
            self.cur_tetromino.rotate_counter_clockwise()
    
    # check collision for cur tetromino
    def has_collision_cur_tetromino(self):
        for r in range(self.cur_tetromino.size):
            for c in range(self.cur_tetromino.size):
                if self.cur_tetromino.shape[r][c] and self.has_collision(self.y + r, self.x + c):
                    return True
        return False
    
    # check collision for one block
    def has_collision(self, r, c):
        if c < 0 or c >= self.w or r >= self.h or self.gameboard[r][c]:
            return True
        return False

    def run(self):

        def get_x_offset_for_centering(main_surface, blit_surface):
            return (main_surface.get_size()[0] - blit_surface.get_size()[0]) // 2
        
        def draw_tetromino(surface, tetromino, x, y, block_size, 
                           draw_border=True, border_color=Tetris.background_color):
            for r in range(tetromino.size):
                for c in range(tetromino.size):
                    if tetromino.shape[r][c]:
                        rect = pygame.Rect(x + c * block_size, 
                                           y + r * block_size, 
                                           block_size, block_size)
                        pygame.draw.rect(surface, tetromino.color, rect)
                        if draw_border:
                            pygame.draw.rect(surface, border_color, rect, 1)

        game_screen_res = self.block_size * self.w, self.block_size * self.h
        info_screen_res = self.block_size * 6, self.block_size * self.h
        preview_screen_res = self.block_size * 5, self.block_size * 5

        main_screen_margin = self.block_size // 2
        main_screen_res = (
            game_screen_res[0] + info_screen_res[0] + main_screen_margin * 3,
            game_screen_res[1] + main_screen_margin * 2,
        )

        game_over_screen_res = main_screen_res[0] // 2, main_screen_res[1] // 2

        game_screen_offset = (main_screen_margin, main_screen_margin)
        info_screen_offset = (main_screen_margin * 2 + game_screen_res[0], main_screen_margin)
        game_over_screen_offset = (
            (main_screen_res[0] - game_over_screen_res[0]) // 2, 
            (main_screen_res[1] - game_over_screen_res[1]) // 2
        )

        pygame.init()

        # main_screen: (game_screen, info_screen: (title, score, preview_screen))
        main_screen = pygame.display.set_mode(main_screen_res)
        main_screen.fill(Tetris.background_color)

        game_screen = pygame.Surface(game_screen_res)
        info_screen = pygame.Surface(info_screen_res)
        preview_screen = pygame.Surface(preview_screen_res)
        
        game_over_background = pygame.Surface(main_screen_res)
        game_over_background.set_alpha(10)
        game_over_background.fill(Tetris.background_color)
        game_over_screen = pygame.Surface(game_over_screen_res)

        title_font = pygame.font.SysFont("Calibri", self.block_size)
        normal_text_font = pygame.font.SysFont("Calibri", self.block_size // 2)

        title = title_font.render("TETRIS", False, (255, 0, 0))
        
        # precompute offset respect to info screen
        title_offset_to_info_screen = (
            get_x_offset_for_centering(info_screen, title), self.block_size
        )
        score_text_offset_to_info_screen_y = title_offset_to_info_screen[1] + self.block_size * 2
        preview_screen_offset_to_info_screen = (
            get_x_offset_for_centering(info_screen, preview_screen), 
            score_text_offset_to_info_screen_y + self.block_size * 3
        )
        option_text_offset_to_info_screen_y = \
            preview_screen_offset_to_info_screen[1] + preview_screen_res[1] + self.block_size * 2

        # precompute offset respect to game over screen
        title_offset_to_game_over_screen = (
            get_x_offset_for_centering(game_over_screen, title), self.block_size
        )
        score_text_offset_to_game_over_screen_y = \
            title_offset_to_game_over_screen[1] + self.block_size * 2
        option_text_offset_to_game_over_screen_y = \
            score_text_offset_to_game_over_screen_y + self.block_size * 3

        grid = [[pygame.Rect(c * self.block_size, r * self.block_size, self.block_size, self.block_size) for c in range(self.w)] for r in range(self.h)]

        clock = pygame.time.Clock()
        running = True

        free_fall_timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(free_fall_timer_event, self.free_fall_interval)

        # This variable is for updating the game one more time (to show 
        # the collided piece) before showing the game over page.
        # There might be better way of doing it...
        last_frame_drawn = False
        
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.reset_game()

                if not self.game_over:
                    if event.type == free_fall_timer_event:
                        self.shift_down()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.shift_horizontal(-1)
                        elif event.key == pygame.K_RIGHT:
                            self.shift_horizontal(1)
                        elif event.key == pygame.K_DOWN:
                            self.shift_down()
                        elif event.key == pygame.K_UP:
                            self.rotate()

            if self.game_over and last_frame_drawn:

                # TODO: draw the last piece on gameboard

                main_screen.blit(game_over_background, (0, 0))
                # pygame.draw.rect(main_screen, (40, 40, 40, 10), (0, 0, main_screen.get_size()[0], main_screen.get_size()[1]))
                # main_screen.fill((40, 40, 40, 10))

                game_over_screen.blit(title, title_offset_to_game_over_screen)
                
                score_text = normal_text_font.render(f"Your Score: {self.score}", False, Tetris.normal_text_color)
                game_over_screen.blit(score_text, (get_x_offset_for_centering(game_over_screen, score_text), score_text_offset_to_game_over_screen_y))

                option_text = normal_text_font.render(f"'R' to restart, 'Esc' to exit", False, Tetris.normal_text_color)
                game_over_screen.blit(option_text, (get_x_offset_for_centering(game_over_screen, option_text), option_text_offset_to_game_over_screen_y))

                main_screen.blit(game_over_screen, game_over_screen_offset)
            
            else:

                # update game screen
                game_screen.fill("black")

                for r in range(self.h):
                    for c in range(self.w):
                        if self.gameboard[r][c]:
                            pygame.draw.rect(game_screen, self.gameboard[r][c], grid[r][c])
                        pygame.draw.rect(game_screen, Tetris.background_color, grid[r][c], 1)

                if self.cur_tetromino:
                    draw_tetromino(
                        game_screen, 
                        self.cur_tetromino, 
                        self.x * self.block_size, 
                        self.y * self.block_size, 
                        self.block_size
                    )

                # update info screen
                info_screen.fill(Tetris.background_color)

                info_screen.blit(title, title_offset_to_info_screen)

                score_text = normal_text_font.render(f"Score: {self.score}", False, Tetris.normal_text_color)
                info_screen.blit(score_text, (get_x_offset_for_centering(info_screen, score_text), score_text_offset_to_info_screen_y))

                preview_screen.fill('black')
                next_text = normal_text_font.render("Next:", False, (255, 255, 255))
                preview_screen.blit(next_text, (self.block_size // 8, self.block_size // 8))
                tetromino_offset = (
                    (preview_screen_res[0] - self.next_tetromino.size * self.block_size) // 2,
                    (preview_screen_res[1] - self.next_tetromino.size * self.block_size) // 2 + self.block_size // 2
                )
                draw_tetromino(
                    preview_screen, 
                    self.next_tetromino, 
                    tetromino_offset[0], 
                    tetromino_offset[1], 
                    self.block_size
                )

                info_screen.blit(preview_screen, preview_screen_offset_to_info_screen)

                option_text = normal_text_font.render(f"'R' to restart, 'Esc' to exit", False, Tetris.normal_text_color)
                info_screen.blit(option_text,(get_x_offset_for_centering(info_screen, option_text), option_text_offset_to_info_screen_y))

                main_screen.blit(game_screen, game_screen_offset)
                main_screen.blit(info_screen, info_screen_offset)

                if self.game_over:
                    last_frame_drawn = True

            pygame.display.flip()

            clock.tick(self.fps)
            
        pygame.quit()

if __name__ == '__main__':
    tetris_game = Tetris()
    tetris_game.run()
