from MiniView import Window

try:
    visual: Window = Window("MiniView", 16 * 100, 10 * 100)
except OSError:
    pass
