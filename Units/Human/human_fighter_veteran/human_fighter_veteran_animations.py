from System.resoursepath import resource_path
from pygame import image, transform
import pyganim
import random


class HumanFighterVeteranAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_pic = [(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand1.png"), 1700),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand2.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand3.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand4.png"), 400),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand5.png"), 800),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand6.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand7.png"), 1200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand6.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand5.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand4.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand3.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand2.png"), 200),
                          (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Stand/human_veteran_stand1.png"), 1500)]

        self.Walk_pic = [(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Walk/human_veteran_walk1.png"), 100),
                         (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Walk/human_veteran_walk2.png"), 100),
                         (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Walk/human_veteran_walk3.png"), 100),
                         (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Walk/human_veteran_walk4.png"), 100),
                         (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Walk/human_veteran_walk5.png"), 100),
                         (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Walk/human_veteran_walk6.png"), 100)]

        self.Attack1_pic = [(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack1/human_veteran_attack1.png"), 140),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack1/human_veteran_attack2.png"), 140),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack1/human_veteran_attack3.png"), 340),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack1/human_veteran_attack4.png"), 140),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack1/human_veteran_attack5.png"), 340),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack1/human_veteran_attack6.png"), 140)]

        self.Attack2_pic = [(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack2/human_veteran_attack1.png"), 168),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack2/human_veteran_attack2.png"), 168),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack2/human_veteran_attack3.png"), 368),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack2/human_veteran_attack4.png"), 168),
                            (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Attack/Attack2/human_veteran_attack5.png"), 368)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Drag/human_veteran_drag1.png"), 350),
                         (resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/Drag/human_veteran_drag2.png"), 350)]

        self.Attack1_right = pyganim.PygAnimation(self.Attack1_pic, loop=False)
        self.Attack1_right._rate = self.speed

        self.Attack1_left = pyganim.PygAnimation(self.Attack1_pic, loop=False)
        self.Attack1_left.anchor(anchorPoint=pyganim.CENTER)
        self.Attack1_left.flip(True, False)
        self.Attack1_left._rate = self.speed
        self.Attack1_left.makeTransformsPermanent()
        self.Attack1_left.clearTransforms()

        self.Attack2_right = pyganim.PygAnimation(self.Attack2_pic, loop=False)
        self.Attack2_right._rate = self.speed

        self.Attack2_left = pyganim.PygAnimation(self.Attack2_pic, loop=False)
        self.Attack2_left.anchor(anchorPoint=pyganim.CENTER)
        self.Attack2_left.flip(True, False)
        self.Attack2_left._rate = self.speed
        self.Attack2_left.makeTransformsPermanent()
        self.Attack_anim_cur = self.Attack1_right

        self.Casting_anim_cur = self.Attack1_right

        self.Dead_right = image.load(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/human_veteran_dead.png"))
        self.Dead_left = transform.flip(image.load(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/human_veteran_dead.png")), True, False)

        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()

        self.Falling_right = image.load(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/human_veteran_falling.png"))
        self.Falling_left = transform.flip(image.load(resource_path("Media/Sprites/Units/Humans/Human_fighter_veteran/human_veteran_falling.png")), True, False)

        self.Stand_right = pyganim.PygAnimation(self.Stand_pic)
        self.Stand_right._rate = self.speed
        self.Stand_right.play()

        self.Stand_left = pyganim.PygAnimation(self.Stand_pic)
        self.Stand_left.anchor(anchorPoint='c')
        self.Stand_left.flip(True, False)
        self.Stand_left._rate = self.speed
        self.Stand_left.play()

        self.Walk_left = pyganim.PygAnimation(self.Walk_pic)
        self.Walk_left.anchor(anchorPoint='c')
        self.Walk_left.flip(True, False)
        self.Walk_left._rate = self.speed
        self.Walk_left.play()

        self.Walk_right = pyganim.PygAnimation(self.Walk_pic)
        self.Walk_right.play()
        self.Walk_right._rate = self.speed

    def attack_anims_con(self, action, dirr):
        self.set_cur_dir(dirr)
        if action == "stop":
            self.Attack_anim_cur.stop()
        elif action == "play":
            self.Attack_anim_cur.play()

    def casting_anim_control(self, action, dirr):
        self.set_cur_dir(dirr)
        if action == "stop":
            self.Casting_anim_cur.stop()
        elif action == "play":
            self.Casting_anim_cur.play()

    def get_anim_speed(self, anim):
        anim_array = self.Attack1_pic
        ms_sum = 0
        if anim == "Attack":
            anim_array = self.Attack1_pic
        for frame in anim_array:
            ms_sum += frame[1]
        return ms_sum

    def set_cur_dir(self, dirr):
        if dirr == 0:
            if random.randint(1, 2) == 1:
                self.Attack_anim_cur = self.Attack1_left
                self.Casting_anim_cur = self.Attack1_left
            else:
                self.Attack_anim_cur = self.Attack2_left
                self.Casting_anim_cur = self.Attack2_left
        else:
            if random.randint(1, 2) == 1:
                self.Attack_anim_cur = self.Attack1_right
                self.Casting_anim_cur = self.Attack1_right
            else:
                self.Attack_anim_cur = self.Attack2_right
                self.Casting_anim_cur = self.Attack2_right
