import pygame, random
from pygments.styles.dracula import background

from engine.engine import Engine
from engine.systems.button_system import ButtonSystem
from engine.systems.draw_system import DrawSystem
from engine.widgets.box import Box
from engine.widgets.button import Button
from engine.widgets.positioned import Positioned
from engine.widgets.text import Text
from game.scenes.main_menu import MainMenuScene


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    engine = Engine("Sudoku", (WINDOW_WIDTH, WINDOW_HEIGHT))

    WHITE = pygame.Color(255, 255, 255)
    welcome_font = pygame.font.Font(None, 80)
    gm_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 48)

    scene = MainMenuScene([
        DrawSystem([
            Positioned(
                position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4),
                child=Text("Welcome to Sudoku!", WHITE, welcome_font)
            ),
            Positioned(
                position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3),
                child=Text("Select Game Mode:", WHITE, gm_font)
            ),
        ]),
        ButtonSystem([
           Button(
               position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
               on_click=lambda: None,
               foreground=Text("Easy", WHITE, button_font),
               background=Box((200, 250), color=WHITE),
               size=(200, 250)
           )
        ]),
    ])
    engine.load_scene(scene)

    engine.main_loop()
    engine.dispose()

    return

    # Initialize screen
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku")


    # Fill background option 1
    background_image = pygame.image.load('Sudoku_BG.jpg')
    background_image = pygame.transform.scale(background_image,(1280,720))

    # Fill background option 2
    lines = [[random.uniform(0,SCREEN_WIDTH), random.uniform(-SCREEN_HEIGHT,SCREEN_HEIGHT)] for i in range(50)]

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    PURPLE = (128,0,128)


    # Welcome text
    welcome_font = pygame.font.Font(None, 80)
    welcome_text = welcome_font.render("Welcome to Sudoku!",1,WHITE)
    welcome_textpos = welcome_text.get_rect()
    welcome_textpos.centerx = screen.get_rect().centerx
    welcome_textpos.centery = 200


    # Select game mode text gm_text == gamemodetext
    gm_font = pygame.font.Font(None, 50)
    gm_text = gm_font.render("Select Game Mode:",1,WHITE)
    gm_textpos = gm_text.get_rect()
    gm_textpos.centerx = screen.get_rect().centerx
    gm_textpos.centery = 350

    # default font for button text
    button_font = pygame.font.Font(None, 48)

    # easy
    easy_rect = pygame.Rect(300,250,320,500)
    easy_text = button_font.render("Easy",1,WHITE)
    easy_button = easy_text.get_rect(center=easy_rect.center)

    # medium
    medium_rect = pygame.Rect(300, 250, 640, 500)
    medium_text = button_font.render("Medium", 1, WHITE)
    medium_button = medium_text.get_rect(center=medium_rect.center)

    # hard
    hard_rect = pygame.Rect(300, 250, 960, 500)
    hard_text = button_font.render("Hard", 1, WHITE)
    hard_button = hard_text.get_rect(center=hard_rect.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if easy_button.collidepoint(mouse_x,mouse_y):
                    print("Easy button pressed!")
                if medium_button.collidepoint(mouse_x,mouse_y):
                    print("Medium button pressed!")
                if hard_button.collidepoint(mouse_x,mouse_y):
                    print("Hard button pressed!")

        # cool purple animated background
        screen.fill(BLACK)
        for line in lines:
            pygame.draw.line(screen, PURPLE, (line[0], line[1]), (line[0], line[1] + 50), 2)
            line[1] += .5
            if line[1] > SCREEN_HEIGHT:
                line[1] = random.randint(-100, 0)

        # placing everything on the screen
        screen.blit(welcome_text, welcome_textpos)
        screen.blit(gm_text,gm_textpos)
        pygame.draw.rect(screen,PURPLE,easy_button)
        screen.blit(easy_text,easy_button)
        pygame.draw.rect(screen, PURPLE, medium_button)
        screen.blit(medium_text,medium_button)
        pygame.draw.rect(screen, PURPLE, hard_button)
        screen.blit(hard_text,hard_button)
        pygame.display.flip()

if __name__ == "__main__":
    main()

