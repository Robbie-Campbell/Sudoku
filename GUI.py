import pygame
from logic import solve, game_board
from pygame.locals import (
    MOUSEBUTTONDOWN,
    K_SPACE,
    KEYDOWN,
    K_ESCAPE
)


def main():
    pygame.init()

    w = 60
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Sudoku!")
    screen.fill((40, 40, 40))

    # Create a surface and pass in a tuple containing its length and width
    surf = pygame.Surface((w, w))

    # Give the surface a color to separate it from the background
    surf.fill((240, 240, 240))

    def make_board(game):
        x, y = 6, 6
        for index, row in enumerate(game):
            for value, col in enumerate(row):
                font = pygame.font.SysFont(None, 30)
                number = font.render(str(game[index][value]), True, (0, 0, 0))
                if game[index][value] != 0:
                    surf.fill((255, 255, 255))
                else:
                    surf.fill((255, 255, 255))
                    number = font.render("", True, (0, 0, 0))
                surf.blit(number, (22, 22))
                screen.blit(surf, (x, y))
                x = x + (w+6)
            y = y + (w+6)
            x = 6

    make_board(game_board)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    screen.fill((40, 40, 40))
                    answer = solve()
                    make_board(answer)
            else:
                running = True
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
