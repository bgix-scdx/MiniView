from .vector2D import Vector2D
from pydantic import BaseModel
from ctypes import c_void_p, c_int, c_ulong
from typing import Any


class Object():
    position: Vector2D = Vector2D(0, 0)
    __priorrender: Vector2D = Vector2D(0, 0)
    name: str = "Object"
    size: Vector2D = Vector2D(100, 100)
    pivotpoint: Vector2D = Vector2D(50, 50)
    color: int = 0xFF0000
    gc: Any = None

    def show(self, screen: Any):
        screen.lib.XCreateGC.argtypes = [c_void_p, c_ulong, c_ulong, c_void_p]
        screen.lib.XCreateGC.restype = c_void_p
        if not self.gc:
            self.gc = screen.lib.XCreateGC(screen.display, screen.window, 0, None)

        screen.lib.XDrawPoint.argtypes = [c_void_p, c_int,
                                          c_void_p, c_int, c_int]

        screen.lib.XSetForeground(screen.display, self.gc, self.color)

        for x in range(self.size.x):
            for y in range(self.size.y):
                screen.lib.XDrawPoint(screen.display, screen.window,
                                      self.gc,
                                      x + self.position.x - self.pivotpoint.x,
                                      y  + self.position.y - self.pivotpoint.y)
        screen.lib.XFlush(screen.display)
