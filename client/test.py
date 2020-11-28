
import numpy as np
import pyglet
from pyglet.gl import *

WIDTH = 800
HEIGHT = 600

window = pyglet.window.Window(WIDTH, HEIGHT)

my_arr = np.zeros((200, 400, 3), dtype='uint8')
my_arr[:, :, 0] = 255

print(my_arr)

drawing = False


print("Change the Size by pressing the buttons Z,X, and C")
print("Change the Color by pressing the buttons R,B, and G")

currentColor = [255, 0, 0] # Starting Color that changes as one presses R,G,B
currentSize = 1

dots = [[-100, -100]]  # Array of arrays that each contain a different shape
colors = [[1, 0, 0]]  # List of Colors for each individual drawn item
sizes = [1]

temp = []  # Temp Shape array until the array is added into the dats array


@window.event
def on_draw():
    data = my_arr.copy()
    data.shape = -1

    print(data)

    # tex_data_working = my_arr.flatten('F').data.__str__()
    tex_data = (GLubyte * data.size)(*data)
    image = pyglet.image.ImageData(200, 400, "RGB", tex_data, 200*3*1) #shape[0] * num_channels * bytes per channel
    print(image.get_data())
    image.blit(0, 0)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global drawing
    if button == pyglet.window.mouse.LEFT:
        drawing = True
        my_arr[x, y] = currentColor


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons == pyglet.window.mouse.LEFT:
        my_arr[x, y] = currentColor


@window.event
def on_mouse_release(x, y, button, modifiers):
    global drawing
    if button == pyglet.window.mouse.LEFT:
        drawing = False


@window.event
def on_key_press(key, modifiers):
    global currentColor, currentSize

    if key == pyglet.window.key.R:  # Colors
        print("Color: RED")
        currentColor = [255, 0, 0]
    if key == pyglet.window.key.G:
        print("Color: GREEN")
        currentColor = [0, 255, 0]
    if key == pyglet.window.key.B:
        print("Color: BLUE")
        currentColor = [0, 0, 255]

    if key == pyglet.window.key.Z:  # Sizes
        print("Size: 1")
        currentSize = 1
    if key == pyglet.window.key.X:
        print("Size: 2")
        currentSize = 5
    if key == pyglet.window.key.C:
        print("Size: 3")
        currentSize = 10


if __name__ == "__main__":
    #
    # a = np.zeros((3, 4, 4), dtype='uint8')
    # a[0, :, :] = 1
    # a[1, :, :] = 2
    # a[2, :, :] = 3
    # print(a.flatten('F')

    pyglet.app.run()
    pass
