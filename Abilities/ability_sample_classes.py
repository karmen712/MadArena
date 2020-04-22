from pygame import *
from System.resoursepath import resource_path
import System.game_options as options
import math
import pyganim


class ParabollicTrajectory:
    def __init__(self, caster):
        self.speed = 7
        self.caster = caster
        self.casting_distance = 300
        self.cooldown = 10000
        self.current_cooldown = 0
        self.damage = 60
        self.projectile = RedBall
        self.projectiles = []
        self.spell_target = None
        self.state = "ready"

    def draw(self, screen):

        if self.current_cooldown > 0:
            self.current_cooldown -= options.milliseconds
            self.state = "on_cd"
        elif self.current_cooldown < 0:
            self.state = "ready"
            self.current_cooldown = 0
        elif self.current_cooldown == 0:
            self.state = "ready"

        if self.state == "casting":
            if self.caster.state != "casting":
                self.state = "ready"

        if self.caster.animations.Casting_anim_cur.isFinished() and self.caster.state == "casting":
            self.caster.animations.Casting_anim_cur.stop()
            self.caster.state = "stand"
            self.spawn_projectile()
            self.state = "on_cd"
            self.current_cooldown = self.cooldown

        for pr in self.projectiles:
            if pr.state != "destroyed":
                pr.draw(screen)
            else:
                self.projectiles.remove(pr)
                del pr

    def spawn_projectile(self):
        self.caster.casting_ability = None
        self.caster.ability_target = None
        pos = self.caster.rect.topleft if self.caster.dir == 0 else self.caster.rect.topright
        self.projectiles.append(self.projectile(pos, self.caster.dir, self.damage, self.caster, self.spell_target))

    def cast(self, target):
        self.caster.set_dir_to(target)
        self.spell_target = target
        self.state = "casting"
        self.caster.casting_ability = self


class RedBall:
    def rotate(self):
        if isinstance(self.fly_anim, pyganim.PygAnimation):
            if self.dir != 0:
                self.fly_anim.anchor(anchorPoint=pyganim.CENTER)
                self.fly_anim.flip(True, False)
        else:
            pygame.transform.flip(self.fly_anim, True, False)

    def __init__(self, pos, dirr, damage, caster, target):
        #  fly_anim must face left by default do not forget to rotate
        self.dir = dirr
        self.sprite = image.load(resource_path("Media/Sprites/Effects/Samples/red_dot.png"))
        self.rect = self.rect = self.sprite.get_rect(center=pos)

        self.fly_anim = image.load(resource_path("Media/Sprites/Effects/Samples/red_dot.png"))
        self.stopped_anim = image.load(resource_path("Media/Sprites/Effects/Samples/red_dot.png"))

        self.caster = caster
        self.current_distance = 0
        self.damage = damage
        self.distance_to_target = abs(caster.rect.center[0] - target.rect.center[0])  # self.get_distance(caster.rect.center, target.rect.center)
        self.force = -self.distance_to_target * 0.029
        self.last_p = []
        self.lifetime = 250
        self.state = "in_motion"
        self.speed = -14 if dirr == 0 else 14
        self.target = target
        self.tail = True
        self.tail_color = (235, 46, 58)
        self.tail_length = 8
        self.y = self.rect.midbottom[1]

    def blit_anim(self, anim, screen, rect):
        if isinstance(anim, pyganim.PygAnimation):
            anim.blit(screen, rect)
            anim.play()
        else:
            screen.blit(anim, rect)

    def draw(self, screen):
        if self.state == "in_motion":
            self.last_p.append(self.rect.center)
            if len(self.last_p) > self.tail_length:
                self.last_p.pop(0)
            dx = self.speed
            dy = self.force
            self.force += options.gravity
            self.current_distance += self.speed
            self.rect.move_ip(dx, dy)
            self.blit_anim(self.fly_anim, screen, self.rect)
            if self.rect.colliderect(self.target.rect):
                self.state = "stopped"
                self.impact()
            if abs(self.current_distance) > self.distance_to_target or self.y < self.rect.center[1]:
                self.state = "stopped"

        elif self.state == "stopped":
            self.blit_anim(self.stopped_anim, screen, self.rect)
            self.lifetime -= options.milliseconds

        if self.tail:
            if len(self.last_p) > 2:
                draw.lines(screen, self.tail_color, False, self.last_p, 1)

        if self.lifetime < 0:
            self.state = "destroyed"

    def impact(self):
        if self.caster is not None:
            self.caster.deal_damage(self.damage, self.target)

    @staticmethod
    def get_distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
