import pygame
from Interface.Background import Background
from GameHUD.game_pause import pause
from System.resoursepath import resource_path
from GameHUD.unit_select_bar import UnitSelectBar
from Interface.Button import Button
from Units.Human import Human
import random


def sandbox(game):

    screen = game.screen
    w, h = screen.get_size()
    timer = pygame.time.Clock()
    bg = Background(resource_path('Media/Images/Backgrounds/Sandbox_bg.png'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)
    available_units = [{'color': (140, 4, 47), 'text': 'human'},
             {'color': (25, 146, 47), 'text': 'hooman'}]

    units = []
    drag = False
    dragged = None
    u_btns = []
    usb = UnitSelectBar((w, h))
    second = 0
    random.seed(a='4x4x4x4x')

    offset = usb.rect.left + 5
    btn_width = w / 16

    for a_unit in available_units:
        btn_pos = offset + (btn_width / 2), (usb.rect.top + 5) + ((usb.rect.height - 10) / 2)
        btn = Button(btn_pos, btn_width, usb.rect.height - 10,
                     (165, 165, 165), fillcolor=a_unit['color'], text=a_unit['text'], focusbrightness=90)
        u_btns.append(btn)
        offset += (5 + btn_width)

    def draw_buttons():
        for u_btn in u_btns:
            u_btn.draw(screen, m_pos)

    def sort_units():
        def sort_by_y(val):
            return val.rect.y
        units.sort(key=sort_by_y)

    while 1:  # Основной цикл программы
        timer.tick(100)
        second += 100
        m_pos = pygame.mouse.get_pos()
        if game.state != "Sandbox":
            break
        screen.blit(bg.image, bg.rect)  # Каждую итерацию необходимо всё перерисовывать

        usb.draw(screen)
        draw_buttons()

        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                raise SystemExit
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pause(game)
            if e.type == pygame.MOUSEBUTTONUP:
                if drag:
                    drag = False
                    dragged.state = "alive"
                    dragged.move_ip(m_pos)
                    dragged = None

            if (e.type == pygame.MOUSEBUTTONDOWN) and (e.button == 1):
                if usb.rect.collidepoint(m_pos):
                    for u_btn in u_btns:
                        if u_btn.fillrect.collidepoint(m_pos):
                            drag = True
                            dragged = Human(m_pos, 100, "drag")
                            units.append(dragged)
                if m_pos[1] > game.WIN_HEIGHT * 0.6875:
                    lucky = random.choice(units)
                    lucky.target = m_pos
        if dragged is not None:
            dragged.draw(screen)
        if second == 1000:
            second = 0
            sort_units()
        for unit in units:
            unit.draw(screen)
        pygame.display.update()
