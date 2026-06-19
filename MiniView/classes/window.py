from .vector2D import Vector2D
from typing import Any

class Window():
    dimensions: Vector2D
    name: str
    __running: bool = False
    __lib: Any
    __display: Any
    __RW: Any
    window: Any

    def __init__(self, name: str, width: int, height: int) -> None:
        self.name = name
        self.dimensions = Vector2D(width, height)

    def open(self) -> None:
        import ctypes
        self.__running = True
        self.__lib = ctypes.CDLL("libX11.so")

        self.__lib.XOpenDisplay.restype = ctypes.c_void_p
        self.__lib.XOpenDisplay.argtypes = [ctypes.c_char_p]
        self.__display = self.__lib.XOpenDisplay(None)

        if not self.__display:
            print("\033[38;2;255mMiniView Failed to Open: "
                  "XOpenDisplay returned None.\033[0m")
            return

        self.__lib.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
        self.__lib.XDefaultRootWindow.restype = ctypes.c_ulong
        self.__RW = self.__lib.XDefaultRootWindow(self.__display)

        self.__lib.XCreateSimpleWindow.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_ulong,
                                                   ctypes.c_uint,
                                                   ctypes.c_uint,
                                                   ctypes.c_uint,
                                                   ctypes.c_uint,
                                                   ctypes.c_ulong,
                                                   ctypes.c_ulong]
        self.__lib.XCreateSimpleWindow.restype = ctypes.c_ulong

        self.window = self.__lib.XCreateSimpleWindow(self.__display,
                                                     self.__RW,
                                                     0, 0,
                                                     self.dimensions.x,
                                                     self.dimensions.y,
                                                     0x000000,
                                                     0x000000)

        self.__lib.XMapWindow.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        self.__lib.XMapWindow.restypes = ctypes.c_int
        self.__lib.XMapWindow(self.__display, self.window)

        self.__lib.XSelectInput.argtypes = [ctypes.c_void_p, ctypes.c_ulong,
                                            ctypes.c_long]
        self.__lib.XSelectInput.restype = ctypes.c_int

        KeyPressMask = 1 << 0
        KeyReleaseMask = 1 << 1
        ButtonPressMask = 1 << 2
        ButtonReleaseMask = 1 << 3
        ExposureMask = 1 << 15
        StructureNotifyMask = 1 << 17

        self.__lib.XSelectInput(self.__display, self.window, KeyPressMask |
                                KeyReleaseMask | ButtonPressMask |
                                ButtonReleaseMask | ExposureMask | StructureNotifyMask)

        class XEvent(ctypes.Structure):
            _fields_ = [
                ("type", ctypes.c_int)
            ]
        
        self.__lib.XNextEvent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.__lib.XNextEvent.restype = ctypes.c_int
        eventlist = XEvent()
    
        while self.__running:
            self.__lib.XNextEvent(self.__display,
                                          ctypes.byref(eventlist))
            print(eventlist.type)
            if eventlist.type == 17:
                self.__running = False
        self.__lib.XCloseDisplay(self.__display)
