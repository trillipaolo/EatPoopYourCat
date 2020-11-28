import numpy as np
import pyglet
from pyglet.gl import *

WIDTH = 800
HEIGHT = 600
SCALE = 4

window = pyglet.window.Window(WIDTH, HEIGHT)
last_point = [0, 0]

matrix = np.zeros((3, WIDTH // SCALE, HEIGHT // SCALE), dtype=np.uint8)

print("Change the Color by pressing the buttons R,B, and G")

current_color = np.array([255, 0, 0])
size = 1


@window.event
def on_draw():
    data = (GLubyte * matrix.size)(*matrix.flatten('F'))
    img = pyglet.image.ImageData(WIDTH // SCALE, HEIGHT // SCALE, "RGB", data, matrix.shape[1] * 3 * 1)
    img.blit(0, 0, width=WIDTH, height=HEIGHT)


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        compute_point(x, y)


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    last_x = x - dx
    last_y = y - dy
    if button == pyglet.window.mouse.LEFT:
        compute_line(last_x, last_y, x, y)


def compute_point(x_screen, y_screen):
    x = np.clip(size - 1, x_screen, WIDTH - size) // SCALE
    y = np.clip(size - 1, y_screen, HEIGHT - size) // SCALE
    draw_point(x, y)


def draw_point(x, y):
    sn = int(np.floor(size / 2))
    sp = int(np.ceil(size / 2))
    matrix[:, x - sn:x + sp, y - sn:y + sp] = \
        np.pad(current_color.reshape((3, 1, 1)),
               ((0, 0), (0, size - 1), (0, size - 1)), mode='edge')


def compute_line(x_last_screen, y_last_screen, x_screen, y_screen):
    low_border = (size // 2) * 5
    high_border = 4 - int(np.ceil(size / 2)) * 5
    x0 = np.clip(low_border, x_last_screen, WIDTH + high_border)
    x1 = np.clip(low_border, x_screen, WIDTH + high_border)
    y0 = np.clip(low_border, y_last_screen, HEIGHT + high_border)
    y1 = np.clip(low_border, y_screen, HEIGHT + high_border)

    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            draw_line_low(x1, y1, x0, y0)
        else:
            draw_line_low(x0, y0, x1, y1)
    else:
        if y0 > y1:
            draw_line_high(x1, y1, x0, y0)
        else:
            draw_line_high(x0, y0, x1, y1)


def draw_line_high(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx

    D = (2 * dx) - dy
    x = x0

    for y in range(y0, y1):
        draw_point(x//SCALE, y//SCALE)
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2 * dx


def draw_line_low(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy

    D = (2 * dy) - dx
    y = y0

    for x in range(x0, x1):
        draw_point(x//SCALE, y//SCALE)
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2 * dy


@window.event
def on_key_press(key, modifiers):
    global current_color, size

    if key == pyglet.window.key.R:  # Colors
        print("Color: RED")
        current_color = np.array([255, 0, 0])
    if key == pyglet.window.key.G:
        print("Color: GREEN")
        current_color = np.array([0, 255, 0])
    if key == pyglet.window.key.B:
        print("Color: BLUE")
        current_color = np.array([0, 0, 255])

    if key == pyglet.window.key.Q:  # Sizes
        print("Size: 1")
        size = 1
    if key == pyglet.window.key.W:
        print("Size: 2")
        size = 2
    if key == pyglet.window.key.E:
        print("Size: 3")
        size = 3
    if key == pyglet.window.key.R:
        print("Size: 4")
        size = 4


if __name__ == "__main__":
    pyglet.app.run()
