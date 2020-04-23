from Interface.Background import *
from Interface.Button import *
import System.game_options as options


def options_menu(game):
    from Menus.main_menu import main_menu
    bg = Background(resource_path('Media/Images/Backgrounds/Main_menu_bg.jpg'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)
    screen = game.screen

    show_dmg_num_opt_button = Button([game.WIN_WIDTH / 2, game.WIN_HEIGHT / 2 - 50], 250, 40, (165, 165, 165),
                            fillcolor=(185, 185, 185), textsize=16, text="Цифры урона: скрыть", textfont="Impact",
                            focusbrightness=20, borderwidth=2)

    back_button = Button([game.WIN_WIDTH / 2, game.WIN_HEIGHT / 2 + 150], 250, 40, (165, 165, 165),
                         fillcolor=(185, 185, 185), textsize=16, text="Назад", textfont="Impact", focusbrightness=20,
                         borderwidth=2)

    while 1:
        if game.state != "OptionsMenu":
            break
        if options.show_damage_numbers:
            show_dmg_num_opt_button.text = "Цифры урона: показывать"
        else:
            show_dmg_num_opt_button.text = "Цифры урона: скрыть"

        timer = game.timer
        timer.tick(60)
        pos = pygame.mouse.get_pos()

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit
            if (e.type == QUIT) or (e.type == KEYDOWN and e.key == K_ESCAPE):
                raise SystemExit
            if (e.type == MOUSEBUTTONUP) and (e.button == 1):
                if back_button.rect.collidepoint(pos):
                    game.state = "MainMenu"
                    game.paused = False
                    main_menu(game)
                    break
                if show_dmg_num_opt_button.rect.collidepoint(pos):
                    options.show_damage_numbers = not options.show_damage_numbers

        screen.blit(bg.image, bg.rect)
        back_button.draw(screen, pos)
        show_dmg_num_opt_button.draw(screen, pos)

        pygame.display.update()
