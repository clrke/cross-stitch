import turtle
from math import sqrt
from PIL import Image
import sys

FRAME_SIZE = 700
PEN_SIZE = 4
PIXEL_DIFFERENCE_THRESHOLD = 40
PIXEL_DRAW_THRESHOLD = 230

EAST = True
WEST = False


class Pixel:
    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb


def stitch_pixel(pixel, xkey, ykey, forward_distance):
    turtle.pencolor(pixel.rgb)

    turtle.penup()
    turtle.goto(xkey(pixel), ykey(pixel))
    turtle.pendown()

    turtle.forward(forward_distance)


def stitch(pixels, length=FRAME_SIZE):
    turtle.left(45)

    half_frame = FRAME_SIZE / 2

    pixel_length = FRAME_SIZE / length
    forward_distance = sqrt(pixel_length ** 2 * 2)

    def get_start_x(p):
        return p.x * pixel_length - half_frame

    def get_start_y(p):
        return p.y * pixel_length - half_frame

    for pixel in pixels:
        stitch_pixel(pixel, get_start_x, get_start_y, forward_distance)

    turtle.right(90)

    def get_start_y(p):
        return (p.y + 1) * pixel_length - half_frame

    for pixel in reversed(pixels):
        stitch_pixel(pixel, get_start_x, get_start_y, forward_distance)

    turtle.left(45)


def get_pixel_average(pixel):
    return sum(pixel) / len(pixel)


def get_pixel_difference(pixel1, pixel2):
    pixel_average1 = get_pixel_average(pixel1)
    pixel_average2 = get_pixel_average(pixel2)

    return abs(pixel_average1 - pixel_average2)


def get_pixels_to_draw(pixels, length, rgb):
    direction = EAST

    for y in range(length):
        row = range(length)
        if direction == WEST:
            row.reverse()

        row_has_pixel_to_draw = False

        for x in row:
            pixel = pixels[x, y][:3]
            pixel_average = sum(pixel) / len(pixel)
            if get_pixel_difference(pixel, rgb) < PIXEL_DIFFERENCE_THRESHOLD \
                    and pixel_average < PIXEL_DRAW_THRESHOLD:
                yield Pixel(x, length - y, pixel)
                row_has_pixel_to_draw = True

        if row_has_pixel_to_draw:
            direction = not direction


def draw(filename):
    image = Image.open(filename)
    pixels = image.load()

    turtle.speed(0)
    turtle.pensize(PEN_SIZE)
    turtle.colormode(255)
    turtle.hideturtle()

    colors_drawn = []

    length = image.size[1]

    for y in range(length):
        for x in range(length):
            pixel = pixels[x, y][:3]

            pixel_average = get_pixel_average(pixel)

            if pixel not in colors_drawn \
                    and pixel_average < PIXEL_DRAW_THRESHOLD:
                pixels_to_draw = list(get_pixels_to_draw(pixels, length, pixel))

                for pixel_to_draw in pixels_to_draw:
                    if pixel_to_draw.rgb not in colors_drawn:
                        colors_drawn.append(pixel_to_draw.rgb)

                stitch(pixels_to_draw, length)

    turtle.exitonclick()


def main():
    if len(sys.argv) < 2:
        print "Usage:   python cross_stitch.py <image filename>"
        print "Example: python cross_stitch.py pythonph.resized.png"

        return

    filename = sys.argv[1]

    draw(filename)


if __name__ == '__main__':
    main()
