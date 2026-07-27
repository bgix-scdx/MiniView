from .vector2D import Vector2D
from typing import Any, List, Dict
from threading import Thread
from ctypes import c_void_p, c_int, c_char_p, c_ulong, POINTER, c_uint
from ctypes import c_long, Structure, CDLL, byref
from time import sleep
from .objects import Object
from platform import system

class Window():
    dimensions: Vector2D
    name: str
    __running: bool = False
    lib: Any
    display: Any
    __RW: Any
    ready: bool = False
    objects: Dict[str, Object] = {}
    window: Any

    def __init__(self, name: str, width: int, height: int) -> None:
        self.name = name
        self.dimensions = Vector2D(width, height)
        self.connection = Thread(target=self.open)
        self.connection.start()
        self.__running = True
        while not self.ready and self.__running:
            pass
        sleep(0.1)

    def open(self) -> None:
        if system() == "Linux":
            self.open_linux()
        elif system() == "Mac"
            print("--TODO")
            self.__running = False
            raise OSError            
        else:
            self.__running = False
            raise OSError

    def open_linux(self) -> None:
        self.lib = CDLL("libX11.so")
        self.lib.XOpenDisplay.restype = c_void_p
        self.lib.XOpenDisplay.argtypes = [c_char_p]
        self.display = self.lib.XOpenDisplay(None)

        if not self.display:
            print("\033[38;2;255mMiniView Failed to Open: "
                  "XOpenDisplay returned None.\033[0m")
            return

        self.lib.XDefaultRootWindow.argtypes = [c_void_p]
        self.lib.XDefaultRootWindow.restype = c_ulong
        self.__RW = self.lib.XDefaultRootWindow(self.display)

        self.lib.XCreateSimpleWindow.argtypes = [c_void_p,
                                                 c_ulong,
                                                 c_uint,
                                                 c_uint,
                                                 c_uint,
                                                 c_uint,
                                                 c_ulong,
                                                 c_ulong]
        self.lib.XCreateSimpleWindow.restype = c_ulong

        self.window = self.lib.XCreateSimpleWindow(self.display,
                                                   self.__RW,
                                                   0, 0,
                                                   self.dimensions.x,
                                                   self.dimensions.y,
                                                   0x000000,
                                                   0x000000)

        self.lib.XMapWindow.argtypes = [c_void_p, c_ulong]
        self.lib.XMapWindow.restypes = c_int
        self.lib.XMapWindow(self.display, self.window)

        self.lib.XSelectInput.argtypes = [c_void_p, c_ulong, c_long]
        self.lib.XSelectInput.restype = c_int

        KeyPressMask = 1 << 0
        KeyReleaseMask = 1 << 1
        ButtonPressMask = 1 << 2
        ButtonReleaseMask = 1 << 3
        ExposureMask = 1 << 15
        StructureNotifyMask = 1 << 17

        self.lib.XSelectInput(self.display, self.window, KeyPressMask |
                              KeyReleaseMask | ButtonPressMask |
                              ButtonReleaseMask | ExposureMask |
                              StructureNotifyMask)

        class XEvent(Structure):
            _fields_ = [
                ("pad", c_long * 24)
            ]

        self.lib.XNextEvent.argtypes = [c_void_p, c_void_p]
        self.lib.XNextEvent.restype = c_int

        self.lib.XInternAtom.argtypes = [c_void_p, c_char_p, c_int]
        self.lib.XInternAtom.restype = c_ulong

        self.lib.XSetWMProtocols.argtypes = [
            c_void_p, c_ulong, POINTER(c_ulong), c_int
        ]
        self.lib.XSetWMProtocols.restype = c_int

        eventlist = XEvent()
        wm_delete = self.lib.XInternAtom(
            self.display,
            b"WM_DELETE_WINDOW",
            False
        )
        atoms = (c_ulong * 1)(wm_delete)
        self.lib.XSetWMProtocols(self.display, self.window,
                                 atoms, 1)

        self.lib.XSetForeground.argtypes = [c_void_p, c_void_p, c_ulong]

        self.lib.XSetForeground
        self.lib.XFlush.argtypes = [c_void_p]
        self.lib.XPending.argtypes = [c_void_p]
        self.lib.XPending.restype = c_int

        self.ready = True
        while self.__running:
            for obj in self.objects.values():
                obj.show(self)
            while self.lib.XPending(self.display):
                self.lib.XNextEvent(self.display,
                                    byref(eventlist))
                if eventlist.pad[0] == 33:
                    self.__running = False
                    break
            self.lib.XFlush(self.display)
            sleep(1/120)

    def insert(self, object: Object, name: str) -> None:
        self.objects[name] = object
