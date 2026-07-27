from MiniView import Window, Vector2D, Object
from time import sleep

try:
    visual: Window = Window("MiniView", 16 * 100, 10 * 100)
except OSError:
    pass