import pygame as pg
import socket

WIDTH = 1000
HEIGHT = 750

xMiddle = WIDTH / 2
yMiddle = HEIGHT / 2

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
YELLOW = (255,255,0)

colorPalitre = {"GRAY": GRAY,
                "RED": RED,
                "GREEN": GREEN,
                "YELLOW": YELLOW}

SERVER_HOST = '192.168.1.103'
SERVER_PORT = 65432

clock = pg.time.Clock()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Не потрібно дійсно підключатися
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip