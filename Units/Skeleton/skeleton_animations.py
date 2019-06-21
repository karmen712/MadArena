from System.resoursepath import resource_path
from pygame import image, transform
import pyganim
import random


class SkeletonAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_pic = [(resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand1.png"), 400),
                          (resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand2.png"), 200),
                          (resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand3.png"), 400),
                          (resource_path("Media/Sprites/Units/Skeleton/Stand/skeleton_stand2.png"), 200)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Skeleton/Drag/drag1.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Drag/drag2.png"), 300),
                         (resource_path("Media/Sprites/Units/Skeleton/Drag/drag3.png"), 300),
                         (resource_path("Media/Sprites/Units/Skeleton/Drag/drag4.png"), 300)]

        self.Walk_pic = [(resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk1.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk2.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk3.png"), 200),
                         (resource_path("Media/Sprites/Units/Skeleton/Walk/skeleton_walk4.png"), 200)]

        self.Attack1_pic = [(resource_path("Media/Sprites/Units/Skeleton/Attack/Attack1/skeleton_attack1.png"), 300),
                            (resource_path("Media/Sprites/Units/Skeleton/Attack/Attack1/skeleton_attack2.png"), 300),
                            (resource_path("Media/Sprites/Units/Skeleton/Attack/Attack1/skeleton_attack3.png"), 300),
                            (resource_path("Media/Sprites/Units/Skeleton/Attack/Attack1/skeleton_attack4.png"), 300)]

        self.Attack2_pic = [(resource_path("Media/Sprites/Units/Skeleton/Attack/Attack2/skeleton_attack1.png"), 300),
                            (resource_path("Media/Sprites/Units/Skeleton/Attack/Attack2/skeleton_attack2.png"), 300),
                            (resource_path("Media/Sprites/Units/Skeleton/Attack/Attack2/skeleton_attack3.png"), 300),
                            (resource_path("Media/Sprites/Units/Skeleton/Attack/Attack2/skeleton_attack4.png"), 300)]

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

        self.Dead_right = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_dead.png"))
        self.Dead_left = transform.flip(image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_dead.png")), True, False)

        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()

        self.Falling_right = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_falling.png"))
        self.Falling_left = image.load(resource_path("Media/Sprites/Units/Skeleton/skeleton_falling.png"))
        transform.flip(self.Falling_left, True, False)

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
        if dirr == 0:
            if random.randint(1, 2) == 1:
                self.Attack_anim_cur = self.Attack1_left
            else:
                self.Attack_anim_cur = self.Attack2_left
        else:
            if random.randint(1, 2) == 1:
                self.Attack_anim_cur = self.Attack1_right
            else:
                self.Attack_anim_cur = self.Attack2_right
        if action == "stop":
            self.Attack_anim_cur.stop()
        elif action == "play":
            self.Attack_anim_cur.play()

    def get_anim_speed(self, anim):
        anim_array = self.Attack_pic
        ms_sum = 0
        if anim == "Attack":
            anim_array = self.Attack_pic
        for frame in anim_array:
            ms_sum += frame[1]
        return ms_sum
