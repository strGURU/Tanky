import pygame as pg
from config import *
import threading
from random import choice, randint
import time

pg.init()


class GameSprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, w, h, win):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(filename), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.win = win
        self.IsPainting = True
        self.animationCounter = 0
        self.animationFrame = 0

    def reset(self):
        self.win.blit(self.image, (self.rect.x, self.rect.y))


class Block(GameSprite):
    def __init__(self, x, y, skin, win):
        GameSprite.__init__(self, f"Sprites/Blocks/{skin}.png", x, y, WIDTH / 20, WIDTH / 20, win)
        self.IsDestryable = False if skin == "Metal" else True

class Buffs():
    def __init__(self, win):
        self.BulletSpeed = GameSprite("Sprites/Tanks/Bufes/BulletSpeed.png", -100, -100, 48, 45, win)
        self.TankHealth = GameSprite("Sprites/Tanks/Bufes/TankHealth.png", -100, -100, 48, 45, win)
        self.TankSpeed = GameSprite("Sprites/Tanks/Bufes/TankSpeed.png", -100, -100, 48, 45, win)
        self.ChooseList = [self.BulletSpeed, self.TankHealth, self.TankSpeed]

    def Spawn(self, colisionList):
        while True:
            time.sleep(randint(5, 30))
            PointIsReady = False
            while not PointIsReady:
                x = randint(0, WIDTH - self.BulletSpeed.w)
                y = randint(0, HEIGHT - self.BulletSpeed.w)
                if not self.check(x, y, colisionList):
                    buff = choice(self.ChooseList)
                    buff.rect.x = x
                    buff.rect.y = y
                    PointIsReady = True

    def Working(self, collision_list):
        for box in self.ChooseList:
            box.reset()
            self.PlayerCheck(box.rect.x, box.rect.y, box, collision_list)

    def Start(self, collisionList):
        thread = threading.Thread(target=self.Spawn, args=(collisionList,))
        thread.daemon = True
        thread.start()

    def check(self, x, y,  collision_list):
        object_touch = []
        tmp_area = pg.Rect(x, y, self.BulletSpeed.w, self.BulletSpeed.w)
        for collision in collision_list:
            object_touch.append(collision.rect.colliderect(tmp_area))
        return True in object_touch

    def PlayerCheck(self, x, y, box, collision_list):
        tmp_area = pg.Rect(x, y, box.w, box.h)
        for collision in collision_list:
            if collision.rect.colliderect(tmp_area):
                if isinstance(collision, Tank):
                    if box is self.BulletSpeed:
                        collision.bulletSpeed += 10
                        box.rect.x = -100
                        box.rect.y = -100
                    if box is self.TankSpeed:
                        collision.speed += collision.speed * 0.2
                        box.rect.x = -100
                        box.rect.y = -100
                    if box is self.TankHealth:
                        collision.HP += 1
                        box.rect.x = -100
                        box.rect.y = -100

class Tank(GameSprite):
    def __init__(self, x, y, skin, StartSide, hp, speed, win, HpRender, ControlKeys=None):
        GameSprite.__init__(self, f"Sprites/Tanks/{skin}/{StartSide}1.png", x, y, WIDTH / 20, WIDTH / 20, win)
        self.skin = skin
        self.HP = hp
        self.speed = speed
        self.WolkAnimFrame = 1
        self.side = StartSide
        self.font = pg.font.Font("Sprites/Minecraft.ttf", 30)
        self.HpRender = HpRender

        self.ShootButton = True
        self.CanShoot = True
        self.IsExpoding = False

        self.bullet = GameSprite("Sprites/Bullets.Explods/BULLET.png", 0, 0, self.w * 0.18, self.h * 0.24, self.win)
        self.bulletSpeed = 10
        self.bulletAngle = 0
        self.bulletAnimationCounter = 0
        self.bulletAnimationFrame = 0

        self.ControlKeys = ControlKeys if ControlKeys is not None else {
            "UP": pg.K_UP,
            "DOWN": pg.K_DOWN,
            "LEFT": pg.K_LEFT,
            "RIGHT": pg.K_RIGHT,
            "SHOOT": pg.K_z
        }

    def move(self, collision_list):
        keys_move = pg.key.get_pressed()
        if self.HP > 0:
            if keys_move[self.ControlKeys["UP"]] and self.rect.y > 0 and not self.check(self.rect.x, self.rect.y - self.speed, collision_list):
                if self.side != "UP":
                    self.side = "UP"
                self.rect.y -= self.speed
                self.image = pg.transform.scale(pg.image.load(f"Sprites/Tanks/{self.skin}/UP{self.WolkAnimFrame}.png"), (self.w, self.h))
                self.WolkAnimFrame = 1 if self.WolkAnimFrame == 2 else 2
            elif keys_move[self.ControlKeys["DOWN"]] and self.rect.y < HEIGHT - self.w and not self.check(self.rect.x, self.rect.y + self.speed, collision_list):
                if self.side != "DOWN":
                    self.side = "DOWN"
                self.rect.y += self.speed
                self.image = pg.transform.scale(pg.image.load(f"Sprites/Tanks/{self.skin}/DOWN{self.WolkAnimFrame}.png"), (self.w, self.h))
                self.WolkAnimFrame = 1 if self.WolkAnimFrame == 2 else 2
            elif keys_move[self.ControlKeys["LEFT"]] and self.rect.x > 0 and not self.check(self.rect.x - self.speed, self.rect.y, collision_list):
                if self.side != "LEFT":
                    self.side = "LEFT"
                self.rect.x -= self.speed
                self.image = pg.transform.scale(pg.image.load(f"Sprites/Tanks/{self.skin}/LEFT{self.WolkAnimFrame}.png"), (self.w, self.h))
                self.WolkAnimFrame = 1 if self.WolkAnimFrame == 2 else 2
            elif keys_move[self.ControlKeys["RIGHT"]] and self.rect.x < WIDTH - self.h and not self.check(self.rect.x + self.speed, self.rect.y, collision_list):
                if self.side != "RIGHT":
                    self.side = "RIGHT"
                self.rect.x += self.speed
                self.image = pg.transform.scale(pg.image.load(f"Sprites/Tanks/{self.skin}/RIGHT{self.WolkAnimFrame}.png"), (self.w, self.h))
                self.WolkAnimFrame = 1 if self.WolkAnimFrame == 2 else 2
            if keys_move[self.ControlKeys["SHOOT"]] and self.ShootButton and self.CanShoot:
                self.shoot()
                self.CanShoot = False
                self.ShootButton = False
        if not keys_move[self.ControlKeys["SHOOT"]]:
            self.ShootButton = True
        self.bulletFlying(collision_list)

    def shoot(self):
        if self.side == "UP":
            self.bulletAngle = 0
            self.bullet.rect.x = self.rect.x + self.w / 2 - self.bullet.w / 2
            self.bullet.rect.y = self.rect.y - self.bullet.h
        elif self.side == "DOWN":
            self.bulletAngle = 180
            self.bullet.rect.x = self.rect.x + self.w / 2 - self.bullet.w / 2
            self.bullet.rect.y = self.rect.y + self.w
        elif self.side == "RIGHT":
            self.bulletAngle = -90
            self.bullet.rect.x = self.rect.x + self.w
            self.bullet.rect.y = self.rect.y + self.w / 2 - self.bullet.w / 2
        elif self.side == "LEFT":
            self.bulletAngle = 90
            self.bullet.rect.x = self.rect.x - self.bullet.h
            self.bullet.rect.y = self.rect.y + self.w / 2 - self.bullet.w / 2
        self.bullet.image = pg.transform.rotate(self.bullet.image, self.bulletAngle)

    def draw_hp(self):
        if self.HP > 0:
            hp_text = self.font.render(f"{self.skin} HP: {self.HP}", True, colorPalitre[self.skin])
        else:
            hp_text = self.font.render("DEATH", True, colorPalitre[self.skin])
        if self.HP == -1:
            if self.skin == "YELLOW":
                self.HpRender[0] += 0.8
            else:
                self.HpRender[0] += 0.47
        self.win.blit(hp_text, (self.HpRender[0], self.HpRender[1]))

    def bulletFlying(self, collision_list):
        if not self.CanShoot and not self.IsExpoding:
            self.bullet.reset()
            if self.bulletAngle == 0:
                self.bulletCheck(self.bullet.rect.x, self.bullet.rect.y - self.bulletSpeed, collision_list)
                self.bullet.rect.y -= self.bulletSpeed
            elif self.bulletAngle == 180:
                self.bulletCheck(self.bullet.rect.x, self.bullet.rect.y + self.bulletSpeed, collision_list)
                self.bullet.rect.y += self.bulletSpeed
            elif self.bulletAngle == 90:
                self.bulletCheck(self.bullet.rect.x - self.bulletSpeed, self.bullet.rect.y, collision_list)
                self.bullet.rect.x -= self.bulletSpeed
            elif self.bulletAngle == -90:
                self.bulletCheck(self.bullet.rect.x + self.bulletSpeed, self.bullet.rect.y, collision_list)
                self.bullet.rect.x += self.bulletSpeed
            if (self.bullet.rect.x >= WIDTH or self.bullet.rect.x < 0 or
                self.bullet.rect.y >= HEIGHT or self.bullet.rect.y < 0):
                self.bullet.rect.x -= self.w * 0.7
                self.bullet.rect.y -= self.h * 0.7
                self.IsExpoding = True

        if self.IsExpoding:
            self.bullet.reset()
            if 0 <= self.bulletAnimationCounter < 10:
                self.bulletAnimationFrame = 1
            elif 10 <= self.bulletAnimationCounter < 20:
                self.bulletAnimationFrame = 2
            elif 20 <= self.bulletAnimationCounter < 30:
                self.bulletAnimationFrame = 3
            self.bullet.image = pg.transform.scale(pg.image.load(f"Sprites/Bullets.Explods/miniEXPODE{self.bulletAnimationFrame}.png"),(self.w * 1.4, self.h * 1.4))
            self.bulletAnimationCounter += 1

            if self.bulletAnimationCounter >= 30:
                self.bullet.image = pg.transform.scale(pg.image.load(f"Sprites/Bullets.Explods/BULLET.png"),(self.w * 0.18, self.h * 0.24))
                self.IsExpoding = False
                self.CanShoot = True
                self.bulletAnimationCounter = 0
        if self.HP <= 0:
            if 0 <= self.animationCounter < 20:
                self.image = pg.transform.scale(pg.image.load(f"Sprites/Bullets.Explods/miniEXPODE3.png"),(self.w * 1.4, self.h * 1.4))
            elif 20 <= self.animationCounter < 40:
                self.image = pg.transform.scale(pg.image.load(f"Sprites/Bullets.Explods/bigEXPODE1.png"),(self.w * 2.5, self.h * 2.5))
            elif 40 <= self.animationCounter < 60:
                self.image = pg.transform.scale(pg.image.load(f"Sprites/Bullets.Explods/bigEXPODE2.png"),(self.w * 2.5, self.h * 2.5))
            self.animationCounter += 1

            if self.animationCounter >= 60:
                self.IsPainting = False
                self.CanShoot = True
                self.animationCounter = 0
                self.HP -= 1

    def check(self, x, y,  collision_list):
        object_touch = []
        tmp_area = pg.Rect(x, y, self.w, self.h)
        for collision in collision_list:
            if collision is self:
                continue
            object_touch.append(collision.rect.colliderect(tmp_area))
        return True in object_touch

    def BulletColibrate(self):
        if self.bulletAngle == 0:
            self.bullet.rect.x -= self.w * 0.7
            self.bullet.rect.y -= self.h * 0.7
        elif self.bulletAngle == 180:
            self.bullet.rect.x -= self.w * 0.7
            self.bullet.rect.y -= self.h * 0.7
        elif self.bulletAngle == 90:
            self.bullet.rect.x -= self.w * 0.7
            self.bullet.rect.y -= self.h * 0.7
        elif self.bulletAngle == -90:
            self.bullet.rect.x -= self.w * 0.7
            self.bullet.rect.y -= self.h * 0.7

    def bulletCheck(self, x, y,  collision_list):
        tmp_area = pg.Rect(x, y, self.bullet.w, self.bullet.h)
        for collision in collision_list:
            if collision.rect.colliderect(tmp_area):
                if isinstance(collision, Tank) and not collision is self:
                    collision.HP -= 1
                    self.BulletColibrate()
                    self.IsExpoding = True
                if isinstance(collision, Block):
                    if collision.IsDestryable:
                        collision.IsPainting = False
                    self.BulletColibrate()
                    self.IsExpoding = True
