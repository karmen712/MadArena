from pygame import *

from Interface.Background import *
from Interface.Button import *

from GameModes.sandbox_mode import sandbox


def main_menu(game):

    bg = Background(resource_path('Media/Images/Backgrounds/Main_menu_bg.jpg'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)
    screen = game.screen

    sandbox_button = Button([game.WIN_WIDTH/2, game.WIN_HEIGHT/2 - 50], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185), textsize=16, text="Песочница", textfont="Impact", focusbrightness=20, borderwidth=2)
    quit_button = Button([game.WIN_WIDTH/2, game.WIN_HEIGHT/2 + 100], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185), textsize=16, text="Выйти", textfont="Impact", focusbrightness=20, borderwidth=2)

    while 1:  # Основной цикл программы
        if game.state != "MainMenu":
            break
        timer = game.timer
        timer.tick(60)
        pos = pygame.mouse.get_pos()

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit
            if (e.type == QUIT) or (e.type == KEYDOWN and e.key == K_ESCAPE):
                raise SystemExit
            if (e.type == MOUSEBUTTONUP) and (e.button == 1):
                if sandbox_button.rect.collidepoint(pos):
                    game.state = "Sandbox"
                    sandbox(game)
                    break
                if quit_button.rect.collidepoint(pos):
                    raise SystemExit

        screen.blit(bg.image, bg.rect)
        sandbox_button.draw(screen, pos)
        quit_button.draw(screen, pos)

        pygame.display.update()
