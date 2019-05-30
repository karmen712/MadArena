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
    available_units = [{'color': (25, 146, 47), 'text': 'hooman', 'team': 1},
                       {'color': (140, 4, 47), 'text': 'human', 'team': 2}
                       ]
    units = []
    sel_units = []
    drag = False
    dragged = None
    selecting = False
    u_btns = []
    usb = UnitSelectBar((w, h))
    second = 0
    random.seed(a='4x4x4x4x')
    sel_rect = pygame.Rect(0, 0, 0, 0)
    sel_pos_start = (0, 0)

    offset = usb.rect.left + 5
    btn_width = w / 16

    for a_unit in available_units:
        btn_pos = offset + (btn_width / 2), (usb.rect.top + 5) + ((usb.rect.height - 10) / 2)
        btn = Button(btn_pos, btn_width, usb.rect.height - 10, (165, 165, 165), fillcolor=a_unit['color'],
                     text=a_unit['text'], focusbrightness=90, data=a_unit['team'])
        u_btns.append(btn)
        offset += (5 + btn_width)

    def draw_buttons():
        for u_btn in u_btns:
            u_btn.draw(screen, m_pos)

    def sort_units():
        def sort_by_y(val):
            return val.half_rect.y
        units.sort(key=sort_by_y)

    def clear_selection():
        for s_unit in sel_units:
            s_unit.selected = False
        sel_units.clear()

    while 1:  # Основной цикл программы
        timer.tick(100)
        second += 100
        m_pos = pygame.mouse.get_pos()
        if game.state != "Sandbox":
            break
        screen.blit(bg.image, bg.rect)  # Каждую итерацию необходимо всё перерисовывать

        usb.draw(screen)
        draw_buttons()
        if selecting:
            sel_rect.topleft = sel_pos_start
            sel_rect.width = m_pos[0] - sel_pos_start[0]
            sel_rect.height = m_pos[1] - sel_pos_start[1]
            pygame.draw.rect(screen, (30, 200, 10), sel_rect, 1)
        if drag:
            dragged.move_ip(m_pos)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                raise SystemExit
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pause(game)
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    if drag:
                        drag = False
                        dragged.state = "stand"
                        dragged.move_ip(m_pos)
                        dragged.target = dragged.rect.midbottom
                        dragged = None
                    elif selecting:
                        selecting = False
                        clear_selection()
                        for unit in units:
                            if unit.rect.colliderect(sel_rect) and unit.team == 1:
                                unit.selected = True
                                sel_units.append(unit)
                    else:
                        pass
                        clear_selection()
                if e.button == 3:
                    if m_pos[1] > game.WIN_HEIGHT * 0.6875:
                        formation_order = 0
                        for sel_unit in sel_units:
                            sel_unit.target = (m_pos[0]+random.randint(1, 7), m_pos[1]+formation_order)
                            formation_order += random.randint(1, 7) + sel_unit.body_height
            if (e.type == pygame.MOUSEBUTTONDOWN) and (e.button == 1):
                if usb.rect.collidepoint(m_pos):
                    for u_btn in u_btns:
                        if u_btn.fillrect.collidepoint(m_pos):
                            drag = True
                            dragged = Human(m_pos, 100, "drag", u_btn.data)
                            dragged.id = len(units)
                            units.append(dragged)
                elif not selecting:
                    selecting = True
                    sel_pos_start = m_pos
        if second == 1000:
            second = 0
            sort_units()
        for unit in units:
            unit.draw(screen)
            screen.blit(game.font.render(unit.state, False, (155, 55, 55)), (unit.rect.topleft[0], unit.rect.topleft[1]-10))
            for unit2 in units:
                if unit.id == unit2.id:
                    continue
                if unit.half_rect.colliderect(unit2.half_rect):
                    if unit.half_rect.center[0] > unit2.half_rect.center[0]:
                        unit.rect.x += 1
                        unit2.rect.x -= 1
                    else:
                        unit.rect.x -= 1
                        unit2.rect.x += 1
                    if unit.half_rect.center[1] > unit2.half_rect.center[1]:
                        unit.rect.y += 1
                        unit2.rect.y -= 1
                    else:
                        unit.rect.y -= 1
                        unit2.rect.y += 1
        pygame.display.update()
