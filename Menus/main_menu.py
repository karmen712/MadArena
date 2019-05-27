from pygame import *

from Interface.Background import *
from Interface.Button import *


def main_menu(game):

    bg = Background(resource_path('Media/Images/Backgrounds/Main_menu_bg.jpg'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)
    screen = game.screen

    BeginButton = Button([game.WIN_WIDTH/2, game.WIN_HEIGHT/2 - 50], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185), textsize=14, text="Песочница", textfont="TimesNewRoman", focusbrightness=20, borderwidth=2)
    #HelpButton = Button([game.WIN_WIDTH/2, game.WIN_HEIGHT/2], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185), textsize=14, text="Помощь", textfont="TimesNewRoman", focusbrightness=20, borderwidth=2)
    #InfoButton = Button([game.WIN_WIDTH/2, game.WIN_HEIGHT/2 + 50], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185), textsize=14, text="Автор", textfont="TimesNewRoman", focusbrightness=20, borderwidth=2)
    QuitButton = Button([game.WIN_WIDTH/2, game.WIN_HEIGHT/2 + 100], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185), textsize=14, text="Выйти", textfont="TimesNewRoman", focusbrightness=20, borderwidth=2)


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
                # if not show_help and not show_info:
                if BeginButton.rect.collidepoint(pos):
                    game.state = "SandBox"
                    # sandbox(game)
                    break
                if QuitButton.rect.collidepoint(pos):
                    raise SystemExit
                    # if HelpButton.rect.collidepoint(pos):
                    #     show_help = not show_help
                    # if InfoButton.rect.collidepoint(pos):
                    #     show_info = not show_info
                else:
                    pass
                    # if show_info:
                    #     show_info = not show_info
                    # if show_help:
                    #     show_help = not show_help

        screen.blit(bg.image, bg.rect)
        BeginButton.draw(screen, pos)
        # HelpButton.draw(screen, pos)
        # InfoButton.draw(screen, pos)
        QuitButton.draw(screen, pos)
        # if show_help:
        #     screen.blit(help_image, (game.WIN_WIDTH/4, game.WIN_HEIGHT/4))
        # if show_info:
        #     screen.blit(info_image, (game.WIN_WIDTH / 9, game.WIN_HEIGHT / 9))
        pygame.display.update()
