from System.resoursepath import resource_path
from pygame import image
import pyganim
import random


class HumanAnimations:
    def __init__(self, speed):
        self.speed = speed / 100  # проценты перевожу в десятые доли
        self.Stand_right_pic = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right3.png"), 700),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right2.png"), 300),
                                (resource_path("Media/Sprites/Units/Human/Stand/human_stand_right1.png"), 200)]

        self.Stand_left_pic = [(resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 800),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left2.png"), 400),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left1.png"), 300),
                               (resource_path("Media/Sprites/Units/Human/Stand/human_stand_left3.png"), 200)]

        self.Drag_pic = [(resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag23.png"), 300),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag22.png"), 300),
                         (resource_path("Media/Sprites/Units/Human/Drag/human_Drag21.png"), 200)]

        self.Walk_left_pic = [(resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left1.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left2.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left3.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left4.png"), 200),
                              (resource_path("Media/Sprites/Units/Human/Walk/Left/human_walk_left5.png"), 200)]

        self.Walk_right_pic = [(resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right1.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right2.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right3.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right4.png"), 200),
                               (resource_path("Media/Sprites/Units/Human/Walk/Right/human_walk_right5.png"), 200)]

        self.Attack1_left_pic = [(resource_path("Media/Sprites/Units/Human/Attack/Attack1/Left/human_attack_left1.png"), 600),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Attack1/Left/human_attack_left2.png"), 400),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Attack1/Left/human_attack_left4.png"), 200),
                                 (resource_path("Media/Sprites/Units/Human/Attack/Attack1/Left/human_attack_left3.png"), 300)]

        self.Attack1_right_pic = [(resource_path("Media/Sprites/Units/Human/Attack/Attack1/Right/human_attack_right1.png"), 600),
                                  (resource_path("Media/Sprites/Units/Human/Attack/Attack1/Right/human_attack_right2.png"), 400),
                                  (resource_path("Media/Sprites/Units/Human/Attack/Attack1/Right/human_attack_right4.png"), 200),
                                  (resource_path("Media/Sprites/Units/Human/Attack/Attack1/Right/human_attack_right3.png"), 300)]

        self.Attack2_pic = [(resource_path("Media/Sprites/Units/Human/Attack/Attack2/human_attack2_1.png"), 600),
                            (resource_path("Media/Sprites/Units/Human/Attack/Attack2/human_attack2_2.png"), 400),
                            (resource_path("Media/Sprites/Units/Human/Attack/Attack2/human_attack2_3.png"), 200),
                            (resource_path("Media/Sprites/Units/Human/Attack/Attack2/human_attack2_4.png"), 300)]

        self.Attack1_left = pyganim.PygAnimation(self.Attack1_left_pic, loop=False)
        self.Attack1_left._rate = self.speed
        self.Attack1_right = pyganim.PygAnimation(self.Attack1_right_pic, loop=False)
        self.Attack1_right._rate = self.speed

        self.Attack2_right = pyganim.PygAnimation(self.Attack2_pic, loop=False)
        self.Attack2_right._rate = self.speed

        self.Attack2_left = pyganim.PygAnimation(self.Attack2_pic, loop=False)
        self.Attack2_left.anchor(anchorPoint=pyganim.CENTER)
        self.Attack2_left.flip(True, False)
        self.Attack2_left._rate = self.speed
        self.Attack2_left.makeTransformsPermanent()

        self.Attack_anim_cur = self.Attack1_right

        self.Casting_anim_cur = self.Attack1_right

        self.Dead_left = image.load(resource_path("Media/Sprites/Units/Human/human_dead_left.png"))
        self.Dead_right = image.load(resource_path("Media/Sprites/Units/Human/human_dead_right.png"))
        self.Drag = pyganim.PygAnimation(self.Drag_pic)
        self.Drag.play()
        self.Falling_right = image.load(resource_path("Media/Sprites/Units/Human/human_falling_right.png"))
        self.Falling_left = image.load(resource_path("Media/Sprites/Units/Human/human_falling_left.png"))
        self.Stand_right = pyganim.PygAnimation(self.Stand_right_pic)
        self.Stand_right._rate = self.speed
        self.Stand_right.play()
        self.Stand_left = pyganim.PygAnimation(self.Stand_left_pic)
        self.Stand_left._rate = self.speed
        self.Stand_left.play()
        self.Walk_left = pyganim.PygAnimation(self.Walk_left_pic)
        self.Walk_left._rate = self.speed
        self.Walk_left.play()
        self.Walk_right = pyganim.PygAnimation(self.Walk_right_pic)
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
        anim_array = self.Attack1_left_pic
        ms_sum = 0
        if anim == "Attack":
            anim_array = self.Attack1_left_pic
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

