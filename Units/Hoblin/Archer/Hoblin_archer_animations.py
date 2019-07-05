from System.resoursepath import resource_path
from pygame import image, transform
import pyganim
import random


class HoblinArcherAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_pic = [(resource_path("Media/Sprites/Units/Hoblin/Archer/stand/hoblin_stand_1.png"), 250),
                          (resource_path("Media/Sprites/Units/Hoblin/Archer/stand/hoblin_stand_2.png"), 250),
                          (resource_path("Media/Sprites/Units/Hoblin/Archer/stand/hoblin_stand_3.png"), 250),
                          (resource_path("Media/Sprites/Units/Hoblin/Archer/stand/hoblin_stand_4.png"), 250),
                          (resource_path("Media/Sprites/Units/Hoblin/Archer/stand/hoblin_stand_5.png"), 250),
                          (resource_path("Media/Sprites/Units/Hoblin/Archer/stand/hoblin_stand_6.png"), 2250)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Hoblin/Archer/Drag/hoblin_archer_drag_1.png"), 350),
                         (resource_path("Media/Sprites/Units/Hoblin/Archer/Drag/hoblin_archer_drag_2.png"), 350)]

        self.Walk_pic = [(resource_path("Media/Sprites/Units/Hoblin/Archer/walk/hoblin_archer_walk1.png"), 200),
                         (resource_path("Media/Sprites/Units/Hoblin/Archer/walk/hoblin_archer_walk2.png"), 200),
                         (resource_path("Media/Sprites/Units/Hoblin/Archer/walk/hoblin_archer_walk3.png"), 200),
                         (resource_path("Media/Sprites/Units/Hoblin/Archer/walk/hoblin_archer_walk4.png"), 200),
                         (resource_path("Media/Sprites/Units/Hoblin/Archer/walk/hoblin_archer_walk5.png"), 200),
                         (resource_path("Media/Sprites/Units/Hoblin/Archer/walk/hoblin_archer_walk6.png"), 200),
                         (resource_path("Media/Sprites/Units/Hoblin/Archer/walk/hoblin_archer_walk7.png"), 200)]

        self.Attack_pic = [(resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_1.png"), 200),
                           (resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_2.png"), 200),
                           (resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_3.png"), 200),
                           (resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_4.png"), 200),
                           (resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_5.png"), 200),
                           (resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_6.png"), 200),
                           (resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_7.png"), 200),
                           (resource_path("Media/Sprites/Units/Hoblin/Archer/attack/hoblin_attack_8.png"), 200)
                           ]

        self.Attack1_right = pyganim.PygAnimation(self.Attack_pic, loop=False)
        self.Attack1_right._rate = self.speed

        self.Attack1_left = pyganim.PygAnimation(self.Attack_pic, loop=False)
        self.Attack1_left.anchor(anchorPoint=pyganim.CENTER)
        self.Attack1_left.flip(True, False)
        self.Attack1_left._rate = self.speed
        self.Attack1_left.makeTransformsPermanent()
        self.Attack1_left.clearTransforms()

        self.Attack_anim_cur = self.Attack1_right

        self.Casting_anim_cur = self.Attack1_right

        self.Dead_left = image.load(resource_path("Media/Sprites/Units/Hoblin/Archer/hoblin_archer_dead.png"))
        self.Dead_right = transform.flip(self.Dead_left, True, False)

        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()

        self.Falling_right = image.load(resource_path("Media/Sprites/Units/Hoblin/Archer/hoblin_archer_falling.png"))
        self.Falling_left = transform.flip(self.Falling_right, True, False)

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
        anim_array = self.Attack_pic
        ms_sum = 0
        if anim == "Attack":
            anim_array = self.Attack_pic
        for frame in anim_array:
            ms_sum += frame[1]
        return ms_sum

    def set_cur_dir(self, dirr):
        if dirr == 0:
            self.Attack_anim_cur = self.Attack1_left
            self.Casting_anim_cur = self.Attack1_left
        else:
            self.Attack_anim_cur = self.Attack1_right
            self.Casting_anim_cur = self.Attack1_left

