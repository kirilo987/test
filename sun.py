from turtle import *

t = Turtle()
t.speed(0)
t.pensize(2)

# Функція для малювання сонця (жовте коло)
def draw_sun_body(radius):
    t.penup()
    t.goto(0, -radius)
    t.pendown()
    t.color("orange", "yellow")
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Функція для малювання одного променя
def draw_ray(length, angle):
    t.penup()
    t.goto(0, 0)
    t.setheading(angle)
    t.forward(60)
    t.pendown()
    t.color("gold")
    t.forward(length)
    t.penup()

# Малювання сонця
draw_sun_body(60)

# Малювання 12 променів навколо
for i in range(12):
    draw_ray(40, i * 30)

done()