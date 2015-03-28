import turtle
from random import randint
from math import sqrt
from PIL import Image
import sys

filename = sys.argv[1]

class Pixel():
	"""docstring for Pixel"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

def stitch(pixels, rgb, length=400):
	turtle.pencolor(rgb)

	turtle.left(45)

	half_frame = 200

	forward_distance = sqrt(
		(400/length) ** 2 +
		(400/length) ** 2
	)

	for pixel in pixels:
		turtle.penup()
		turtle.goto(
			pixel.x*400/length-half_frame,
			pixel.y*400/length-half_frame
		)
		turtle.pendown()

		turtle.forward(forward_distance)

	turtle.right(90)

	for pixel in reversed(pixels):
		turtle.penup()
		turtle.goto(
			pixel.x*400/length-half_frame,
			(pixel.y+1)*400/length-half_frame
		)
		turtle.pendown()

		turtle.forward(forward_distance)

	turtle.left(45)

def get_pixels_to_draw(pixels, length, rgb):
	direction = 0

	for y in reversed(range(length)):
		row = range(length)
		if direction == 1:
			row.reverse()

		found = False
		for x in row:
			if pixels[x, y] == rgb:
				yield Pixel(x, length-y)
				found = True

		if found:
			direction = 1 if direction == 0 else 0

im = Image.open(filename)
pixels = im.load()

turtle.speed(0)
turtle.pensize(3)
turtle.colormode(255)
turtle.hideturtle()

colors_drawn = []

length = im.size[0]

for y in range(length):
	for x in range(length):
		pixel = pixels[x, y]
		pixel_average = sum(pixel) / len(pixel)

		if pixels[x, y] not in colors_drawn and pixel_average < 230:
			colors_drawn.append(pixel)
			stitch(
				list(get_pixels_to_draw(pixels, length, pixel)),
				pixels[x,y],
				length
			)

turtle.exitonclick()
