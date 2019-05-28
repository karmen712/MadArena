import pygame
from Interface.Background import Background
from GameHUD.game_pause import pause
from System.resoursepath import resource_path
from GameHUD.unit_select_bar import UnitSelectBar
from Interface.Button import Button


def sandbox(game):

    screen = game.screen
    w, h = screen.get_size()
    timer = pygame.time.Clock()
    bg = Background(resource_path('Media/Images/Backgrounds/Sandbox_bg.png'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)
    units = [{'color': (140, 4, 47), 'text': 'human'},
             {'color': (25, 146, 47), 'text': 'hooman'}]

    def draw_buttons(m_pos):
        offset = usb.rect.left + 5
        btn_width = w / 16

        for unit in units:
            btn_pos = offset + (btn_width/2), (usb.rect.top + 5) + ((usb.rect.height - 10)/2)
            btn = Button(btn_pos, btn_width, usb.rect.height - 10,
                         (165, 165, 165), fillcolor=unit['color'], text=unit['text'], focusbrightness=90)

            btn.draw(screen, m_pos)
            offset += (5 + btn_width)

    while 1:  # Основной цикл программы
        timer.tick(100)
        m_pos = pygame.mouse.get_pos()
        if game.state != "Sandbox":
            break
        screen.blit(bg.image, bg.rect)  # Каждую итерацию необходимо всё перерисовывать

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                raise SystemExit
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pause(game)
        usb = UnitSelectBar((w, h))
        usb.draw(screen)
        draw_buttons(m_pos)

        pygame.display.update()
