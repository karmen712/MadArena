from Interface.Button import Button
import pygame


def pause(game):
    from Menus.main_menu import main_menu

    game.paused = not game.paused
    screen = game.screen

    continuebutton = Button([game.WIN_WIDTH / 2, game.WIN_HEIGHT / 2 - 75], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185),
                            textsize=14, text="Продолжить", textfont="TimesNewRoman", focusbrightness=40, borderwidth=2)
    mmquitbutton = Button([game.WIN_WIDTH / 2, game.WIN_HEIGHT / 2 - 25], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185),
                          textsize=14, text="Главное Меню", textfont="TimesNewRoman", focusbrightness=40, borderwidth=2)
    quitbutton = Button([game.WIN_WIDTH / 2, game.WIN_HEIGHT / 2 + 75], 250, 40, (165, 165, 165), fillcolor=(185, 185, 185),
                        textsize=14, text="Выйти из игры", textfont="TimesNewRoman", focusbrightness=40, borderwidth=2)
    pause_window = pygame.Rect(game.WIN_WIDTH / 2, game.WIN_HEIGHT / 2, game.WIN_WIDTH / 3, game.WIN_HEIGHT / 2.6)
    pause_window.center = (game.WIN_WIDTH / 2, game.WIN_HEIGHT / 2)

    while game.paused:
        pos = pygame.mouse.get_pos()
        game.timer.tick(60)
        pygame.draw.rect(screen, (125, 225, 125), pause_window, 0)
        continuebutton.draw(screen, pos)
        mmquitbutton.draw(screen, pos)
        quitbutton.draw(screen, pos)

        for ev in pygame.event.get():  # Обрабатываем события
            if ev.type == pygame.QUIT:
                raise SystemExit
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                game.paused = False
                pygame.mouse.set_visible(False)
            if (ev.type == pygame.MOUSEBUTTONUP) and (ev.button == 1):
                if quitbutton.rect.collidepoint(pos):
                    raise SystemExit
                if continuebutton.rect.collidepoint(pos):
                    game.paused = False
                if mmquitbutton.rect.collidepoint(pos):
                    game.state = "MainMenu"
                    game.paused = False
                    main_menu(game)

        pygame.display.update()
