import pygame
from Interface.Background import Background
from GameHUD.game_pause import pause
from System.resoursepath import resource_path
from GameHUD.unit_select_bar import UnitSelectBar
from Interface.Button import Button
from Units.Human import Human
import random
import math
from System.MyPhysics import Physics
from Menus.options import *


def sandbox(game):

    screen = game.screen
    w, h = screen.get_size()
    #timer = pygame.time.Clock()
    bg = Background(resource_path('Media/Images/Backgrounds/Sandbox_bg.png'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)
    available_units = [{'color': (25, 146, 47), 'text': 'hooman', 'team': 1},
                       {'color': (140, 4, 47), 'text': 'human', 'team': 2}
                       ]
    phys = Physics(friction, gravity)
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
    sea_border_y = game.WIN_HEIGHT * 0.5
    # transparent_surface = pygame.Surface((w, h), pygame.SRCALPHA)

    offset = usb.rect.left + 5
    btn_width = w / 16

    for a_unit in available_units:
        btn_pos = offset + (btn_width / 2), (usb.rect.top + 5) + ((usb.rect.height - 10) / 2)
        btn = Button(btn_pos, btn_width, usb.rect.height - 10, (165, 165, 165), fillcolor=a_unit['color'],
                     text=a_unit['text'], focusbrightness=90, data=a_unit['team'])
        u_btns.append(btn)
        offset += (5 + btn_width)

    def draw_buttons():
        for u_bt in u_btns:
            u_bt.draw(screen, m_pos)

    def sort_units():
        def sort_by_y(val):
            return val.half_rect.y
        units.sort(key=sort_by_y)

    def clear_selection():
        for s_unit in sel_units:
            s_unit.selected = False
        sel_units.clear()

    def get_unit_by_id(uid):
        for un in units:
            if uid == un.id:
                return un

    def unit_able_to(u, action):
        if action == "attack":
            return u.state in ["stand", "attack_move"] and u.attack_target is None
        if action == "be_attacked":
            return u.state in ["stand", "moving", "falling", "stunned", "attack"]
        if action == "collide":
            return u.state in ["stand", "moving", "falling", "stunned", "attack_move", "attack"]

    def get_distance(pos1, pos2):
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

    while 1:  # Основной цикл программы
        if game.state != "Sandbox":
            break
        pygame.time.wait(milliseconds)
        second += milliseconds
        m_pos = pygame.mouse.get_pos()

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
        # region EVENT DETECTION ---------------------------------------------------------------------------------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pause(game)
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    if drag:
                        drag = False
                        dragged.move_ip(m_pos)
                        if sea_border_y > m_pos[1]:
                            dragged.z = sea_border_y - m_pos[1] + dragged.rect.height
                            dragged.state = "falling"
                        else:
                            dragged.state = "stand"
                            dragged.target = dragged.rect.midbottom
                        dragged = None
                    elif selecting:
                        selecting = False
                        clear_selection()
                        sel_rect.normalize()
                        for unit in units:
                            if unit.rect.colliderect(sel_rect) and unit.team == 1:
                                unit.selected = True
                                sel_units.append(unit)
                    else:
                        clear_selection()
                if e.button == 3:
                    if m_pos[1] > sea_border_y:
                        formation_order = 0
                        frmt_sighn = 1
                        if len(sel_units) == 1:
                            sel_units[0].target = m_pos
                        for sel_unit in sel_units:
                            sel_unit.attack_target = None
                            frmt_sighn = frmt_sighn * -1
                            sel_unit.target = (m_pos[0]+random.randint(1, 7), m_pos[1]+(formation_order*frmt_sighn))
                            formation_order += random.randint(1, 7) + sel_unit.body_height
            if (e.type == pygame.MOUSEBUTTONDOWN) and (e.button == 1):
                if usb.rect.collidepoint(m_pos):
                    for u_btn in u_btns:
                        if u_btn.fillrect.collidepoint(m_pos):
                            drag = True
                            dragged = Human.Human(m_pos, 100, "drag", u_btn.data)
                            dragged.id = len(units)
                            units.append(dragged)
                elif not selecting:
                    selecting = True
                    sel_pos_start = m_pos
        # endregion
        if second == 250:
            second = 0
            sort_units()
        for unit in units:
            unit.draw(screen)
            phys.border_intersect(unit, sea_border_y, game.WIN_WIDTH, game.WIN_HEIGHT)
            phys.speed_regulation(unit)

            attack_targets = []
            if unit_able_to(unit, "attack"):
                for unit2 in units:
                    if unit.id == unit2.id or unit.team == unit2.team:
                        continue
                    if unit_able_to(unit2, "be_attacked") and get_distance(unit.rect.midbottom, unit2.rect.midbottom) < unit.enemy_detect_range:
                        attack_targets.append(unit2)

            if len(attack_targets) > 1:
                min_dist = unit.enemy_detect_range
                for tr in attack_targets:
                    dist = get_distance(unit.rect.midbottom, tr.rect.midbottom)
                    if dist < min_dist:
                        min_dist = dist
                        unit.attack_target = tr
            elif len(attack_targets) == 1:
                unit.attack_target = attack_targets[0]

            for unit2 in units:
                if unit.id == unit2.id or not unit_able_to(unit, "collide"):
                    continue
                if unit.half_rect.colliderect(unit2.half_rect) and unit_able_to(unit, "collide") and unit_able_to(unit2, "collide"):
                    phys.collide_units(unit, unit2)
            screen.blit(game.font.render(str(unit.state), False, (155, 55, 55)), (unit.rect.topleft[0], unit.rect.topleft[1] - 30))
            screen.blit(game.font.render(str(unit.hp), False, (55, 55, 55)), (unit.rect.topleft[0] - 20, unit.rect.topleft[1] - 10))
        pygame.display.update()
