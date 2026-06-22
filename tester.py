from MiniView import Window, Vector2D, Object
from time import sleep


visual: Window = Window("MiniView", 16 * 100, 10 * 100)
obj: Object = Object()
visual.insert(obj, "Baka")
print("Hello World")

sleep(5)

obj.position = Vector2D(100, 100)
