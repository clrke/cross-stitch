import turtle
from random import randint
from math import sqrt

class Pixel():
	"""docstring for Pixel"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

def stitch(pixels, rgb, length=400):
	turtle.color(rgb)

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

pixels = [
	Pixel(0, 3),
	Pixel(3, 3),
	Pixel(3, 0),
	Pixel(0, 0),
]

stitch(pixels, (0, 0, 0), 4)

turtle.exitonclick()
