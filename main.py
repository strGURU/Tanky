import pygame as pg
from config import *
from tankController import *
from map import *

screen = pg.display.set_mode((WIDTH, HEIGHT))

def main():
    pg.init()

    pg.display.set_caption("Tanki Online")
    pg.display.set_icon(pg.image.load("Sprites/Tanks/GRAY/RIGHT1.png"))

    RedTank = Tank(100, 50, "RED", "DOWN", 5, 2, screen, [50, 125], {
        "UP": pg.K_w,
        "DOWN": pg.K_s,
        "LEFT": pg.K_a,
        "RIGHT": pg.K_d,
        "SHOOT": pg.K_q
    })
    GrayTank = Tank(850, 50, "GRAY", "DOWN", 5, 2, screen, [800, 125], {
        "UP": pg.K_UP,
        "DOWN": pg.K_DOWN,
        "LEFT": pg.K_LEFT,
        "RIGHT": pg.K_RIGHT,
        "SHOOT": pg.K_RSHIFT
    })

    GreenTank = Tank(100, 650, "GREEN", "UP",  5, 2, screen, [50, 600], {
        "UP": pg.K_i,
        "DOWN": pg.K_k,
        "LEFT": pg.K_j,
        "RIGHT": pg.K_l,
        "SHOOT": pg.K_u
    })

    YellowTank = Tank(850, 650, "YELLOW", "UP",  5, 2, screen, [780, 600],{
        "UP": pg.K_t,
        "DOWN": pg.K_g,
        "LEFT": pg.K_f,
        "RIGHT": pg.K_h,
        "SHOOT": pg.K_r
    })

    PaintList.insert(0, RedTank)
    PaintList.insert(0, GrayTank)
    PaintList.insert(0, GreenTank)
    PaintList.insert(0, YellowTank)

    CollisionList.insert(0, RedTank)
    CollisionList.insert(0, GrayTank)
    CollisionList.insert(0, GreenTank)
    CollisionList.insert(0, YellowTank)

    TankList = [RedTank, GrayTank, GreenTank, YellowTank]

    Boxes = Buffs(screen)
    Boxes.Start(CollisionList)

    IsRunning = True
    while IsRunning:
        screen.fill(BLACK)
        Boxes.Working(CollisionList)

        for obj in PaintList:
            if obj.IsPainting:
                obj.reset()
            if isinstance(obj, Tank):
                if obj.HP == 0:
                    CollisionList.remove(obj)
                    obj.HP -= 1
                if obj.HP > -2:
                    obj.move(CollisionList)
            if isinstance(obj, Block) and not obj.IsPainting and obj.animationCounter == 0:
                CollisionList.remove(obj)
                obj.animationCounter += 1

        for tank in TankList:
            tank.draw_hp()

        clock.tick(60)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                IsRunning = False
                pg.quit()

if __name__ == "__main__":
    main()
