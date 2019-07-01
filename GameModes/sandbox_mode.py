import pygame
from Interface.Background import Background
from GameHUD.game_pause import pause
from System.resoursepath import resource_path
from GameHUD.unit_select_bar import UnitSelectBar
from Interface.Button import Button
from Units.Human import Human
from Units.Skeleton import skeleton
import random
import math
from System.MyPhysics import Physics
from Menus.options import *
from Units.Hoblin.Archer.Hoblin_archer import HoblinArcher
from Units.Special.arena_cleaners import MeatHoover
from  Effects.static_effects import BloodSplat


def sandbox(game):

    screen = game.screen
    w, h = screen.get_size()
    #timer = pygame.time.Clock()
    bg = Background(resource_path('Media/Images/Backgrounds/Sandbox_bg.png'), [0, 0], game.WIN_WIDTH, game.WIN_HEIGHT)
    available_units = [{'color': (140, 100, 95), 'text': 'human', 'unit': 'human'},
                       {'color': (163, 164, 167), 'text': 'skeleton', 'unit': 'skeleton'},
                       {'color': (60, 164, 67), 'text': 'hoblin archer', 'unit': 'hoblin archer'},
                       ]
    phys = Physics(friction, gravity)
    units = []
    effects = []
    sel_units = []
    drag = False
    dragged = None
    selecting = False
    u_btns = []
    usb = UnitSelectBar((w, h))
    player_team = 1
    second = 0
    random.seed()
    sel_rect = pygame.Rect(0, 0, 0, 0)
    sel_pos_start = (0, 0)
    sea_border_y = game.WIN_HEIGHT * 0.5
    # transparent_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    auto_spawn_switch = Button(usb.rect.midbottom, 120, 20, (165, 165, 165), fillcolor=(185, 185, 185), centered=False,
                               textsize=12, text="Автоспавн: выкл.", textfont="TimesNewRoman", focusbrightness=40, borderwidth=2)
    auto_spawn = False

    offset = usb.rect.left + 5
    btn_width = w / 16
    unit_classes = [Human.Human, skeleton.Skeleton, HoblinArcher]
    current_team = 1
    team_select_switch = Button(usb.rect.bottomleft, 120, 20, (165, 165, 165), fillcolor=team_colors[current_team], centered=False,
                                textsize=12, text="Команда:1", textfont="TimesNewRoman", focusbrightness=40, borderwidth=2)
    clean_arena_button = Button((team_select_switch.rect.topright[0] + 20, team_select_switch.rect.topright[1]), 120, 20, (165, 165, 165), fillcolor=(70, 150, 150), centered=False,
                                textsize=12, text="Очистить", textfont="TimesNewRoman", focusbrightness=40, borderwidth=2)
    arena_cleaning = False
    arena_cleaner = None

    for a_unit in available_units:
        btn_pos = offset + (btn_width / 2), (usb.rect.top + 5) + ((usb.rect.height - 10) / 2)
        btn = Button(btn_pos, btn_width, usb.rect.height - 10, (165, 165, 165), fillcolor=a_unit['color'],
                     text=a_unit['text'], focusbrightness=90, data=(a_unit['unit']))
        u_btns.append(btn)
        offset += (5 + btn_width)

    def create_unit(unit_to_create, pos, team):
        lcu = unit_to_create(pos, "stand", team)
        lcu.id = len(units)
        units.append(lcu)

    def draw_buttons():
        auto_spawn_switch.draw(screen, m_pos)
        team_select_switch.draw(screen, m_pos)
        clean_arena_button.draw(screen, m_pos)
        for u_bt in u_btns:
            u_bt.draw(screen, m_pos)

    def draw_effects():
        for effect in effects:
            effect.draw(screen)

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
            return u.state in ["stand", "attack_move"]
        if action == "be_attacked":
            return u.state in ["stand", "moving", "falling", "stunned", "attack"]
        if action == "collide":
            return u.state in ["stand", "moving", "falling", "stunned", "attack_move", "attack"]

    def get_distance(pos1, pos2):
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

    def get_unit_from_button(btn_data):
        if btn_data == 'human':
            return Human.Human(m_pos, "drag", current_team)
        elif btn_data == 'skeleton':
            return skeleton.Skeleton(m_pos, "drag", current_team)
        elif btn_data == 'hoblin archer':
            return HoblinArcher(m_pos, "drag", current_team)

    while 1:  # Основной цикл программы
        if game.state != "Sandbox":
            break
        pygame.time.wait(milliseconds)
        second += milliseconds
        m_pos = pygame.mouse.get_pos()

        screen.blit(bg.image, bg.rect)  # Каждую итерацию необходимо всё перерисовывать
        usb.draw(screen)
        draw_buttons()
        draw_effects()

        if selecting:
            sel_rect.topleft = sel_pos_start
            sel_rect.width = m_pos[0] - sel_pos_start[0]
            sel_rect.height = m_pos[1] - sel_pos_start[1]
            pygame.draw.rect(screen, (30, 200, 10), sel_rect, 1)
        if drag:
            dragged.move_ip(m_pos)
        if arena_cleaning:
            arena_cleaner.draw(screen)
            mx, my = arena_cleaner.collector_rect.center
            for du in units:
                if du.rect.colliderect(arena_cleaner.collector_rect):
                    if du.hp > 0:
                        arena_cleaner.deal_damage(du)
                    else:
                        units.remove(du)
                        effects.append(BloodSplat(du.rect.midbottom))
                        del du
                else:
                    dist = get_distance(arena_cleaner.collector_rect.center, du.rect.center)
                    sp = arena_cleaner.seeking_speed
                    dd = sp / dist
                    dx, dy = dd * (mx - du.rect.center[0]), dd * (my - du.rect.center[1])

                    du.rect.move_ip(dx, dy)

            if game.WIN_WIDTH < arena_cleaner.rect.center[0] or arena_cleaner.rect.center[0] < 0:
                clean_arena_button.text = "Очистить"
                clean_arena_button.fillcolor = (70, 150, 150)
                arena_cleaning = False
                del arena_cleaner

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
                        if sea_border_y > dragged.half_rect.center[1]:
                            dragged.z = sea_border_y - dragged.half_rect.center[1]
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
                            if unit.half_rect.colliderect(sel_rect) and unit.team == player_team:
                                unit.selected = True
                                sel_units.append(unit)
                    else:
                        clear_selection()
                if e.button == 3:
                    if m_pos[1] > sea_border_y:
                        if len(sel_units) > 0:
                            formation_order = 0
                            frmt_sighn = 1
                            if len(sel_units) == 1:
                                sel_units[0].target = m_pos
                            for sel_unit in sel_units:
                                sel_unit.attack_target = None
                                frmt_sighn = frmt_sighn * -1
                                sel_unit.target = (m_pos[0]+random.randint(1, 7), m_pos[1]+(formation_order*frmt_sighn))
                                formation_order += random.randint(1, 7) + sel_unit.body_height
                                for uni in units:
                                    if uni.team != player_team:
                                        if uni.half_rect.collidepoint(m_pos):
                                            pygame.draw.ellipse(screen, team_colors[uni.team], uni.half_rect, 0)
                                            sel_unit.attack_target = uni
                                            sel_unit.find_point_to_attack(order=True)
            if (e.type == pygame.MOUSEBUTTONDOWN) and (e.button == 1):
                if usb.rect.collidepoint(m_pos):
                    for u_btn in u_btns:
                        if u_btn.fillrect.collidepoint(m_pos):
                            drag = True
                            dragged = get_unit_from_button(u_btn.data)
                            dragged.id = len(units)
                            units.append(dragged)
                elif auto_spawn_switch.rect.collidepoint(m_pos):
                    clear_selection()
                    if auto_spawn:
                        auto_spawn_switch.text = "Автоспавн: выкл."
                        auto_spawn = False
                    else:
                        auto_spawn_switch.text = "Автоспавн: вкл."
                        auto_spawn = True
                elif team_select_switch.rect.collidepoint(m_pos):
                    clear_selection()
                    if current_team < len(team_colors):
                        current_team += 1
                    else:
                        current_team = 1
                    team_select_switch.text = team_select_switch.text[0:7] + str(current_team)
                    team_select_switch.fillcolor = team_colors[current_team]
                    player_team = current_team
                elif clean_arena_button.rect.collidepoint(m_pos):
                    if not arena_cleaning:
                        clean_arena_button.text = "Очистка"
                        clean_arena_button.fillcolor = (120, 120, 120)
                        arena_cleaning = True
                        arena_cleaner = MeatHoover((game.WIN_WIDTH - 80, ((game.WIN_HEIGHT - sea_border_y)/2)+(game.WIN_HEIGHT - sea_border_y)))
                        if random.randint(1, 2) == 2:
                            arena_cleaner.dir = 1
                            arena_cleaner.speed = 4
                            arena_cleaner.rect.x = 0
                elif not selecting:
                    selecting = True
                    sel_pos_start = m_pos
        # endregion
        if second == 250:
            second = 0
            sort_units()
            if auto_spawn:
                create_unit(unit_classes[random.randint(0, len(unit_classes)-1)], (random.randint(10, game.WIN_WIDTH),
                            random.randint(sea_border_y, game.WIN_HEIGHT)), random.randint(1, len(team_colors)))
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
            if unit.state != "dead":
                screen.blit(game.font.render(str(unit.state), False, (55, 55, 55)), (unit.rect.topleft[0], unit.rect.topleft[1] - 30))
                screen.blit(game.font.render(str(unit.hp), False, (55, 55, 55)), (unit.rect.topleft[0] - 10, unit.rect.topleft[1] - 20))
        pygame.display.update()
