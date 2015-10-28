import turtle
from random import randint
from math import sqrt
from PIL import Image
import sys

filename = sys.argv[1]

FRAME_SIZE = 700
PEN_SIZE = 4
PIXEL_THRESHOLD = 230


class Pixel():
	"""docstring for Pixel"""
	def __init__(self, x, y, rgb):
		self.x = x
		self.y = y
		self.rgb = rgb


def stitch(pixels, length=FRAME_SIZE):

	turtle.left(45)

	half_frame = FRAME_SIZE / 2

	forward_distance = sqrt(
		(FRAME_SIZE/length) ** 2 +
		(FRAME_SIZE/length) ** 2)

	for pixel in pixels:
		turtle.penup()
		turtle.goto(
			pixel.x*FRAME_SIZE/length-half_frame,
			pixel.y*FRAME_SIZE/length-half_frame
		)
		turtle.pendown()

		turtle.pencolor(pixel.rgb)
		turtle.forward(forward_distance)

	turtle.right(90)

	for pixel in reversed(pixels):
		turtle.penup()
		turtle.goto(
			pixel.x*FRAME_SIZE/length-half_frame,
			(pixel.y+1)*FRAME_SIZE/length-half_frame
		)
		turtle.pendown()

		turtle.pencolor(pixel.rgb)
		turtle.forward(forward_distance)

	turtle.left(45)


def get_pixel_average(pixel):
    return sum(pixel) / len(pixel)


def get_pixel_distance(pixel1, pixel2):
	pixel_average1 = get_pixel_average(pixel1)
	pixel_average2 = get_pixel_average(pixel2)

	return abs(pixel_average1 - pixel_average2)


def get_pixels_to_draw(pixels, length, rgb):
	direction = 0

	for y in range(length):
		row = range(length)
		if direction == 1:
			row.reverse()

		found = False
		for x in row:
			pixel = pixels[x, y]
			pixel_average = sum(pixel) / len(pixel)
			if get_pixel_distance(pixel, rgb) < 40 and pixel_average < 230:
				yield Pixel(x, length-y, pixel)
				found = True

		if found:
			direction = 1 if direction == 0 else 0


im = Image.open(filename)
pixels = im.load()

turtle.speed(0)
turtle.pensize(PEN_SIZE)
turtle.colormode(255)
turtle.hideturtle()

colors_drawn = []

length = im.size[1]

for y in range(length):
	for x in range(length):
		pixel = pixels[x, y]
		pixel_average = get_pixel_average(pixel)

		if pixels[x, y] not in colors_drawn and pixel_average < PIXEL_THRESHOLD:
			pixels_to_draw = list(get_pixels_to_draw(pixels, length, pixel))

			for pixel_to_draw in pixels_to_draw:
				if pixel_to_draw.rgb not in colors_drawn:
					colors_drawn.append(pixel_to_draw.rgb)

			stitch(pixels_to_draw, length)

turtle.exitonclick()

