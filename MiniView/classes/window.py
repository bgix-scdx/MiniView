from typing import Any, Callable
from ctypes import c_void_p, c_int, c_char_p, c_ulong, POINTER, c_uint
from ctypes import c_long, Structure, CDLL, byref, c_bool
from time import sleep
from platform import system


class Window():
    # dimensions: Vector2D
    name: str = "MiniView"
    __running: bool = False
    lib: Any
    display: Any
    __RW: Any
    ready: bool = False
    window: Any
    icon: str = "MiniView/default_assets/images/icon.png"

    def __init__(self, name: str, width: int, height: int,
                 starting_func: Callable | None = None) -> None:
        self.name = name
        self.dimensions = [width, height]
        self.open()
        self.__running = True

    def open(self) -> None:
        self.__running = True
        try:
            if system() == "Linux":
                self.open_linux()
            elif system() == "Darwin":
                self.open_mac()
            else:
                raise OSError
        except OSError:
            self.__running = False
            raise OSError

    def open_mac(self) -> None:
        import ctypes.util
        self.lib = CDLL(ctypes.util.find_library("objc"))
        CDLL(ctypes.util.find_library("Cocoa"))

        self.lib.objc_getClass.restype = c_void_p
        self.lib.objc_getClass.argtypes = [c_char_p]

        self.lib.sel_registerName.restype = c_void_p
        self.lib.sel_registerName.argtypes = [c_char_p]

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p]
        self.lib.objc_msgSend.restype = c_void_p

        NSApp = self.lib.objc_getClass(b"NSApplication")
        SharedApp = self.lib.sel_registerName(b"sharedApplication")

        app = self.lib.objc_msgSend(NSApp, SharedApp)

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_long]
        self.lib.objc_msgSend(app,
                              self.lib.sel_registerName(
                                  b"setActivationPolicy:"), 0)

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p]
        self.lib.objc_msgSend(app,
                              self.lib.sel_registerName(b"finishLaunching"))

        class NSRect(Structure):
            _fields_ = [
                ("x", ctypes.c_double),
                ("y", ctypes.c_double),
                ("width", ctypes.c_double),
                ("height", ctypes.c_double),
            ]

        frame = NSRect(100, 100, self.dimensions[0], self.dimensions[1])
        style_mask = 1 | 2 | 4 | 8

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p]
        win = self.lib.objc_msgSend(self.lib.objc_getClass(b"NSWindow"),
                                    self.lib.sel_registerName(b"alloc"))
        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, NSRect,
                                          c_ulong, c_ulong, c_bool]
        style = b"initWithContentRect:styleMask:backing:defer:"
        win = self.lib.objc_msgSend(win,
                                    self.lib.sel_registerName(style),
                                    frame, style_mask, 2, False)

        # icon image

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
        ns_imagestr = self.lib.objc_msgSend(self.lib.objc_getClass(
                                                b"NSString"),
                                            self.lib.sel_registerName(
                                                b"stringWithUTF8String:"),
                                            str(self.icon).encode())

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p]
        ns_alloc = self.lib.objc_msgSend(self.lib.objc_getClass(b"NSImage"),
                                         self.lib.sel_registerName(b"alloc"))

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
        ns_image = self.lib.objc_msgSend(ns_alloc,
                                         self.lib.sel_registerName(
                                             b"initWithContentsOfFile:"),
                                         ns_imagestr)

        self.lib.objc_msgSend(app,
                              self.lib.sel_registerName(
                                  b"setApplicationIconImage:"),
                              ns_image)

        # window name

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_char_p]
        ns_title = self.lib.objc_msgSend(self.lib.objc_getClass(b"NSString"),
                                         self.lib.sel_registerName(
                                             b"stringWithUTF8String:"),
                                         self.name.encode())

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
        self.lib.objc_msgSend(win, self.lib.sel_registerName(b"setTitle:"),
                              ns_title)

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_bool]
        self.lib.objc_msgSend(app,
                              self.lib.sel_registerName(
                                  b"activateIgnoringOtherApps:"),
                              True)

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
        self.lib.objc_msgSend(win,
                              self.lib.sel_registerName(
                                  b"makeKeyAndOrderFront:"),
                              None)

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p]
        self.lib.objc_msgSend(win, self.lib.sel_registerName(b"display"))

        self.window = win

        self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_char_p]

        NSDate = self.lib.objc_getClass(b"NSDate")
        NSDefaultRunLoopMode = self.lib.objc_msgSend(
            self.lib.objc_getClass(b"NSString"),
            self.lib.sel_registerName(b"stringWithUTF8String:"),
            b"kCFRunLoopDefaultMode"
        )

        self.ready = True

        while self.__running:
            self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p]
            distant_future = self.lib.objc_msgSend(NSDate,
                                                   self.lib.sel_registerName(
                                                       b"distantFuture"))
            self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p,
                                              c_ulong, c_void_p, c_void_p,
                                              c_bool]
            event = self.lib.objc_msgSend(app, self.lib.sel_registerName(
                b"nextEventMatchingMask:untilDate:inMode:dequeue:"),
                c_ulong(0xFFFFFFFFFFFFFFFF), distant_future,
                NSDefaultRunLoopMode, True)

            if event:
                self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p, c_void_p]
                self.lib.objc_msgSend(app,
                                      self.lib.sel_registerName(b"sendEvent:"),
                                      event)
            self.lib.objc_msgSend.argtypes = [c_void_p, c_void_p]
            is_visible = self.lib.objc_msgSend(win, self.lib.sel_registerName(
                                                b"isVisible"))
            if not is_visible:
                self.__running = False
                break
            sleep(1/120)

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
                                                   self.dimensions[0],
                                                   self.dimensions[1],
                                                   0x000000,
                                                   0x000000)

        self.lib.XMapWindow.restypes = c_int
        self.lib.XMapWindow.argtypes = [c_void_p, c_ulong]
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
            while self.lib.XPending(self.display):
                self.lib.XNextEvent(self.display,
                                    byref(eventlist))
                if eventlist.pad[0] == 33:
                    self.__running = False
                    break
            self.lib.XFlush(self.display)
            sleep(1/120)
